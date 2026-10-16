import type { Prisma, ProspectStage } from "@prisma/client";
import { z } from "zod";
import { db } from "@/server/db";
import { followUpsSchema } from "@/server/domain/followups";
import { INVITE_NOTE_MAX, unknownVariables } from "@/server/domain/templates";
import { engineDeps } from "@/server/engine/deps";
import { insertProspects, scoreNewProspects } from "@/server/engine/sourcing";
import { getProvider } from "@/server/linkedin";
import { UserError } from "./errors";

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

const list = (max = 50) => z.preprocess(parseList, z.array(z.string().trim().min(1).max(200)).max(max));

/** Browsers submit textarea content with CRLF line endings; messages use LF. */
const text = () => z.string().transform((v) => v.replace(/\r\n?/g, "\n"));

const template = (label: string, max: number) =>
  text().pipe(
    z.string().trim().max(max, `${label} : ${max} caractères maximum`).refine((t) => unknownVariables(t).length === 0, {
      message: `${label} : variable inconnue`,
    }),
  );

export const campaignSchema = z.object({
  name: z.string().trim().min(1, "Nom requis").max(120),
  accountId: z.string().min(1, "Choisissez un compte LinkedIn"),
  sources: z.preprocess(parseList, z.array(z.enum(["SEARCH", "SIGNALS", "POST_ENGAGERS", "PROFILE_VISITORS"]))),
  titles: list(),
  keywords: list(),
  industries: list(),
  locations: list(),
  companySizes: list(),
  signals: z.preprocess(parseList, z.array(z.enum(["NEW_ROLE", "HIRING", "FUNDRAISING"]))),
  postUrls: z.preprocess(parseList, z.array(z.url("URL de post invalide")).max(10)),
  searchUrl: z
    .string()
    .trim()
    .default("")
    .refine((v) => v === "" || /^https:\/\/([a-z]+\.)?linkedin\.com\/search\/results\/people\//i.test(v), {
      message: "Collez une URL de recherche de personnes LinkedIn (linkedin.com/search/results/people/…). Sales Navigator n'est pas pris en charge.",
    }),
  exclusions: list(100),
  minScore: z.coerce.number().int().min(0).max(100),
  weeklyProspectTarget: z.coerce.number().int().min(10).max(1000),
  offer: text().pipe(z.string().trim().max(3000)),
  persona: text().pipe(z.string().trim().max(3000)),
  aiPersonalization: z.preprocess((v) => v === true || v === "on" || v === "true", z.boolean()),
  inviteNote: template("Note d'invitation", INVITE_NOTE_MAX).transform((v) => (v === "" ? null : v)),
  firstMessage: template("Premier message", 2000).refine((v) => v.length > 0, "Premier message requis"),
  followUps: z.preprocess(parseJson, followUpsSchema),
  setterMode: z.enum(["OFF", "APPROVAL", "AUTO"]),
  bookingUrl: z.union([z.url("Lien de réservation invalide"), z.literal("")]),
});

export type CampaignInput = z.infer<typeof campaignSchema>;

async function checkCampaign(workspaceId: string, input: CampaignInput) {
  for (const [i, step] of input.followUps.entries()) {
    if (unknownVariables(step.template).length > 0) throw new UserError(`Relance ${i + 1} : variable inconnue.`);
  }
  const account = await db.linkedInAccount.findFirst({ where: { id: input.accountId, workspaceId, status: { not: "DISCONNECTED" } } });
  if (!account) throw new UserError("Compte LinkedIn introuvable.");
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
    if (campaign.account.status !== "ACTIVE") throw new UserError("Le compte LinkedIn de cette campagne n'est pas actif.");
    const hasProspects = await db.prospect.count({ where: { campaignId } });
    if (campaign.sources.length === 0 && hasProspects === 0) {
      throw new UserError("Ajoutez une source de prospects ou importez une liste avant de lancer la campagne.");
    }
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
