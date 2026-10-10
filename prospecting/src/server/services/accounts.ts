import type { AccountType } from "@prisma/client";
import { randomUUID } from "node:crypto";
import { z } from "zod";
import { db } from "@/server/db";
import { DAILY_INVITE_CAP, DAILY_MESSAGE_CAP, WEEKLY_INVITE_CAP } from "@/server/domain/quotas";
import { isValidTimezone, parseHourMinute } from "@/server/domain/schedule";
import { accountQuota } from "@/server/engine/quota";
import { PROVIDERS, getProvider } from "@/server/linkedin";
import { ProviderActionError, ProviderAuthError, ProviderLimitError } from "@/server/linkedin/types";
import { UserError } from "./errors";

export async function listAccounts(workspaceId: string, now = new Date()) {
  const accounts = await db.linkedInAccount.findMany({
    where: { workspaceId, status: { not: "DISCONNECTED" } },
    orderBy: { createdAt: "asc" },
    include: { _count: { select: { campaigns: { where: { status: "ACTIVE" } } } } },
  });
  return Promise.all(accounts.map(async (a) => ({ ...a, quota: await accountQuota(db, a, now) })));
}

export const connectAccountSchema = z
  .object({
    provider: z.enum(PROVIDERS).default("browser"),
    fullName: z.string().trim().max(100).default(""),
    headline: z.string().trim().max(200).default(""),
    accountType: z.enum(["FREE", "PREMIUM", "SALES_NAVIGATOR", "RECRUITER"]),
    sessionCookie: z.string().trim().max(2000).default(""),
  })
  .refine((v) => v.sessionCookie === "" || v.sessionCookie.length > 20, { message: "Ce cookie li_at semble incomplet", path: ["sessionCookie"] })
  .refine((v) => (v.provider === "browser" && v.sessionCookie) || v.fullName.length >= 2, { message: "Nom requis", path: ["fullName"] });

/** Turns provider failures into messages that tell the user what to do. */
async function linkedin<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (error instanceof ProviderAuthError) throw new UserError(`LinkedIn a refusé la session : ${error.message}`);
    if (error instanceof ProviderActionError || error instanceof ProviderLimitError) throw new UserError(`LinkedIn : ${error.message}`);
    throw error;
  }
}

export async function connectAccount(workspaceId: string, input: z.infer<typeof connectAccountSchema>) {
  const workspace = await db.workspace.findUniqueOrThrow({ where: { id: workspaceId } });
  const providerName = input.provider;
  if (providerName === "browser" && !input.sessionCookie) {
    // No cookie: the account waits until someone logs in by hand (npm run linkedin:login).
    const account = await db.linkedInAccount.create({
      data: {
        workspaceId, provider: "browser", externalId: `br-${randomUUID()}`, fullName: input.fullName, headline: input.headline,
        accountType: input.accountType, timezone: workspace.timezone, status: "PAUSED", statusReason: "Session LinkedIn à ouvrir",
      },
    });
    return db.linkedInAccount.update({
      where: { id: account.id },
      data: { statusReason: `Session LinkedIn à ouvrir : lancez « npm run linkedin:login -- --account ${account.id} » sur votre machine, ou collez un cookie li_at.` },
    });
  }
  const connected = await linkedin(() => getProvider(db, providerName).connectAccount(input));
  return db.linkedInAccount.create({
    data: {
      workspaceId,
      provider: providerName,
      externalId: connected.externalId,
      fullName: connected.fullName,
      headline: connected.headline,
      accountType: connected.accountType as AccountType,
      timezone: workspace.timezone,
    },
  });
}

function safeParseTime(value: string): number | null {
  try {
    return parseHourMinute(value);
  } catch {
    return null;
  }
}

const optionalLimit = (cap: number) =>
  z.preprocess((v) => (v === "" || v === null || v === undefined ? null : Number(v)), z.number().int().min(0).max(cap).nullable());

export const accountSettingsSchema = z
  .object({
    accountType: z.enum(["FREE", "PREMIUM", "SALES_NAVIGATOR", "RECRUITER"]),
    timezone: z.string().refine(isValidTimezone, "Fuseau horaire inconnu"),
    sendingDays: z.array(z.coerce.number().int().min(1).max(7)).min(1, "Choisissez au moins un jour"),
    sendingStart: z.string().regex(/^\d{2}:\d{2}$/),
    sendingEnd: z.string().regex(/^\d{2}:\d{2}$/),
    weeklyInviteLimit: optionalLimit(200),
    dailyInviteLimit: optionalLimit(DAILY_INVITE_CAP),
    dailyMessageLimit: optionalLimit(DAILY_MESSAGE_CAP),
  })
  .refine((v) => safeParseTime(v.sendingStart) !== null && safeParseTime(v.sendingEnd) !== null, {
    message: "Heure invalide",
    path: ["sendingEnd"],
  })
  .refine((v) => v.weeklyInviteLimit === null || v.weeklyInviteLimit <= WEEKLY_INVITE_CAP[v.accountType], {
    message: "Au-dessus du plafond de sécurité pour ce type de compte",
    path: ["weeklyInviteLimit"],
  });

export async function updateAccountSettings(workspaceId: string, accountId: string, input: z.infer<typeof accountSettingsSchema>) {
  const { count } = await db.linkedInAccount.updateMany({ where: { id: accountId, workspaceId }, data: input });
  if (count === 0) throw new UserError("Compte introuvable.");
}

export const sessionSchema = z.object({ sessionCookie: z.string().trim().min(20, "Collez le cookie li_at de votre session LinkedIn").max(2000) });

/** New cookie for an existing account (after an expired session or a security check). */
export async function updateAccountSession(workspaceId: string, accountId: string, sessionCookie: string) {
  const account = await db.linkedInAccount.findFirst({ where: { id: accountId, workspaceId } });
  if (!account) throw new UserError("Compte introuvable.");
  const provider = getProvider(db, account.provider);
  if (!provider.updateSession) throw new UserError("Ce type de compte n'utilise pas de session LinkedIn.");
  const me = await linkedin(() => provider.updateSession!({ externalId: account.externalId }, sessionCookie));
  await db.linkedInAccount.update({
    where: { id: accountId },
    data: { fullName: me.fullName || account.fullName, headline: me.headline || account.headline, status: "ACTIVE", statusReason: null },
  });
}

export async function setAccountStatus(workspaceId: string, accountId: string, status: "ACTIVE" | "PAUSED" | "DISCONNECTED") {
  const account = await db.linkedInAccount.findFirst({ where: { id: accountId, workspaceId } });
  if (!account) throw new UserError("Compte introuvable.");
  await db.linkedInAccount.update({ where: { id: accountId }, data: { status, ...(status === "ACTIVE" ? { statusReason: null } : {}) } });
  if (status === "DISCONNECTED") {
    await db.campaign.updateMany({ where: { accountId, status: "ACTIVE" }, data: { status: "PAUSED" } });
  }
}
