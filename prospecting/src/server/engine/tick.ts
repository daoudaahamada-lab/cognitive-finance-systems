import type { LinkedInAccount } from "@prisma/client";
import { MINUTE } from "@/server/domain/time";
import type { EngineDeps } from "./deps";
import { syncEvents } from "./events";
import { runOutreach, type OutreachResult } from "./outreach";
import { scoreNewProspects, sourceProspects } from "./sourcing";

/** Covers a tick that waits on several model calls; released as soon as the tick ends. */
export const LEASE_MS = 15 * MINUTE;

export type AccountTickResult = {
  accountId: string;
  events: number;
  sourced: number;
  scored: number;
  outreach: OutreachResult | null;
  error?: string;
};

/**
 * One pass of the prospecting machine over every active account:
 * sync LinkedIn events, source and score prospects, then send what is due.
 */
export async function runTick(deps: EngineDeps, options: { workspaceId?: string } = {}): Promise<AccountTickResult[]> {
  const accounts = await deps.db.linkedInAccount.findMany({
    where: { status: "ACTIVE", ...(options.workspaceId ? { workspaceId: options.workspaceId } : {}) },
    orderBy: { lastSyncedAt: { sort: "asc", nulls: "first" } },
  });
  const results: AccountTickResult[] = [];
  for (const account of accounts) {
    if (!(await acquireLease(deps, account))) continue;
    try {
      results.push(await tickAccount(deps, account));
    } catch (error) {
      results.push({
        accountId: account.id, events: 0, sourced: 0, scored: 0, outreach: null,
        error: error instanceof Error ? error.message : String(error),
      });
    } finally {
      await deps.db.linkedInAccount.update({
        where: { id: account.id },
        data: { lockedUntil: null, lastSyncedAt: deps.now },
      });
    }
  }
  return results;
}

async function tickAccount(deps: EngineDeps, account: LinkedInAccount): Promise<AccountTickResult> {
  const events = await syncEvents(deps, account);

  const campaigns = await deps.db.campaign.findMany({
    where: { accountId: account.id, status: "ACTIVE" },
    include: { account: true, workspace: true },
  });
  let sourced = 0;
  let scored = 0;
  for (const campaign of campaigns) {
    sourced += await sourceProspects(deps, campaign);
    scored += await scoreNewProspects(deps, campaign);
  }

  const outreach = await runOutreach(deps, account);
  return { accountId: account.id, events, sourced, scored, outreach };
}

/** Lease so that the worker and a manual "run now" never work on the same account at once. */
async function acquireLease(deps: EngineDeps, account: LinkedInAccount): Promise<boolean> {
  const { count } = await deps.db.linkedInAccount.updateMany({
    where: { id: account.id, OR: [{ lockedUntil: null }, { lockedUntil: { lt: deps.now } }] },
    data: { lockedUntil: new Date(deps.now.getTime() + LEASE_MS) },
  });
  return count === 1;
}
