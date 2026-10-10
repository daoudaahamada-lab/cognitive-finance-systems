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

export async function onboardingStatus(workspaceId: string) {
  const [accounts, campaigns, active, workspace] = await Promise.all([
    db.linkedInAccount.count({ where: { workspaceId, status: { not: "DISCONNECTED" } } }),
    db.campaign.count({ where: { workspaceId } }),
    db.campaign.count({ where: { workspaceId, status: "ACTIVE" } }),
    db.workspace.findUniqueOrThrow({ where: { id: workspaceId } }),
  ]);
  return {
    accountConnected: accounts > 0,
    offerDescribed: workspace.offer.trim().length > 0 && workspace.bookingUrl.length > 0,
    campaignCreated: campaigns > 0,
    campaignLaunched: active > 0,
  };
}
