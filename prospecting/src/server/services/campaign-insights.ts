import type { Campaign, LinkedInAccount, ProspectStage, Workspace } from "@prisma/client";
import { formatAgo, formatNumber } from "@/lib/format";
import { SETTER_MODES } from "@/lib/labels";
import { agentMode, type AgentMode } from "@/server/agents";
import { db } from "@/server/db";
import { FIRST_MESSAGE_DELAY_HOURS, parseFollowUps, sequenceEndDay, sequenceTimeline } from "@/server/domain/followups";
import { isWithinSendingWindow } from "@/server/domain/schedule";
import { DAY } from "@/server/domain/time";
import { isRealAccount } from "@/server/engine/pace";

/**
 * What the campaign page says about a campaign beyond its raw fields: whether it can be launched,
 * what the engine will do next, and which values (campaign or workspace) actually apply.
 */

type CampaignWithAccount = Campaign & { account: LinkedInAccount };
type WorkspaceDefaults = Pick<Workspace, "bookingUrl" | "offer">;

/** Anchors of the campaign editor sections (/campaigns/<id>/edit#<section>), as campaign-form.tsx names its cards. */
export type EditSection = "general" | "ciblage" | "offre" | "sequence" | "setter";

export function editHref(campaignId: string, section: EditSection): string {
  return `/campaigns/${campaignId}/edit#${section}`;
}

// ---------------------------------------------------------------------------
// French wording helpers
// ---------------------------------------------------------------------------

/** "a", "a et b", "a, b et c". */
export function joinFr(items: string[]): string {
  if (items.length <= 1) return items[0] ?? "";
  return `${items.slice(0, -1).join(", ")} et ${items.at(-1)}`;
}

/** Cumulative follow-up days: "J+3 et J+8" for delays [3, 5]; "" without follow-ups. */
export function followUpDays(followUps: { delayDays: number }[]): string {
  return joinFr(sequenceTimeline(followUps).map((s) => `J+${s.dayFromFirst}`));
}

/** "J+3 et J+8 après le premier message" or "Aucune relance". */
export function followUpSummary(followUps: { delayDays: number }[]): string {
  return followUps.length ? `${followUpDays(followUps)} après le premier message` : "Aucune relance";
}

/** Personalisation as it really behaves: without Claude, templates are sent as they are. */
export function personalizationLabel(enabled: boolean, mode: AgentMode = agentMode()): string {
  if (!enabled) return "Désactivée (modèles envoyés tels quels)";
  return mode === "claude" ? "Activée : Claude adapte chaque message au profil" : "Activée, sans effet tant que Claude n'est pas configuré";
}

const DAY_NAMES = ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"];

function hourLabel(value: string): string {
  const [h = "0", m = "00"] = value.split(":");
  return m === "00" ? `${Number(h)} h` : `${Number(h)} h ${m}`;
}

function daysLabel(days: number[]): string {
  const sorted = [...new Set(days)].filter((d) => d >= 1 && d <= 7).sort((a, b) => a - b);
  if (sorted.length === 7) return "tous les jours";
  if (sorted.length === 0) return "aucun jour";
  const contiguous = sorted.every((d, i) => i === 0 || d === sorted[i - 1]! + 1);
  if (contiguous && sorted.length >= 3) return `${DAY_NAMES[sorted[0]! - 1]}–${DAY_NAMES[sorted.at(-1)! - 1]}`;
  return joinFr(sorted.map((d) => DAY_NAMES[d - 1]!));
}

/** "lun–ven 9 h–18 h", "tous les jours 24 h/24". The time zone is named when it is not Paris. */
export function sendingWindowLabel(account: Pick<LinkedInAccount, "sendingDays" | "sendingStart" | "sendingEnd" | "timezone">): string {
  const hours = account.sendingStart === account.sendingEnd ? "24 h/24" : `${hourLabel(account.sendingStart)}–${hourLabel(account.sendingEnd)}`;
  const zone = account.timezone && account.timezone !== "Europe/Paris" ? ` (${account.timezone})` : "";
  return `${daysLabel(account.sendingDays)} ${hours}${zone}`;
}

/** Ends a fragment with exactly one full stop, so reasons can be followed by another sentence. */
export function withPeriod(text: string): string {
  const trimmed = text.trim().replace(/\s*[.;:,]+$/, "");
  return /[!?…]$/.test(trimmed) ? trimmed : `${trimmed}.`;
}

/** First sentence of a text (the setter's short answer for the offer). */
export function firstSentence(text: string): string {
  const trimmed = text.trim();
  const match = /^[\s\S]*?[.!?…](?=\s|$)/.exec(trimmed);
  return (match ? match[0] : trimmed).replace(/\s+/g, " ");
}

// ---------------------------------------------------------------------------
// Effective settings: campaign value, or the workspace default when it is empty
// ---------------------------------------------------------------------------

export type SettingOrigin = "campaign" | "workspace" | "none";
export type EffectiveSetting = { value: string; origin: SettingOrigin };

function effective(own: string, fallback: string): EffectiveSetting {
  if (own.trim()) return { value: own.trim(), origin: "campaign" };
  if (fallback.trim()) return { value: fallback.trim(), origin: "workspace" };
  return { value: "", origin: "none" };
}

/** The booking link and offer the engine and the setter actually use (see engine/vars.ts and outreach.ts). */
export function effectiveSettings(campaign: Pick<Campaign, "bookingUrl" | "offer">, workspace: WorkspaceDefaults) {
  const offer = effective(campaign.offer, workspace.offer);
  return {
    bookingUrl: effective(campaign.bookingUrl, workspace.bookingUrl),
    offer: { ...offer, value: firstSentence(offer.value) },
  };
}

// ---------------------------------------------------------------------------
// Launch readiness
// ---------------------------------------------------------------------------

/** ok: done; info: a recommendation; warn: works but may disappoint; blocker: launching would fail or do harm. */
export type CheckLevel = "ok" | "info" | "warn" | "blocker";

export type ReadinessCheck = {
  key: "account" | "session" | "targeting" | "booking" | "signals" | "setter";
  level: CheckLevel;
  label: string;
  detail: string;
  /** Where to fix it, with the link text. */
  fix?: { href: string; label: string };
};

export type ReadinessInput = {
  campaign: CampaignWithAccount;
  workspace: WorkspaceDefaults;
  /** Prospects already attached to the campaign (imports, for a draft). */
  prospectCount: number;
  now?: Date;
};

function targetingCheck(campaign: CampaignWithAccount, prospectCount: number): ReadinessCheck {
  const base = { key: "targeting" as const, label: "Ciblage renseigné" };
  const fix = { href: editHref(campaign.id, "ciblage"), label: "Compléter le ciblage" };
  const { sources } = campaign;
  const real = isRealAccount(campaign.account);
  const imported = prospectCount > 0 ? `${formatNumber(prospectCount)} profil${prospectCount > 1 ? "s" : ""} importé${prospectCount > 1 ? "s" : ""}` : null;

  if (sources.length === 0 && prospectCount === 0) {
    return { ...base, level: "blocker", detail: "Aucune source de prospects : choisissez-en une ou importez une liste.", fix };
  }
  if (sources.includes("SEARCH") && !campaign.searchUrl.trim() && campaign.titles.length === 0 && campaign.keywords.length === 0) {
    return { ...base, level: "blocker", detail: "La recherche n'a aucun critère : ajoutez au moins un poste ou un mot-clé, ou collez une URL de recherche LinkedIn.", fix };
  }
  // Sources that cannot find anyone on their own.
  const useful = sources.filter((s) => !(s === "SIGNALS" && real) && !(s === "POST_ENGAGERS" && campaign.postUrls.length === 0));
  if (sources.length > 0 && useful.length === 0 && prospectCount === 0) {
    const detail = sources.includes("POST_ENGAGERS") && campaign.postUrls.length === 0
      ? "Aucun post à surveiller : ajoutez des URL de posts, une autre source ou importez une liste."
      : "Les sources choisies ne trouvent personne avec ce compte : ajoutez la recherche ou importez une liste.";
    return { ...base, level: "blocker", detail, fix };
  }

  const parts: string[] = [];
  if (campaign.searchUrl.trim()) parts.push("URL de recherche LinkedIn");
  if (campaign.titles.length) parts.push(`${campaign.titles.length} poste${campaign.titles.length > 1 ? "s" : ""}`);
  if (campaign.keywords.length) parts.push(`${campaign.keywords.length} mot${campaign.keywords.length > 1 ? "s" : ""}-clé${campaign.keywords.length > 1 ? "s" : ""}`);
  if (sources.includes("POST_ENGAGERS") && campaign.postUrls.length) parts.push(`${campaign.postUrls.length} post${campaign.postUrls.length > 1 ? "s" : ""} surveillé${campaign.postUrls.length > 1 ? "s" : ""}`);
  if (imported) parts.push(imported);
  if (sources.includes("POST_ENGAGERS") && campaign.postUrls.length === 0) {
    return { ...base, level: "warn", detail: `${parts.join(" · ") || "Ciblage partiel"}. Aucun post à surveiller : la source « Engagement sur des posts » ne trouvera personne.`, fix };
  }
  return { ...base, level: "ok", detail: parts.join(" · ") || "Sources sans critère particulier" };
}

/** The checklist shown before launch. Any blocker disables 'Lancer la campagne'. */
export function readinessChecks({ campaign, workspace, prospectCount, now = new Date() }: ReadinessInput): ReadinessCheck[] {
  const { account } = campaign;
  const checks: ReadinessCheck[] = [];
  const accountFix = { href: `/accounts#${account.id}`, label: "Ouvrir Comptes LinkedIn" };

  // 1. The account the campaign sends from.
  if (account.status === "ACTIVE") {
    checks.push({ key: "account", level: "ok", label: "Compte LinkedIn actif", detail: account.fullName });
  } else if (account.status === "DISCONNECTED") {
    checks.push({
      key: "account", level: "blocker", label: "Compte LinkedIn actif",
      detail: `${account.fullName} est déconnecté : choisissez un autre compte pour cette campagne.`,
      fix: { href: editHref(campaign.id, "general"), label: "Changer de compte" },
    });
  } else {
    checks.push({
      key: "account", level: "blocker", label: "Compte LinkedIn actif",
      detail: `${withPeriod(`${account.fullName} est en pause${account.statusReason ? ` : ${account.statusReason}` : ""}`)} Réactivez-le dans Comptes LinkedIn.`,
      fix: accountFix,
    });
  }

  // 2. Browser accounts: the read-only connection check.
  if (account.provider === "browser") {
    if (account.lastDiagnosisOk === true) {
      checks.push({ key: "session", level: "ok", label: "Connexion vérifiée", detail: `Dernière vérification ${formatAgo(account.lastDiagnosedAt, now)}` });
    } else if (account.lastDiagnosisOk === false) {
      checks.push({
        key: "session", level: "warn", label: "Connexion vérifiée",
        detail: `La dernière vérification (${formatAgo(account.lastDiagnosedAt, now)}) a signalé un problème : corrigez-le puis relancez-la.`,
        fix: { ...accountFix, label: "Vérifier la connexion" },
      });
    } else {
      checks.push({
        key: "session", level: "warn", label: "Connexion vérifiée",
        detail: "Pas encore vérifiée : « Vérifier la connexion » teste la session sans rien envoyer.",
        fix: { ...accountFix, label: "Vérifier la connexion" },
      });
    }
  }

  // 3. Targeting.
  checks.push(targetingCheck(campaign, prospectCount));

  // 4. Booking link: the setter sends it to interested prospects.
  const { bookingUrl } = effectiveSettings(campaign, workspace);
  if (bookingUrl.origin !== "none") {
    checks.push({
      key: "booking", level: "ok", label: "Lien de réservation",
      detail: bookingUrl.origin === "campaign" ? "Propre à la campagne" : "Celui des Réglages",
    });
  } else if (campaign.setterMode !== "OFF") {
    checks.push({
      key: "booking", level: "blocker", label: "Lien de réservation",
      detail: "Le setter l'envoie aux prospects intéressés : renseignez-le dans les Réglages (ou dans la campagne).",
      fix: { href: "/settings", label: "Ouvrir les Réglages" },
    });
  } else {
    checks.push({ key: "booking", level: "info", label: "Lien de réservation", detail: "Aucun : facultatif tant que le setter est désactivé.", fix: { href: "/settings", label: "Ouvrir les Réglages" } });
  }

  // 5. Buying signals only exist in the simulator.
  if (campaign.sources.includes("SIGNALS") && isRealAccount(account)) {
    checks.push({
      key: "signals", level: "warn", label: "Signaux d'achat sans effet sur un vrai compte",
      detail: "Cette source ne trouve personne avec un vrai compte LinkedIn pour l'instant ; les autres sources continuent.",
      fix: { href: editHref(campaign.id, "ciblage"), label: "Modifier les sources" },
    });
  }

  // 6. Setter mode: start by reviewing its answers.
  if (campaign.setterMode === "APPROVAL") {
    checks.push({ key: "setter", level: "ok", label: "Setter en mode Validation", detail: "Vous relisez chaque réponse avant envoi." });
  } else {
    checks.push({
      key: "setter", level: "info", label: "Setter : Validation recommandé pour démarrer",
      detail: campaign.setterMode === "AUTO"
        ? "En Automatique, le setter répond seul dès les premières réponses. En Validation, vous relisez d'abord ce qu'il propose."
        : "Désactivé, toutes les réponses vous reviennent. En Validation, le setter vous propose une réponse à valider.",
      fix: { href: editHref(campaign.id, "setter"), label: "Changer de mode" },
    });
  }

  return checks;
}

export function isBlocked(checks: ReadinessCheck[]): boolean {
  return checks.some((c) => c.level === "blocker");
}

/** 'Ce qui va se passer': the settings read as what the engine will do. */
export function launchPlan(campaign: CampaignWithAccount, prospectCount: number): string[] {
  const followUps = parseFollowUps(campaign.followUps);
  const steps: string[] = [];
  if (campaign.sources.length > 0) {
    steps.push(`~${formatNumber(campaign.weeklyProspectTarget)} profils/semaine`, `invitation si note ≥ ${campaign.minScore}`);
  }
  if (prospectCount > 0) {
    steps.push(`${formatNumber(prospectCount)} profil${prospectCount > 1 ? "s" : ""} importé${prospectCount > 1 ? "s" : ""} invité${prospectCount > 1 ? "s" : ""} quelle que soit leur note`);
  }
  steps.push(`premier message ${FIRST_MESSAGE_DELAY_HOURS} h après acceptation`);
  steps.push(followUps.length ? `relance${followUps.length > 1 ? "s" : ""} à ${followUpDays(followUps)}` : "sans relance");
  steps.push(campaign.setterMode === "OFF" ? "setter désactivé" : `setter en mode ${SETTER_MODES[campaign.setterMode]?.label ?? campaign.setterMode}`);

  const sentences = [`${capitalize(steps.join(", "))}.`];
  sentences.push(
    `Envois ${sendingWindowLabel(campaign.account)} ; la séquence s'arrête dès que le prospect répond${followUps.length ? `, et à J+${sequenceEndDay(followUps)} sans réponse` : ""}.`,
  );
  return sentences;
}

function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

export type LaunchReadiness = { checks: ReadinessCheck[]; blocked: boolean; plan: string[]; prospectCount: number };

export async function launchReadiness(campaign: CampaignWithAccount, workspace: WorkspaceDefaults, now = new Date()): Promise<LaunchReadiness> {
  const prospectCount = await db.prospect.count({ where: { campaignId: campaign.id } });
  const checks = readinessChecks({ campaign, workspace, prospectCount, now });
  return { checks, blocked: isBlocked(checks), plan: launchPlan(campaign, prospectCount), prospectCount };
}

// ---------------------------------------------------------------------------
// Next actions of an active campaign
// ---------------------------------------------------------------------------

export type NextActions = {
  /** QUALIFIED prospects waiting for an invitation. */
  toInvite: number;
  /** Invitations not accepted yet. */
  pendingInvites: number;
  /** Accepted invitations whose first message is scheduled. */
  firstMessages: number;
  /** Follow-ups due in the next 24 hours. */
  followUpsSoon: number;
  window: { label: string; open: boolean };
  /** LinkedIn warned about the invitation limit: no invitations before this date. */
  invitesPausedUntil: Date | null;
  account: { id: string; fullName: string; status: LinkedInAccount["status"]; statusReason: string | null; lastError: string | null; lastErrorAt: Date | null };
};

export async function nextActions(campaign: CampaignWithAccount, now = new Date()): Promise<NextActions> {
  const { account } = campaign;
  const steps = parseFollowUps(campaign.followUps);
  const notSnoozed = { OR: [{ snoozedUntil: null }, { snoozedUntil: { lte: now } }] };
  const [byStage, followUpsSoon] = await Promise.all([
    db.prospect.groupBy({
      by: ["stage"],
      where: { campaignId: campaign.id, stage: { in: ["QUALIFIED", "INVITED", "CONNECTED"] }, ...notSnoozed },
      _count: true,
    }),
    steps.length
      ? db.prospect.count({
          where: {
            campaignId: campaign.id,
            stage: "MESSAGED",
            followUpsSent: { lt: steps.length },
            nextActionAt: { lte: new Date(now.getTime() + DAY) },
            ...notSnoozed,
          },
        })
      : Promise.resolve(0),
  ]);
  const count = (stage: ProspectStage) => byStage.find((r) => r.stage === stage)?._count ?? 0;
  return {
    toInvite: count("QUALIFIED"),
    pendingInvites: count("INVITED"),
    firstMessages: count("CONNECTED"),
    followUpsSoon,
    window: { label: sendingWindowLabel(account), open: isWithinSendingWindow(account, now) },
    invitesPausedUntil: account.invitesPausedUntil && account.invitesPausedUntil > now ? account.invitesPausedUntil : null,
    account: {
      id: account.id,
      fullName: account.fullName,
      status: account.status,
      statusReason: account.statusReason,
      lastError: account.lastError,
      lastErrorAt: account.lastErrorAt,
    },
  };
}
