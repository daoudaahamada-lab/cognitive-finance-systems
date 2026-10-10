import type { LinkedInAccount } from "@prisma/client";
import type { Db } from "@/server/db";
import { effectiveLimits, remainingQuota, type QuotaUsage } from "@/server/domain/quotas";
import { DAY, WEEK } from "@/server/domain/time";

export const MESSAGE_ACTIVITY_TYPES = ["MESSAGE_SENT", "FOLLOW_UP_SENT", "AI_REPLY_SENT", "HUMAN_REPLY_SENT"] as const;

/** Real-time rolling windows: quotas are never accelerated by TIME_SCALE. */
export async function quotaUsage(db: Db, accountId: string, now: Date): Promise<QuotaUsage> {
  const dayAgo = new Date(now.getTime() - DAY);
  const weekAgo = new Date(now.getTime() - WEEK);
  const [invitesLast24h, invitesLast7d, messagesLast24h] = await Promise.all([
    db.activity.count({ where: { accountId, type: "INVITE_SENT", createdAt: { gt: dayAgo, lte: now } } }),
    db.activity.count({ where: { accountId, type: "INVITE_SENT", createdAt: { gt: weekAgo, lte: now } } }),
    db.activity.count({ where: { accountId, type: { in: [...MESSAGE_ACTIVITY_TYPES] }, createdAt: { gt: dayAgo, lte: now } } }),
  ]);
  return { invitesLast24h, invitesLast7d, messagesLast24h };
}

export async function accountQuota(db: Db, account: LinkedInAccount, now: Date) {
  const limits = effectiveLimits(account);
  const usage = await quotaUsage(db, account.id, now);
  return { limits, usage, remaining: remainingQuota(limits, usage) };
}
