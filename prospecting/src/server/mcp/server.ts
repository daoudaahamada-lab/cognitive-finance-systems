import type { CallToolResult } from "@modelcontextprotocol/sdk/types.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { agentLabel } from "@/server/agents";
import { db } from "@/server/db";
import { DEFAULT_FIRST_MESSAGE, DEFAULT_FOLLOW_UPS, DEFAULT_INVITE_NOTE } from "@/server/domain/campaign-defaults";
import { MAX_FOLLOW_UPS, parseFollowUps } from "@/server/domain/followups";
import { engineDeps } from "@/server/engine/deps";
import { runTick } from "@/server/engine/tick";
import { listAccounts } from "@/server/services/accounts";
import { dashboard } from "@/server/services/analytics";
import { attentionItems } from "@/server/services/attention";
import { campaignSchema, createCampaign, funnelFromStages, getCampaign, importProspects, listCampaigns, setCampaignStatus, stageCounts, updateCampaign } from "@/server/services/campaigns";
import { UserError } from "@/server/services/errors";
import { INBOX_TABS, approveDraft, getThread, handBackToAi, listConversations, logMeeting, markHandled, rejectDraft, sendHumanReply, takeOver } from "@/server/services/inbox";
import { listMeetings, setMeetingStatus } from "@/server/services/meetings";
import { applyManualStage, getProspect, listProspects, saveNotes, snoozeProspect } from "@/server/services/prospects";
import type { TokenIdentity } from "@/server/services/tokens";
import { BRAND } from "@/lib/brand";

const INSTRUCTIONS = `${BRAND.name} automatise la prospection LinkedIn B2B : sourcing, scoring, invitations, messages, relances, et un setter qui répond aux prospects et réserve des rendez-vous.
Pour faire le point, commence par get_overview (son champ attention liste ce qui attend l'utilisateur, le plus urgent d'abord) puis list_conversations (onglet "todo" : ce qui attend une décision humaine).
approve_draft, send_reply et hand_back_to_setter envoient de vrais messages LinkedIn au nom de l'utilisateur : montre-lui le texte et attends son accord avant de les appeler.
Les quotas LinkedIn et les horaires d'envoi sont appliqués par le moteur ; aucun outil ne permet de les dépasser.`;

const STAGES = ["NEW", "QUALIFIED", "DISQUALIFIED", "INVITED", "CONNECTED", "MESSAGED", "REPLIED", "MEETING_BOOKED", "NOT_INTERESTED", "UNRESPONSIVE"] as const;
const id = (what: string) => z.string().min(1).describe(`Identifiant ${what}`);
const list = (what: string) => z.array(z.string().min(1)).describe(what);

function json(data: unknown): CallToolResult {
  return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
}

async function run(fn: () => Promise<unknown>): Promise<CallToolResult> {
  try {
    return json(await fn());
  } catch (error) {
    if (error instanceof UserError || error instanceof z.ZodError) {
      const message = error instanceof z.ZodError ? error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ") : error.message;
      return { isError: true, content: [{ type: "text", text: message }] };
    }
    console.error("[mcp] tool failed", error);
    return { isError: true, content: [{ type: "text", text: "Erreur interne : voir les journaux du serveur." }] };
  }
}

/** Drops keys whose value is undefined, so they never overwrite defaults or stored values. */
function provided<T extends object>(values: T): Partial<T> {
  return Object.fromEntries(Object.entries(values).filter(([, v]) => v !== undefined)) as Partial<T>;
}

function name(p: { firstName: string; lastName: string }) {
  return `${p.firstName} ${p.lastName}`;
}

/** One MCP server per request, bound to the workspace of the token that called it. */
export function buildMcpServer(identity: TokenIdentity): McpServer {
  const ws = identity.workspaceId;
  const server = new McpServer({ name: BRAND.name.toLowerCase(), version: "1.0.0" }, { instructions: INSTRUCTIONS });
  const read = { readOnlyHint: true, openWorldHint: false } as const;

  // ---------------------------------------------------------------- Monitor
  server.registerTool(
    "get_overview",
    {
      title: "Vue d'ensemble",
      description: "Ce qui attend l'utilisateur (attention : comptes en pause ou en erreur, moteur arrêté, actions LinkedIn impossibles, campagnes épuisées, rendez-vous à confirmer, conversations à traiter), indicateurs de la période et de la période précédente, entonnoir, prochains rendez-vous, quotas des comptes et agents actifs.",
      inputSchema: { days: z.union([z.literal(7), z.literal(30), z.literal(90)]).default(30).describe("Période en jours") },
      annotations: read,
    },
    ({ days }) =>
      run(async () => {
        const [data, accounts, attention] = await Promise.all([dashboard(ws, days), listAccounts(ws), attentionItems(ws)]);
        return {
          periodDays: days,
          agents: agentLabel(),
          attention,
          kpis: data.kpis,
          previousKpis: data.previousKpis,
          funnel: data.funnel,
          inbox: data.inbox,
          upcomingMeetings: data.upcomingMeetings.map((m) => ({ id: m.id, startsAt: m.startsAt, prospect: name(m.prospect), company: m.prospect.company, prospectId: m.prospect.id })),
          accounts: accounts.map((a) => ({ id: a.id, name: a.fullName, status: a.status, limits: a.quota.limits, usage: a.quota.usage })),
        };
      }),
  );

  server.registerTool(
    "list_accounts",
    { title: "Comptes LinkedIn", description: "Comptes LinkedIn connectés : statut, type, horaires d'envoi, plafonds et consommation des quotas.", annotations: read },
    () =>
      run(async () =>
        (await listAccounts(ws)).map((a) => ({
          id: a.id,
          name: a.fullName,
          provider: a.provider,
          type: a.accountType,
          status: a.status,
          statusReason: a.statusReason,
          invitesPausedUntil: a.invitesPausedUntil,
          sending: { days: a.sendingDays, from: a.sendingStart, to: a.sendingEnd, timezone: a.timezone },
          limits: a.quota.limits,
          usage: a.quota.usage,
          activeCampaigns: a._count.campaigns,
        })),
      ),
  );

  server.registerTool(
    "list_campaigns",
    { title: "Campagnes", description: "Campagnes non archivées avec leur statut, leur compte et leur entonnoir.", annotations: read },
    () =>
      run(async () =>
        (await listCampaigns(ws)).map((c) => ({ id: c.id, name: c.name, status: c.status, account: c.account.fullName, setterMode: c.setterMode, funnel: c.funnel })),
      ),
  );

  server.registerTool(
    "get_campaign",
    { title: "Détail d'une campagne", description: "Ciblage, offre, séquence de messages, setter et entonnoir d'une campagne.", inputSchema: { campaignId: id("de la campagne") }, annotations: read },
    ({ campaignId }) =>
      run(async () => {
        const c = await getCampaign(ws, campaignId);
        if (!c) throw new UserError("Campagne introuvable.");
        return {
          id: c.id,
          name: c.name,
          status: c.status,
          accountId: c.accountId,
          targeting: { sources: c.sources, searchUrl: c.searchUrl, titles: c.titles, keywords: c.keywords, industries: c.industries, locations: c.locations, companySizes: c.companySizes, signals: c.signals, postUrls: c.postUrls, exclusions: c.exclusions, minScore: c.minScore, weeklyProspectTarget: c.weeklyProspectTarget },
          offer: c.offer,
          persona: c.persona,
          sequence: { aiPersonalization: c.aiPersonalization, inviteNote: c.inviteNote, firstMessage: c.firstMessage, followUps: parseFollowUps(c.followUps) },
          setter: { mode: c.setterMode, bookingUrl: c.bookingUrl },
          funnel: funnelFromStages(await stageCounts({ campaignId: c.id })),
        };
      }),
  );

  // ------------------------------------------------------- Decide & understand
  server.registerTool(
    "list_conversations",
    {
      title: "Conversations",
      description: "Conversations avec les prospects. Onglets : todo (attend une décision humaine), drafts (réponses proposées par le setter, à valider), ai (gérées par le setter), all.",
      inputSchema: { tab: z.enum(INBOX_TABS).default("todo"), query: z.string().optional().describe("Filtre sur le nom ou l'entreprise"), limit: z.number().int().min(1).max(100).default(30) },
      annotations: read,
    },
    ({ tab, query, limit }) =>
      run(async () =>
        (await listConversations(ws, tab, query)).slice(0, limit).map((c) => ({
          id: c.id,
          prospect: { name: name(c.prospect), title: c.prospect.title, company: c.prospect.company, stage: c.prospect.stage },
          status: c.status,
          escalationReason: c.escalationReason,
          lastIntent: c.lastIntent,
          unread: c.unread,
          lastMessage: c.messages[0] ? { from: c.messages[0].author, text: c.messages[0].body, at: c.messages[0].sentAt } : null,
          pendingDraftId: c.drafts[0]?.id ?? null,
        })),
      ),
  );

  server.registerTool(
    "get_conversation",
    { title: "Lire une conversation", description: "Fil complet d'une conversation, avec le prospect, la réponse proposée en attente et la raison d'une éventuelle escalade.", inputSchema: { conversationId: id("de la conversation") }, annotations: read },
    ({ conversationId }) =>
      run(async () => {
        const t = await getThread(ws, conversationId);
        if (!t) throw new UserError("Conversation introuvable.");
        return {
          id: t.id,
          status: t.status,
          escalationReason: t.escalationReason,
          lastIntent: t.lastIntent,
          prospect: { id: t.prospect.id, name: name(t.prospect), title: t.prospect.title, company: t.prospect.company, stage: t.prospect.stage, campaign: t.prospect.campaign.name },
          messages: t.messages.map((m) => ({ from: m.author, text: m.body, at: m.sentAt })),
          pendingDraft: t.drafts[0] ? { id: t.drafts[0].id, text: t.drafts[0].body, intent: t.drafts[0].intent, rationale: t.drafts[0].rationale, author: t.drafts[0].author } : null,
          meeting: t.prospect.meetings[0] ? { startsAt: t.prospect.meetings[0].startsAt, status: t.prospect.meetings[0].status } : null,
        };
      }),
  );

  server.registerTool(
    "approve_draft",
    {
      title: "Valider une réponse proposée",
      description: "Envoie sur LinkedIn la réponse proposée par le setter, telle quelle ou modifiée. Envoie un vrai message : obtiens l'accord de l'utilisateur sur le texte avant.",
      inputSchema: { draftId: id("de la réponse proposée"), editedMessage: z.string().min(1).max(8000).optional().describe("Texte modifié à envoyer à la place de la réponse proposée") },
      annotations: { destructiveHint: false, openWorldHint: true },
    },
    ({ draftId, editedMessage }) => run(async () => (await approveDraft(ws, draftId, editedMessage), { sent: true })),
  );

  server.registerTool(
    "reject_draft",
    { title: "Refuser une réponse proposée", description: "Écarte la réponse proposée par le setter ; la conversation passe à l'humain.", inputSchema: { draftId: id("de la réponse proposée") }, annotations: { destructiveHint: false, openWorldHint: false } },
    ({ draftId }) => run(async () => (await rejectDraft(ws, draftId), { rejected: true })),
  );

  server.registerTool(
    "send_reply",
    {
      title: "Répondre à un prospect",
      description: "Envoie un message rédigé par l'utilisateur dans une conversation. Envoie un vrai message LinkedIn : obtiens son accord sur le texte avant.",
      inputSchema: {
        conversationId: id("de la conversation"),
        message: z.string().min(1).max(8000),
        handBackToSetter: z.boolean().default(false).describe("Rendre ensuite la conversation au setter"),
      },
      annotations: { destructiveHint: false, openWorldHint: true },
    },
    ({ conversationId, message, handBackToSetter }) => run(async () => (await sendHumanReply(ws, conversationId, message, handBackToSetter), { sent: true })),
  );

  server.registerTool(
    "hand_back_to_setter",
    {
      title: "Rendre au setter",
      description: "Rend la conversation au setter. Si le prospect attend une réponse, le setter répond ou propose une réponse à valider, selon le mode de la campagne.",
      inputSchema: { conversationId: id("de la conversation") },
      annotations: { destructiveHint: false, openWorldHint: true },
    },
    ({ conversationId }) => run(async () => (await handBackToAi(ws, conversationId), { status: "AI_ACTIVE" })),
  );

  server.registerTool(
    "take_over_conversation",
    { title: "Prendre la main", description: "Le setter arrête de répondre dans cette conversation.", inputSchema: { conversationId: id("de la conversation") }, annotations: { destructiveHint: false, openWorldHint: false } },
    ({ conversationId }) => run(async () => (await takeOver(ws, conversationId), { status: "HUMAN" })),
  );

  server.registerTool(
    "mark_conversation_handled",
    { title: "Marquer traité", description: "Retire la conversation de l'onglet « à traiter ».", inputSchema: { conversationId: id("de la conversation") }, annotations: { destructiveHint: false, openWorldHint: false, idempotentHint: true } },
    ({ conversationId }) => run(async () => (await markHandled(ws, conversationId), { handled: true })),
  );

  // -------------------------------------------------------------- Prospects
  server.registerTool(
    "list_prospects",
    {
      title: "Prospects",
      description: "Prospects filtrés par étape, campagne, texte ou score minimum. 50 par page.",
      inputSchema: {
        stage: z.enum(STAGES).optional(),
        campaignId: z.string().optional(),
        query: z.string().optional().describe("Nom, entreprise ou poste"),
        minScore: z.number().int().min(0).max(100).optional(),
        sort: z.enum(["recent", "score"]).default("recent"),
        page: z.number().int().min(1).default(1),
      },
      annotations: read,
    },
    (args) =>
      run(async () => {
        const result = await listProspects(ws, { ...args, q: args.query });
        return {
          total: result.total,
          page: result.page,
          pages: result.pages,
          prospects: result.rows.map((p) => ({ id: p.id, name: name(p), title: p.title, company: p.company, location: p.location, score: p.score, stage: p.stage, signal: p.signal, campaign: p.campaign.name, updatedAt: p.stageChangedAt })),
        };
      }),
  );

  server.registerTool(
    "get_prospect",
    { title: "Fiche prospect", description: "Profil, score et raisons, historique, notes, conversation et rendez-vous d'un prospect.", inputSchema: { prospectId: id("du prospect") }, annotations: read },
    ({ prospectId }) =>
      run(async () => {
        const p = await getProspect(ws, prospectId);
        if (!p) throw new UserError("Prospect introuvable.");
        return {
          id: p.id,
          name: name(p),
          headline: p.headline,
          title: p.title,
          company: p.company,
          companySize: p.companySize,
          industry: p.industry,
          location: p.location,
          profileUrl: p.profileUrl,
          signal: p.signal,
          signalDetail: p.signalDetail,
          stage: p.stage,
          score: p.score,
          scoreSummary: p.scoreSummary,
          scoreReasons: p.scoreReasons,
          scoredBy: p.scoredBy,
          disqualifiedReason: p.disqualifiedReason,
          campaign: p.campaign.name,
          notes: p.notes,
          snoozedUntil: p.snoozedUntil,
          conversationId: p.conversation?.id ?? null,
          meetings: p.meetings.map((m) => ({ id: m.id, startsAt: m.startsAt, status: m.status })),
          history: p.activities.slice(0, 30).map((a) => ({ type: a.type, at: a.createdAt, data: a.data })),
        };
      }),
  );

  server.registerTool(
    "set_prospect_status",
    {
      title: "Changer le statut d'un prospect",
      description: "exclude : ne jamais le contacter (avant toute conversation). requalify : remettre un prospect écarté dans la file. not_interested : clore.",
      inputSchema: { prospectId: id("du prospect"), action: z.enum(["exclude", "requalify", "not_interested"]) },
      annotations: { destructiveHint: false, openWorldHint: false },
    },
    ({ prospectId, action }) => run(async () => (await applyManualStage(ws, prospectId, action), { updated: true })),
  );

  server.registerTool(
    "snooze_prospect",
    { title: "Mettre en veille", description: "Suspend toute action sur le prospect pendant N jours (0 pour réveiller).", inputSchema: { prospectId: id("du prospect"), days: z.number().int().min(0).max(365) }, annotations: { destructiveHint: false, openWorldHint: false, idempotentHint: true } },
    ({ prospectId, days }) => run(async () => (await snoozeProspect(ws, prospectId, days), { snoozedDays: days })),
  );

  server.registerTool(
    "save_prospect_notes",
    { title: "Notes sur un prospect", description: "Remplace les notes du prospect.", inputSchema: { prospectId: id("du prospect"), notes: z.string().max(5000) }, annotations: { destructiveHint: false, openWorldHint: false, idempotentHint: true } },
    ({ prospectId, notes }) => run(async () => (await saveNotes(ws, prospectId, notes), { saved: true })),
  );

  server.registerTool(
    "import_prospects",
    {
      title: "Importer des prospects",
      description: "Ajoute des profils LinkedIn (URL linkedin.com/in/...) à une campagne. Ils sont contactés quel que soit leur score, sauf exclusion.",
      inputSchema: { campaignId: id("de la campagne"), profileUrls: z.array(z.string().url()).min(1).max(1000) },
      annotations: { destructiveHint: false, openWorldHint: true },
    },
    ({ campaignId, profileUrls }) => run(() => importProspects(ws, campaignId, profileUrls.join("\n"))),
  );

  // ------------------------------------------------------------- Configure
  const campaignFields = {
    name: z.string().min(1).max(120).optional(),
    titles: list("Postes ciblés").optional(),
    keywords: list("Mots-clés").optional(),
    industries: list("Secteurs").optional(),
    locations: list("Zones").optional(),
    companySizes: z.array(z.enum(["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"])).optional(),
    sources: z.array(z.enum(["SEARCH", "SIGNALS", "POST_ENGAGERS", "PROFILE_VISITORS"])).optional(),
    signals: z.array(z.enum(["NEW_ROLE", "HIRING", "FUNDRAISING"])).optional(),
    postUrls: z.array(z.string().url()).max(10).optional(),
    searchUrl: z.string().optional().describe("URL de recherche de personnes LinkedIn à utiliser telle quelle (vide pour la construire depuis les postes et mots-clés)"),
    exclusions: list("Termes d'exclusion").optional(),
    minScore: z.number().int().min(0).max(100).optional(),
    weeklyProspectTarget: z.number().int().min(10).max(1000).optional(),
    offer: z.string().max(3000).optional(),
    persona: z.string().max(3000).optional(),
    aiPersonalization: z.boolean().optional(),
    inviteNote: z.string().max(300).optional().describe("Vide pour inviter sans note"),
    firstMessage: z.string().min(1).max(2000).optional(),
    followUps: z.array(z.object({ delayDays: z.number().int().min(1).max(30), template: z.string().min(1).max(2000) })).max(MAX_FOLLOW_UPS).optional(),
    setterMode: z.enum(["OFF", "APPROVAL", "AUTO"]).optional(),
    bookingUrl: z.string().optional().describe("Lien de réservation, vide pour celui des réglages"),
  };

  server.registerTool(
    "create_campaign",
    {
      title: "Créer une campagne",
      description: "Crée une campagne en brouillon. Les champs omis prennent des valeurs par défaut (offre et client idéal des réglages, séquence type, setter en validation). Variables de message : {{firstName}}, {{company}}, {{title}}, {{bookingUrl}}…",
      inputSchema: { ...campaignFields, name: z.string().min(1).max(120), accountId: z.string().optional().describe("Compte LinkedIn ; par défaut le premier compte actif") },
      annotations: { destructiveHint: false, openWorldHint: false },
    },
    (args) =>
      run(async () => {
        const workspace = await db.workspace.findUniqueOrThrow({ where: { id: ws } });
        const accountId = args.accountId ?? (await db.linkedInAccount.findFirst({ where: { workspaceId: ws, status: "ACTIVE" }, orderBy: { createdAt: "asc" } }))?.id;
        if (!accountId) throw new UserError("Aucun compte LinkedIn actif : connectez-en un d'abord.");
        const defaults = {
          sources: ["SEARCH"], titles: [], keywords: [], industries: [], locations: [], companySizes: [], signals: [], postUrls: [], exclusions: [],
          searchUrl: "", minScore: 60, weeklyProspectTarget: 100, offer: workspace.offer, persona: workspace.persona, aiPersonalization: true,
          inviteNote: DEFAULT_INVITE_NOTE, firstMessage: DEFAULT_FIRST_MESSAGE, followUps: DEFAULT_FOLLOW_UPS, setterMode: "APPROVAL", bookingUrl: "",
        };
        const input = campaignSchema.parse({
          ...defaults,
          ...provided(args),
          accountId,
        });
        const campaign = await createCampaign(ws, input);
        return { id: campaign.id, status: campaign.status, next: "Relisez la campagne puis lancez-la avec set_campaign_status." };
      }),
  );

  server.registerTool(
    "update_campaign",
    {
      title: "Modifier une campagne",
      description: "Modifie seulement les champs fournis (ciblage, offre, séquence, setter). Les changements s'appliquent aux prochaines actions du moteur.",
      inputSchema: { campaignId: id("de la campagne"), ...campaignFields },
      annotations: { destructiveHint: false, openWorldHint: false, idempotentHint: true },
    },
    ({ campaignId, ...changes }) =>
      run(async () => {
        const c = await getCampaign(ws, campaignId);
        if (!c) throw new UserError("Campagne introuvable.");
        const defined = provided(changes);
        const input = campaignSchema.parse({ ...c, inviteNote: c.inviteNote ?? "", followUps: parseFollowUps(c.followUps), ...defined });
        await updateCampaign(ws, campaignId, input);
        return { updated: Object.keys(defined) };
      }),
  );

  server.registerTool(
    "set_campaign_status",
    {
      title: "Lancer, suspendre ou archiver",
      description: "ACTIVE lance la campagne (le moteur commence à prospecter et à envoyer), PAUSED la suspend, ARCHIVED l'arrête et la retire de la liste.",
      inputSchema: { campaignId: id("de la campagne"), status: z.enum(["ACTIVE", "PAUSED", "ARCHIVED"]) },
      annotations: { destructiveHint: true, openWorldHint: true },
    },
    ({ campaignId, status }) => run(async () => (await setCampaignStatus(ws, campaignId, status), { status })),
  );

  // -------------------------------------------------------------- Schedule
  server.registerTool(
    "list_meetings",
    { title: "Rendez-vous", description: "Rendez-vous à venir et passés.", annotations: read },
    () =>
      run(async () => {
        const { upcoming, past } = await listMeetings(ws);
        const shape = (m: (typeof upcoming)[number]) => ({ id: m.id, startsAt: m.startsAt, status: m.status, origin: m.origin, prospect: name(m.prospect), prospectId: m.prospect.id, company: m.prospect.company, campaign: m.campaign.name });
        return { upcoming: upcoming.map(shape), past: past.slice(0, 30).map(shape) };
      }),
  );

  server.registerTool(
    "log_meeting",
    { title: "Enregistrer un rendez-vous", description: "Enregistre un rendez-vous pris hors setter ; la conversation est close.", inputSchema: { prospectId: id("du prospect"), startsAt: z.string().describe("Date et heure ISO 8601, ex. 2026-10-20T14:00:00+02:00") }, annotations: { destructiveHint: false, openWorldHint: false } },
    ({ prospectId, startsAt }) => run(async () => (await logMeeting(ws, prospectId, new Date(startsAt)), { logged: true })),
  );

  server.registerTool(
    "set_meeting_status",
    { title: "Statut d'un rendez-vous", description: "Indique si un rendez-vous a eu lieu, si le prospect était absent, ou s'il est annulé.", inputSchema: { meetingId: id("du rendez-vous"), status: z.enum(["SCHEDULED", "COMPLETED", "NO_SHOW", "CANCELED"]) }, annotations: { destructiveHint: false, openWorldHint: false, idempotentHint: true } },
    ({ meetingId, status }) => run(async () => (await setMeetingStatus(ws, meetingId, status), { status })),
  );

  // ---------------------------------------------------------------- Engine
  server.registerTool(
    "run_engine",
    {
      title: "Synchroniser maintenant",
      description: "Exécute un passage du moteur maintenant (Vela le fait en continu tant qu'il est lancé) : synchronisation LinkedIn, sourcing, scoring, envois dus dans les quotas et horaires.",
      annotations: { destructiveHint: false, openWorldHint: true },
    },
    () =>
      run(async () => {
        const results = await runTick(engineDeps(), { workspaceId: ws });
        return results.map((r) => ({ accountId: r.accountId, events: r.events, sourced: r.sourced, scored: r.scored, invites: r.outreach?.invites ?? 0, messages: r.outreach?.messages ?? 0, skipped: r.outreach?.skipped, error: r.error }));
      }),
  );

  return server;
}
