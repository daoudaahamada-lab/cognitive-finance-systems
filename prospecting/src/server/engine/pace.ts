import type { LinkedInAccount } from "@prisma/client";
import type { Db } from "@/server/db";
import type { EffectiveLimits } from "@/server/domain/quotas";
import { sendingWindowMinutes } from "@/server/domain/schedule";
import { MINUTE, timeScale } from "@/server/domain/time";

/** Anything but the simulator drives a real LinkedIn account. */
export function isRealAccount(account: { provider: string }): boolean {
  return account.provider !== "simulator";
}

/** TIME_SCALE only speeds up the simulator's world: a real account always waits in real time. */
export function waitScale(account: { provider: string }): number {
  return isRealAccount(account) ? 1 : timeScale();
}

/** Minimum gap between two actions so that a daily cap is spread over the whole sending window. */
export function actionSpacing(windowMinutes: number, dailyCap: number): number {
  return dailyCap > 0 ? Math.floor((windowMinutes * MINUTE) / dailyCap) : Infinity;
}

/**
 * How many invitations and sequence messages this tick may send on top of the quotas.
 * A real account sends one at a time, spread over its sending window (40 invitations
 * over 9 h: one every 13 minutes or so) instead of in bursts. The simulator is not paced.
 */
export async function paceBudget(
  db: Db,
  account: LinkedInAccount,
  limits: EffectiveLimits,
  now: Date,
): Promise<{ invites: number; messages: number }> {
  if (!isRealAccount(account)) return { invites: Infinity, messages: Infinity };
  const window = sendingWindowMinutes(account);
  const latest = (types: ("INVITE_SENT" | "MESSAGE_SENT" | "FOLLOW_UP_SENT")[]) =>
    db.activity.findFirst({
      where: { accountId: account.id, type: { in: types }, createdAt: { lte: now } },
      orderBy: { createdAt: "desc" },
      select: { createdAt: true },
    });
  const [lastInvite, lastMessage] = await Promise.all([latest(["INVITE_SENT"]), latest(["MESSAGE_SENT", "FOLLOW_UP_SENT"])]);
  const ready = (last: { createdAt: Date } | null, dailyCap: number) =>
    !last || now.getTime() - last.createdAt.getTime() >= actionSpacing(window, dailyCap) ? 1 : 0;
  return { invites: ready(lastInvite, limits.dailyInvites), messages: ready(lastMessage, limits.dailyMessages) };
}
