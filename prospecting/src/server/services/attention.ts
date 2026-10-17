import type { ProspectSource } from "@prisma/client";
import { formatAgo, plural } from "@/lib/format";
import { db } from "@/server/db";
import { DAY } from "@/server/domain/time";
import { PROSPECT_ERROR_CODES, type ActionErrorCode } from "@/server/linkedin/types";
import { engineStatus } from "./engine-status";
import { inboxCounts } from "./inbox";

export type AttentionSeverity = "high" | "medium" | "low";

export type AttentionKind =
  | "account_paused"
  | "account_disconnected"
  | "account_error"
  | "engine_down"
  | "action_failed"
  | "campaign_exhausted"
  | "meetings_to_confirm"
  | "inbox_todo"
  | "drafts";

/** One thing that waits for the user, most urgent first. `detail` says why or what to do. */
export type AttentionItem = {
  kind: AttentionKind;
  severity: AttentionSeverity;
  label: string;
  detail?: string;
  href: string;
  count: number;
};

/** Account errors and failed actions older than this no longer need the user. */
export const ATTENTION_WINDOW = DAY;

const SEVERITY_RANK: Record<AttentionSeverity, number> = { high: 0, medium: 1, low: 2 };

/** Same rule as the engine (engine/sourcing.ts): sources it can page through by itself. */
const AUTOMATIC_SOURCES: ProspectSource[] = ["SEARCH", "SIGNALS", "POST_ENGAGERS", "PROFILE_VISITORS"];

/**
 * An account's statusReason as it reads away from the account card. The "session to open" reason
 * (services/accounts.ts) points at a form "ci-dessous" and a terminal command that only make sense on /accounts.
 */
export function reasonOutsideAccounts(reason: string): string {
  return isSessionToOpen(reason) ? "Session LinkedIn à ouvrir : connectez-la depuis la fiche du compte." : reason;
}

function isSessionToOpen(reason: string): boolean {
  return reason.startsWith("Session LinkedIn à ouvrir");
}

/** French reason and what Vela does about it, per ACTION_FAILED code (data.code). */
const FAILURE_REASONS: Record<ActionErrorCode | "LIMIT", { reason: string; detail: string }> = {
  LIMIT: { reason: "limite d'invitations signalée par LinkedIn", detail: "Vela suspend les invitations de ce compte pendant 24 h." },
  WORKER_UNAVAILABLE: { reason: "le navigateur de Vela ne répond pas", detail: "Vérifiez que Vela est lancé sur votre ordinateur. Il réessaiera au prochain passage." },
  UNEXPECTED_PAGE: { reason: "page LinkedIn inattendue", detail: "Vela réessaiera au prochain passage. Si cela se répète, vérifiez la connexion du compte." },
  CONNECT_UNAVAILABLE: { reason: "invitation impossible sur ces profils", detail: "Ces prospects ont été écartés ; Vela passe aux suivants." },
  MESSAGE_UNAVAILABLE: { reason: "message impossible", detail: "Vela réessaie plus tard, puis abandonne après plusieurs échecs." },
  PROFILE_NOT_FOUND: { reason: "profil introuvable", detail: "Vela passe aux prospects suivants." },
  ALREADY_CONNECTED: { reason: "déjà en relation", detail: "Vela passe directement au premier message." },
  ALREADY_PENDING: { reason: "invitation déjà en attente", detail: "Vela attend la réponse à l'invitation existante." },
};

/**
 * Everything on the workspace that needs the user now, including failures the engine would otherwise keep quiet:
 * paused accounts, sync errors, a stopped engine, failed LinkedIn actions, campaigns with nobody left to invite,
 * meetings whose outcome is unknown, and the inbox. Items with nothing to report are left out.
 */
export async function attentionItems(workspaceId: string, now = new Date()): Promise<AttentionItem[]> {
  const since = new Date(now.getTime() - ATTENTION_WINDOW);
  const [accounts, status, failures, campaigns, pastMeetings, inbox] = await Promise.all([
    db.linkedInAccount.findMany({
      where: { workspaceId },
      orderBy: { createdAt: "asc" },
      select: {
        id: true, fullName: true, status: true, statusReason: true, lastError: true, lastErrorAt: true,
        _count: { select: { campaigns: { where: { status: { not: "ARCHIVED" } } } } },
        // Where a disconnected account's row leads: its only campaign, else the campaign list.
        campaigns: { where: { status: { not: "ARCHIVED" } }, orderBy: { createdAt: "asc" }, select: { id: true }, take: 2 },
      },
    }),
    engineStatus(workspaceId, now),
    db.activity.findMany({
      where: { workspaceId, type: "ACTION_FAILED", createdAt: { gte: since } },
      select: { data: true, prospectId: true, campaignId: true },
      orderBy: { createdAt: "desc" },
      take: 500,
    }),
    db.campaign.findMany({
      where: { workspaceId, status: "ACTIVE" },
      orderBy: { createdAt: "asc" },
      select: {
        id: true, name: true, sources: true, postUrls: true, sourcingState: true,
        _count: { select: { prospects: { where: { stage: { in: ["NEW", "QUALIFIED"] } } } } },
        prospects: { where: { source: "IMPORT" }, select: { id: true }, take: 1 },
      },
    }),
    db.meeting.count({ where: { workspaceId, status: "SCHEDULED", startsAt: { lt: now } } }),
    inboxCounts(workspaceId),
  ]);

  const items: AttentionItem[] = [];

  for (const a of accounts) {
    if (a.status === "PAUSED" && a.statusReason) {
      items.push({
        kind: "account_paused", severity: "high", label: `${a.fullName} est en pause`, detail: reasonOutsideAccounts(a.statusReason),
        href: `/accounts#${a.id}`, count: 1,
      });
    }
  }
  for (const a of accounts) {
    if (a.status === "ACTIVE" && a.lastError && a.lastErrorAt && a.lastErrorAt >= since) {
      items.push({
        kind: "account_error", severity: "high", label: `${a.fullName} : la dernière synchronisation a échoué`,
        detail: `${a.lastError} (${formatAgo(a.lastErrorAt, now)})`, href: `/accounts#${a.id}`, count: 1,
      });
    }
  }
  // Without an active account the engine has nothing to do: the paused-account rows already say why.
  if (status.level === "down" && accounts.some((a) => a.status === "ACTIVE")) {
    items.push({
      kind: "engine_down", severity: "high", label: "Le moteur est arrêté",
      detail: `${status.lastSyncAt ? `Dernière synchronisation ${formatAgo(status.lastSyncAt, now)}.` : "Aucune synchronisation pour l'instant."} Vérifiez que Vela est lancé sur votre ordinateur.`,
      href: "/accounts", count: 1,
    });
  }

  const failed = failureItems(failures);
  items.push(...failed.filter((f) => f.severity !== "low"));

  if (inbox.todo > 0) {
    items.push({ kind: "inbox_todo", severity: "medium", label: "Conversations à traiter au total", href: "/inbox?tab=todo", count: inbox.todo });
  }
  if (inbox.drafts > 0) {
    items.push({ kind: "drafts", severity: "medium", label: "dont réponses du setter à valider", href: "/inbox?tab=drafts", count: inbox.drafts });
  }

  for (const c of campaigns) {
    if (c._count.prospects > 0) continue;
    const auto = automaticSources(c);
    if (auto.length === 0) {
      // Nothing for Vela to page through: only a new list brings prospects, wider targeting would change nothing.
      items.push({
        kind: "campaign_exhausted", severity: "medium",
        label: c.prospects.length > 0
          ? `Campagne ${c.name} : tous les prospects importés ont été contactés, importez une nouvelle liste`
          : `Campagne ${c.name} : aucun prospect à contacter, importez une liste`,
        href: `/campaigns/${c.id}#import`, count: 1,
      });
    } else if (sourcingExhausted(c.sourcingState, auto)) {
      items.push({
        kind: "campaign_exhausted", severity: "medium", label: `Campagne ${c.name} : plus aucun prospect à inviter, élargissez le ciblage`,
        href: `/campaigns/${c.id}`, count: 1,
      });
    }
  }

  // A disconnected account only matters while campaigns still depend on it (archiving them clears the row).
  for (const a of accounts) {
    if (a.status === "DISCONNECTED" && a.statusReason && a._count.campaigns > 0) {
      // /accounts no longer lists a disconnected account: the campaign page offers "Choisir un autre compte".
      const only = a.campaigns.length === 1 ? a.campaigns[0] : undefined;
      const several = a._count.campaigns > 1;
      const dependents = `${plural(a._count.campaigns, "campagne en dépend", "campagnes en dépendent")} : choisissez un autre compte ou archivez-${several ? "les" : "la"}.`;
      // A session that was never opened no longer matters once the account is disconnected (and its card is gone).
      const reason = isSessionToOpen(a.statusReason) ? null : a.statusReason.replace(/[.\s]+$/, "");
      items.push({
        kind: "account_disconnected", severity: "medium", label: `${a.fullName} est déconnecté`,
        detail: reason ? `${reason}. ${dependents}` : dependents,
        href: only ? `/campaigns/${only.id}` : "/campaigns", count: 1,
      });
    }
  }

  if (pastMeetings > 0) {
    items.push({
      kind: "meetings_to_confirm", severity: "low", label: plural(pastMeetings, "rendez-vous à confirmer", "rendez-vous à confirmer"),
      detail: pastMeetings > 1 ? "Indiquez s'ils ont eu lieu." : "Indiquez s'il a eu lieu.", href: "/meetings", count: pastMeetings,
    });
  }

  // Prospect-specific failures are already handled by the engine: they come last, for information.
  items.push(...failed.filter((f) => f.severity === "low"));

  // Stable sort: within a severity, the order above stands (the drafts row stays right under the inbox row).
  return items.sort((a, b) => SEVERITY_RANK[a.severity] - SEVERITY_RANK[b.severity]);
}

/** The campaign's sources the engine can page through by itself (engagers need at least one post). */
function automaticSources(campaign: { sources: ProspectSource[]; postUrls: string[] }): ProspectSource[] {
  return campaign.sources.filter((s) => AUTOMATIC_SOURCES.includes(s) && (s !== "POST_ENGAGERS" || campaign.postUrls.length > 0));
}

/** True when each of these automatic sources has reached its end. */
function sourcingExhausted(sourcingState: unknown, sources: ProspectSource[]): boolean {
  const state = (sourcingState ?? {}) as Partial<Record<ProspectSource, unknown>>;
  return sources.every((s) => state[s] === "done");
}

type Failure = { data: unknown; prospectId: string | null; campaignId: string | null };

/** ACTION_FAILED activities grouped by code: session or machine problems first, then prospect-specific ones. */
function failureItems(failures: Failure[]): AttentionItem[] {
  const groups = new Map<string, Failure[]>();
  for (const f of failures) {
    const data = f.data && typeof f.data === "object" ? (f.data as { code?: unknown }) : {};
    const code = typeof data.code === "string" ? data.code : "UNKNOWN";
    groups.set(code, [...(groups.get(code) ?? []), f]);
  }
  const items: AttentionItem[] = [];
  for (const [code, group] of groups) {
    const known = FAILURE_REASONS[code as keyof typeof FAILURE_REASONS];
    const prospectSpecific = (PROSPECT_ERROR_CODES as string[]).includes(code);
    const prospects = new Set(group.map((f) => f.prospectId).filter(Boolean));
    const campaigns = new Set(group.map((f) => f.campaignId).filter(Boolean));
    const href = !prospectSpecific
      ? "/accounts"
      : prospects.size === 1
        ? `/prospects/${[...prospects][0]}`
        : campaigns.size === 1
          ? `/prospects?campaignId=${[...campaigns][0]}`
          : "/prospects";
    items.push({
      kind: "action_failed",
      severity: prospectSpecific ? "low" : "medium",
      label: `${plural(group.length, "action LinkedIn impossible", "actions LinkedIn impossibles")} en 24 h : ${known?.reason ?? code}`,
      detail: known?.detail,
      href,
      count: group.length,
    });
  }
  return items.sort((a, b) => SEVERITY_RANK[a.severity] - SEVERITY_RANK[b.severity] || b.count - a.count);
}
