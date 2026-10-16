import { agentMode, type AgentMode } from "@/server/agents";
import { db } from "@/server/db";
import { HOUR, MINUTE } from "@/server/domain/time";
import { LEASE_MS } from "@/server/engine/tick";

/** ok: synced in the last 10 minutes; late: within the hour; down: older, or no active account. */
export type EngineLevel = "ok" | "late" | "down";

export const ENGINE_LATE_AFTER = 10 * MINUTE;
export const ENGINE_DOWN_AFTER = HOUR;

export type EngineStatus = {
  /** Most recent pass over an ACTIVE account (null: never). */
  lastSyncAt: Date | null;
  level: EngineLevel;
  /** True while a pass started in the last 10 minutes still holds an account's lease. */
  syncing: boolean;
  /** Providers of the connected (not disconnected) accounts, e.g. ["simulator"]. */
  providers: string[];
  agentMode: AgentMode;
  pausedAccounts: { id: string; fullName: string; statusReason: string | null }[];
  erroredAccounts: { id: string; fullName: string; lastError: string; lastErrorAt: Date | null }[];
};

export async function engineStatus(workspaceId: string, now = new Date()): Promise<EngineStatus> {
  const accounts = await db.linkedInAccount.findMany({
    where: { workspaceId, status: { not: "DISCONNECTED" } },
    orderBy: { createdAt: "asc" },
    select: { id: true, fullName: true, provider: true, status: true, statusReason: true, lastSyncedAt: true, lockedUntil: true, lastError: true, lastErrorAt: true },
  });
  const active = accounts.filter((a) => a.status === "ACTIVE");
  // A worker killed mid-pass leaves its lease behind: only a recent one counts as a pass in progress.
  const syncing = active.some(
    (a) => a.lockedUntil !== null && a.lockedUntil > now && a.lockedUntil.getTime() - LEASE_MS > now.getTime() - ENGINE_LATE_AFTER,
  );
  const times = active.flatMap((a) => (a.lastSyncedAt ? [a.lastSyncedAt.getTime()] : []));
  const lastSyncAt = times.length ? new Date(Math.max(...times)) : null;

  let level: EngineLevel = "down";
  if (active.length > 0 && (syncing || lastSyncAt)) {
    const age = syncing ? 0 : now.getTime() - lastSyncAt!.getTime();
    level = age < ENGINE_LATE_AFTER ? "ok" : age < ENGINE_DOWN_AFTER ? "late" : "down";
  }

  return {
    lastSyncAt,
    level,
    syncing,
    providers: [...new Set(accounts.map((a) => a.provider))],
    agentMode: agentMode(),
    pausedAccounts: accounts.filter((a) => a.status === "PAUSED").map((a) => ({ id: a.id, fullName: a.fullName, statusReason: a.statusReason })),
    erroredAccounts: active.flatMap((a) => (a.lastError ? [{ id: a.id, fullName: a.fullName, lastError: a.lastError, lastErrorAt: a.lastErrorAt }] : [])),
  };
}

/** Only simulated LinkedIn accounts: the app is in test mode. */
export function isSimulatorOnly(status: Pick<EngineStatus, "providers">): boolean {
  return status.providers.length > 0 && status.providers.every((p) => p === "simulator");
}
