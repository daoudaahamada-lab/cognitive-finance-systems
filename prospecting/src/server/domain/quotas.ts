import type { AccountType } from "@prisma/client";

/**
 * Safety caps. LinkedIn publishes no official numbers; these are the commonly
 * observed thresholds above which accounts get restricted. Users may lower
 * them per account but never raise them.
 */
export const WEEKLY_INVITE_CAP: Record<AccountType, number> = {
  FREE: 100,
  PREMIUM: 200,
  SALES_NAVIGATOR: 200,
  RECRUITER: 200,
};
export const DAILY_INVITE_CAP = 40;
export const DAILY_MESSAGE_CAP = 100;

export type AccountLimitInput = {
  accountType: AccountType;
  weeklyInviteLimit: number | null;
  dailyInviteLimit: number | null;
  dailyMessageLimit: number | null;
};

export type EffectiveLimits = {
  weeklyInvites: number;
  dailyInvites: number;
  dailyMessages: number;
};

function clampOverride(override: number | null, cap: number): number {
  if (override === null || !Number.isFinite(override)) return cap;
  return Math.max(0, Math.min(Math.floor(override), cap));
}

export function effectiveLimits(account: AccountLimitInput): EffectiveLimits {
  return {
    weeklyInvites: clampOverride(account.weeklyInviteLimit, WEEKLY_INVITE_CAP[account.accountType]),
    dailyInvites: clampOverride(account.dailyInviteLimit, DAILY_INVITE_CAP),
    dailyMessages: clampOverride(account.dailyMessageLimit, DAILY_MESSAGE_CAP),
  };
}

export type QuotaUsage = {
  invitesLast24h: number;
  invitesLast7d: number;
  messagesLast24h: number;
};

export type RemainingQuota = { invites: number; messages: number };

/** Quotas use rolling windows (last 24 h, last 7 days), like LinkedIn's own limits. */
export function remainingQuota(limits: EffectiveLimits, usage: QuotaUsage): RemainingQuota {
  const invites = Math.min(
    limits.dailyInvites - usage.invitesLast24h,
    limits.weeklyInvites - usage.invitesLast7d,
  );
  return {
    invites: Math.max(0, invites),
    messages: Math.max(0, limits.dailyMessages - usage.messagesLast24h),
  };
}
