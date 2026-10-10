import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { PageHeader } from "@/components/ui/misc";
import { agentMode } from "@/server/agents";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { parseFollowUps } from "@/server/domain/followups";
import { planLimits } from "@/server/domain/plans";
import { getCampaign } from "@/server/services/campaigns";
import { CampaignForm } from "../../campaign-form";

export const metadata: Metadata = { title: "Modifier la campagne" };

export default async function EditCampaignPage({ params }: { params: Promise<{ id: string }> }) {
  const { workspace } = await requireContext();
  const { id } = await params;
  const campaign = await getCampaign(workspace.id, id);
  if (!campaign) notFound();
  const accounts = await db.linkedInAccount.findMany({ where: { workspaceId: workspace.id, status: { not: "DISCONNECTED" } }, select: { id: true, fullName: true } });
  const limits = planLimits(workspace.plan);

  return (
    <>
      <PageHeader title={`Modifier « ${campaign.name} »`} description="Les changements s'appliquent aux prochaines actions du moteur." />
      <CampaignForm
        aiEnabled={agentMode() === "claude"}
        campaignId={campaign.id}
        accounts={accounts}
        plan={{ label: limits.label, setter: limits.setter, maxFollowUps: limits.maxFollowUps }}
        senderFirstName={campaign.account.fullName.split(" ")[0] ?? ""}
        values={{ ...campaign, inviteNote: campaign.inviteNote ?? "", followUps: parseFollowUps(campaign.followUps) }}
      />
    </>
  );
}
