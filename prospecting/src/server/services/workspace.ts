import { z } from "zod";
import { db } from "@/server/db";
import { isValidTimezone } from "@/server/domain/schedule";

export const workspaceSettingsSchema = z.object({
  name: z.string().trim().min(1, "Nom requis").max(100),
  timezone: z.string().refine(isValidTimezone, "Fuseau horaire inconnu"),
  offer: z.string().transform((v) => v.replace(/\r\n?/g, "\n").trim()).pipe(z.string().max(3000)),
  persona: z.string().transform((v) => v.replace(/\r\n?/g, "\n").trim()).pipe(z.string().max(3000)),
  bookingUrl: z.union([z.url("Lien invalide"), z.literal("")]),
});

export async function updateWorkspace(workspaceId: string, input: z.infer<typeof workspaceSettingsSchema>) {
  await db.workspace.update({ where: { id: workspaceId }, data: input });
}

export type OnboardingStatus = Awaited<ReturnType<typeof onboardingStatus>>;

/**
 * First-run checklist, computed from what is really in place (a paused account does not count as ready).
 * `accountIssue` and `sessionIssue` explain a step that went backwards.
 */
export async function onboardingStatus(workspaceId: string) {
  const [accounts, campaigns, workspace] = await Promise.all([
    db.linkedInAccount.findMany({
      where: { workspaceId, status: { not: "DISCONNECTED" } },
      orderBy: { createdAt: "asc" },
      select: { id: true, provider: true, status: true, statusReason: true, lastDiagnosisOk: true },
    }),
    db.campaign.findMany({ where: { workspaceId, status: { not: "ARCHIVED" } }, orderBy: { updatedAt: "desc" }, select: { id: true, status: true } }),
    db.workspace.findUniqueOrThrow({ where: { id: workspaceId } }),
  ]);
  const accountReady = accounts.some((a) => a.status === "ACTIVE");
  const paused = accountReady ? undefined : accounts.find((a) => a.status === "PAUSED" && a.statusReason);
  const simulatorOnly = accounts.length > 0 && accounts.every((a) => a.provider === "simulator");
  const browser = accounts.filter((a) => a.provider === "browser");
  const sessionVerified = simulatorOnly || browser.some((a) => a.lastDiagnosisOk === true);
  const failedCheck = sessionVerified ? undefined : browser.find((a) => a.lastDiagnosisOk === false);
  // The campaign the "launch" step opens: the latest draft, else the latest paused one.
  const toLaunch = campaigns.find((c) => c.status === "DRAFT") ?? campaigns.find((c) => c.status === "PAUSED");

  return {
    /** At least one ACTIVE LinkedIn account. */
    accountReady,
    accountIssue: paused ? { accountId: paused.id, reason: paused.statusReason! } : null,
    /** Only simulated accounts: the "verify the connection" step does not apply. */
    simulatorOnly,
    /** A browser account passed "Vérifier la connexion", or the workspace only uses the simulator. */
    sessionVerified,
    sessionIssue: failedCheck ? { accountId: failedCheck.id, reason: "La dernière vérification de la connexion a échoué : relancez-la après avoir corrigé la session." } : null,
    offerDescribed: workspace.offer.trim().length > 0 && workspace.bookingUrl.length > 0,
    campaignCreated: campaigns.length > 0,
    campaignLaunched: campaigns.some((c) => c.status === "ACTIVE"),
    draftCampaignId: toLaunch?.id ?? null,
  };
}
