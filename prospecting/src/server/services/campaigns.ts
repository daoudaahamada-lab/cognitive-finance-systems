import type { Prisma, ProspectStage } from "@prisma/client";
import { z } from "zod";
import { db } from "@/server/db";
import { MAX_FOLLOW_UPS } from "@/server/domain/followups";
import { INVITE_NOTE_MAX, malformedVariables, suggestVariable, unknownVariables } from "@/server/domain/templates";
import { engineDeps } from "@/server/engine/deps";
import { insertProspects, scoreNewProspects } from "@/server/engine/sourcing";
import { getProvider } from "@/server/linkedin";
import { launchReadiness } from "./campaign-insights";
import { UserError, type ActionState } from "./errors";

/** A user error that belongs to one form field: the builder shows it under that field. */
export class CampaignFieldError extends UserError {
  field: string;
  constructor(field: string, message: string) {
    super(message);
    this.field = field;
  }
}

/** Accepts a JSON array (tag inputs) or newline/comma separated text. */
function parseList(value: unknown): unknown {
  if (Array.isArray(value)) return value;
  if (typeof value !== "string" || value.trim() === "") return [];
  const text = value.trim();
  if (text.startsWith("[")) {
    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  }
  return text.split(/[\n,;]/).map((s) => s.trim()).filter(Boolean);
}

function parseJson(value: unknown): unknown {
  if (typeof value !== "string") return value;
  try {
    return JSON.parse(value || "[]");
  } catch {
    return value;
  }
}

/** A tag list. Every message is French: TagInput limits neither the number nor the length of tags. */
const list = (max = 50) =>
  z.preprocess(
    parseList,
    z
      .array(z.string({ error: "Élément invalide" }).trim().min(1, "Élément vide").max(200, "200 caractères maximum par élément"), { error: "Liste invalide" })
      .max(max, `${max} éléments maximum`),
  );

/** Browsers submit textarea content with CRLF line endings; messages use LF. */
const text = () => z.string().transform((v) => v.replace(/\r\n?/g, "\n"));

/** "variable inconnue {{prenom}}. Utilisez une des variables listées." */
export function unknownVariablesMessage(names: string[]): string {
  const quoted = names.map((n) => `{{${n}}}`).join(", ");
  return `${names.length > 1 ? "variables inconnues" : "variable inconnue"} ${quoted}. Utilisez une des variables listées.`;
}

/** "variable mal écrite {prenom} : utilisez {{firstName}}." */
export function malformedVariablesMessage(names: string[]): string {
  const written = names.map((n) => `{${n}}`).join(", ");
  const meant = names.map((n) => `{{${suggestVariable(n) ?? n}}}`).join(", ");
  return `${names.length > 1 ? "variables mal écrites" : "variable mal écrite"} ${written} : utilisez ${meant}.`;
}

const knownVariablesOnly = (prefix: string) => (value: string, ctx: z.RefinementCtx) => {
  const unknown = unknownVariables(value);
  if (unknown.length > 0) ctx.addIssue({ code: "custom", message: `${prefix}${unknownVariablesMessage(unknown)}` });
  // Single braces ({prenom}) are not variables: they would reach the prospect as written.
  const malformed = malformedVariables(value);
  if (malformed.length > 0) ctx.addIssue({ code: "custom", message: `${prefix}${malformedVariablesMessage(malformed)}` });
};

const template = (label: string, max: number) =>
  text().pipe(z.string().trim().max(max, `${label} : ${max} caractères maximum`).superRefine(knownVariablesOnly(`${label} : `)));

/** One follow-up. Messages leave out "Relance N : ", which parseCampaignForm adds from the step's position. */
const followUpStep = z.object({
  delayDays: z.number({ error: "délai invalide" }).int("délai en jours entiers").min(1, "1 jour minimum").max(30, "30 jours maximum"),
  template: text().pipe(z.string().trim().min(1, "texte requis").max(2000, "2000 caractères maximum").superRefine(knownVariablesOnly(""))),
});

/** Searching needs something to search for: a title, a keyword or the user's own LinkedIn search URL. */
export const SEARCH_TARGETING_MESSAGE = "Ajoutez au moins un poste ou un mot-clé, ou collez une URL de recherche LinkedIn";

export function lacksSearchTargeting(c: { sources: readonly string[]; searchUrl: string; titles: readonly string[]; keywords: readonly string[] }): boolean {
  return c.sources.includes("SEARCH") && c.searchUrl.trim() === "" && c.titles.length === 0 && c.keywords.length === 0;
}

const targetingFields = z.object({ sources: z.array(z.string()), searchUrl: z.string(), titles: z.array(z.string()), keywords: z.array(z.string()) });

export const campaignSchema = z.object({
  name: z.string({ error: "Nom requis" }).trim().min(1, "Nom requis").max(120, "120 caractères maximum"),
  accountId: z.string({ error: "Choisissez un compte LinkedIn" }).min(1, "Choisissez un compte LinkedIn"),
  sources: z.preprocess(parseList, z.array(z.enum(["SEARCH", "SIGNALS", "POST_ENGAGERS", "PROFILE_VISITORS"], "Source inconnue"), { error: "Sources invalides" })),
  titles: list(),
  keywords: list(),
  industries: list(),
  locations: list(),
  companySizes: list(),
  signals: z.preprocess(parseList, z.array(z.enum(["NEW_ROLE", "HIRING", "FUNDRAISING"], "Signal inconnu"), { error: "Signaux invalides" })),
  postUrls: z.preprocess(parseList, z.array(z.url("URL de post invalide"), { error: "Liste invalide" }).max(10, "10 posts maximum")),
  searchUrl: z
    .string()
    .trim()
    .default("")
    .refine((v) => v === "" || /^https:\/\/([a-z]+\.)?linkedin\.com\/search\/results\/people\//i.test(v), {
      message: "Collez une URL de recherche de personnes LinkedIn (linkedin.com/search/results/people/…). Sales Navigator n'est pas pris en charge.",
    }),
  exclusions: list(100),
  minScore: z.coerce.number({ error: "Score entre 0 et 100" }).int("Score entre 0 et 100").min(0, "Score entre 0 et 100").max(100, "Score entre 0 et 100"),
  weeklyProspectTarget: z.coerce.number({ error: "Nombre entier attendu" }).int("Nombre entier attendu").min(10, "10 au minimum").max(1000, "1000 au maximum"),
  offer: text().pipe(z.string().trim().max(3000, "3000 caractères maximum")),
  persona: text().pipe(z.string().trim().max(3000, "3000 caractères maximum")),
  aiPersonalization: z.preprocess((v) => v === true || v === "on" || v === "true", z.boolean()),
  inviteNote: template("Note d'invitation", INVITE_NOTE_MAX).transform((v) => (v === "" ? null : v)),
  firstMessage: template("Premier message", 2000).refine((v) => v.length > 0, "Premier message requis"),
  followUps: z.preprocess(parseJson, z.array(followUpStep, { error: "Relances invalides" }).max(MAX_FOLLOW_UPS, `${MAX_FOLLOW_UPS} relances au maximum`)),
  setterMode: z.enum(["OFF", "APPROVAL", "AUTO"], "Choisissez un mode du setter"),
  bookingUrl: z.union([z.url("Lien de réservation invalide"), z.literal("")]),
}).refine((c) => !lacksSearchTargeting(c), {
  message: SEARCH_TARGETING_MESSAGE,
  path: ["titles"],
  // Also checked when other fields are invalid, so every error shows at once.
  when: (payload) => targetingFields.safeParse(payload.value).success,
});

export type CampaignInput = z.infer<typeof campaignSchema>;

/**
 * Validates the builder's form data. Errors are keyed by field, and follow-up errors by step
 * ("followUps.0" for Relance 1), so each one shows under its own textarea.
 */
export function parseCampaignForm(data: unknown): { data: CampaignInput } | { state: ActionState } {
  const parsed = campaignSchema.safeParse(data);
  if (parsed.success) return { data: parsed.data };
  const fieldErrors: Record<string, string> = {};
  for (const issue of parsed.error.issues) {
    const [field, index] = issue.path;
    const step = field === "followUps" && typeof index === "number" ? index : null;
    if (step === null) fieldErrors[String(field ?? "form")] ??= issue.message;
    else fieldErrors[`followUps.${step}`] ??= `Relance ${step + 1} : ${issue.message}`;
  }
  return { state: { error: "Certains champs sont invalides.", fieldErrors } };
}

async function checkCampaign(workspaceId: string, input: CampaignInput) {
  const account = await db.linkedInAccount.findFirst({ where: { id: input.accountId, workspaceId, status: { not: "DISCONNECTED" } } });
  if (!account) throw new CampaignFieldError("accountId", "Ce compte LinkedIn n'est plus connecté : choisissez-en un autre.");
}

export async function createCampaign(workspaceId: string, input: CampaignInput) {
  await checkCampaign(workspaceId, input);
  return db.campaign.create({
    data: { ...input, workspaceId, followUps: input.followUps as Prisma.InputJsonValue, status: "DRAFT" },
  });
}

export async function updateCampaign(workspaceId: string, campaignId: string, input: CampaignInput) {
  await checkCampaign(workspaceId, input);
  const existing = await db.campaign.findFirst({ where: { id: campaignId, workspaceId } });
  if (!existing) throw new UserError("Campagne introuvable.");
  const targetingChanged = (["sources", "searchUrl", "titles", "keywords", "industries", "locations", "companySizes", "signals", "postUrls"] as const).some(
    (k) => JSON.stringify(existing[k]) !== JSON.stringify(input[k]),
  );
  await db.campaign.update({
    where: { id: campaignId },
    data: {
      ...input,
      followUps: input.followUps as Prisma.InputJsonValue,
      // New targeting means new searches: restart pagination.
      ...(targetingChanged ? { sourcingState: {} } : {}),
    },
  });
}

export async function setCampaignStatus(workspaceId: string, campaignId: string, status: "ACTIVE" | "PAUSED" | "ARCHIVED") {
  const campaign = await db.campaign.findFirst({ where: { id: campaignId, workspaceId }, include: { account: true } });
  if (!campaign) throw new UserError("Campagne introuvable.");
  if (status === "ACTIVE") {
    if (campaign.account.status !== "ACTIVE") {
      throw new UserError("Le compte LinkedIn de cette campagne n'est pas actif : réparez-le dans Comptes LinkedIn.");
    }
    if (lacksSearchTargeting(campaign)) throw new CampaignFieldError("titles", `${SEARCH_TARGETING_MESSAGE}.`);
    // Same checklist as the campaign page, so the MCP tools cannot launch what the button refuses.
    const workspace = await db.workspace.findUniqueOrThrow({ where: { id: workspaceId }, select: { bookingUrl: true, offer: true } });
    const blocker = (await launchReadiness(campaign, workspace)).checks.find((check) => check.level === "blocker");
    if (blocker) throw new UserError(blocker.detail);
  }
  await db.campaign.update({
    where: { id: campaignId },
    data: { status, ...(status === "ACTIVE" && !campaign.launchedAt ? { launchedAt: new Date() } : {}) },
  });
}

export type StageCounts = Partial<Record<ProspectStage, number>>;

export async function stageCounts(where: Prisma.ProspectWhereInput): Promise<StageCounts> {
  const rows = await db.prospect.groupBy({ by: ["stage"], where, _count: true });
  return Object.fromEntries(rows.map((r) => [r.stage, r._count]));
}

/** Prospects that reached at least each funnel step. */
export function funnelFromStages(c: StageCounts) {
  const n = (...stages: ProspectStage[]) => stages.reduce((sum, s) => sum + (c[s] ?? 0), 0);
  const afterReply = n("REPLIED", "MEETING_BOOKED", "NOT_INTERESTED");
  const afterMessage = afterReply + n("MESSAGED", "UNRESPONSIVE");
  const afterConnect = afterMessage + n("CONNECTED");
  const afterInvite = afterConnect + n("INVITED");
  return {
    found: afterInvite + n("NEW", "QUALIFIED", "DISQUALIFIED"),
    qualified: afterInvite + n("QUALIFIED"),
    invited: afterInvite,
    connected: afterConnect,
    messaged: afterMessage,
    replied: afterReply,
    meetings: n("MEETING_BOOKED"),
  };
}

export async function listCampaigns(workspaceId: string) {
  const campaigns = await db.campaign.findMany({
    where: { workspaceId, status: { not: "ARCHIVED" } },
    include: { account: { select: { fullName: true } } },
    orderBy: { createdAt: "desc" },
  });
  const order: Record<string, number> = { ACTIVE: 0, PAUSED: 1, DRAFT: 2 };
  campaigns.sort((a, b) => (order[a.status] ?? 3) - (order[b.status] ?? 3));
  return Promise.all(campaigns.map(async (c) => ({ ...c, funnel: funnelFromStages(await stageCounts({ campaignId: c.id })) })));
}

export async function getCampaign(workspaceId: string, campaignId: string) {
  return db.campaign.findFirst({ where: { id: campaignId, workspaceId }, include: { account: true } });
}

const LINKEDIN_PROFILE_URL = /https?:\/\/(?:[a-z]{2,3}\.)?linkedin\.com\/in\/[^\s,;"'<>]+/gi;
export const IMPORT_MAX = 1000;

/** Imports any LinkedIn profile URLs found in pasted text or a CSV export. */
export async function importProspects(workspaceId: string, campaignId: string, text: string) {
  const campaign = await db.campaign.findFirst({ where: { id: campaignId, workspaceId }, include: { account: true, workspace: true } });
  if (!campaign) throw new UserError("Campagne introuvable.");
  const urls = [...new Set((text.match(LINKEDIN_PROFILE_URL) ?? []).map((u) => u.replace(/\/+$/, "")))];
  if (urls.length === 0) throw new UserError("Aucune URL de profil LinkedIn (linkedin.com/in/...) trouvée.");
  if (urls.length > IMPORT_MAX) throw new UserError(`${IMPORT_MAX} profils maximum par import.`);

  const deps = engineDeps();
  const profiles = await getProvider(db, campaign.account.provider).lookupProfiles({ externalId: campaign.account.externalId }, urls);
  const imported = await insertProspects(deps, campaign, profiles, "IMPORT");
  await scoreNewProspects(deps, campaign, IMPORT_MAX);
  return { found: urls.length, imported, skipped: urls.length - imported };
}
