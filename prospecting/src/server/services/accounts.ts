import type { AccountType } from "@prisma/client";
import { z } from "zod";
import { db } from "@/server/db";
import { planLimits } from "@/server/domain/plans";
import { DAILY_INVITE_CAP, DAILY_MESSAGE_CAP, WEEKLY_INVITE_CAP } from "@/server/domain/quotas";
import { isValidTimezone, parseHourMinute } from "@/server/domain/schedule";
import { accountQuota } from "@/server/engine/quota";
import { getProvider } from "@/server/linkedin";
import { UserError } from "./errors";

export async function listAccounts(workspaceId: string, now = new Date()) {
  const accounts = await db.linkedInAccount.findMany({
    where: { workspaceId, status: { not: "DISCONNECTED" } },
    orderBy: { createdAt: "asc" },
    include: { _count: { select: { campaigns: { where: { status: "ACTIVE" } } } } },
  });
  return Promise.all(accounts.map(async (a) => ({ ...a, quota: await accountQuota(db, a, now) })));
}

export const connectAccountSchema = z.object({
  fullName: z.string().trim().min(2, "Nom requis").max(100),
  headline: z.string().trim().max(200).default(""),
  accountType: z.enum(["FREE", "PREMIUM", "SALES_NAVIGATOR", "RECRUITER"]),
});

export async function connectAccount(workspaceId: string, input: z.infer<typeof connectAccountSchema>) {
  const workspace = await db.workspace.findUniqueOrThrow({ where: { id: workspaceId } });
  const limits = planLimits(workspace.plan);
  const active = await db.linkedInAccount.count({ where: { workspaceId, status: { not: "DISCONNECTED" } } });
  if (active >= limits.maxAccounts) {
    throw new UserError(
      limits.maxAccounts === 1
        ? `Le plan ${limits.label} inclut un seul compte LinkedIn. Passez au plan Agency pour en connecter plusieurs.`
        : `Le plan ${limits.label} est limité à ${limits.maxAccounts} comptes LinkedIn.`,
    );
  }
  const providerName = process.env.LINKEDIN_PROVIDER ?? "simulator";
  const connected = await getProvider(db, providerName).connectAccount(input);
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

export async function setAccountStatus(workspaceId: string, accountId: string, status: "ACTIVE" | "PAUSED" | "DISCONNECTED") {
  const account = await db.linkedInAccount.findFirst({ where: { id: accountId, workspaceId } });
  if (!account) throw new UserError("Compte introuvable.");
  await db.linkedInAccount.update({ where: { id: accountId }, data: { status } });
  if (status === "DISCONNECTED") {
    await db.campaign.updateMany({ where: { accountId, status: "ACTIVE" }, data: { status: "PAUSED" } });
  }
}
