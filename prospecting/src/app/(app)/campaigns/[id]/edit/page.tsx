import { TriangleAlert } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { PageHeader } from "@/components/ui/misc";
import { agentMode } from "@/server/agents";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { parseFollowUps } from "@/server/domain/followups";
import { getCampaign } from "@/server/services/campaigns";
import { CampaignForm } from "../../campaign-form";

export const metadata: Metadata = { title: "Modifier la campagne" };

export default async function EditCampaignPage({ params }: { params: Promise<{ id: string }> }) {
  const { workspace } = await requireContext();
  const { id } = await params;
  const campaign = await getCampaign(workspace.id, id);
  if (!campaign) notFound();
  const accounts = await db.linkedInAccount.findMany({
    where: { workspaceId: workspace.id, status: { not: "DISCONNECTED" } },
    select: { id: true, fullName: true, provider: true, accountType: true, status: true },
    orderBy: { createdAt: "asc" },
  });
  // A disconnected account is not offered in the list: ask for another one instead of silently picking the first.
  const disconnected = campaign.account.status === "DISCONNECTED";

  return (
    <>
      <PageHeader
        title={`Modifier « ${campaign.name} »`}
        description="Les modifications s'appliquent aux prochains envois ; les messages déjà partis ne changent pas."
      />
      {disconnected ? (
        <p className="mb-6 flex items-start gap-2.5 rounded-card border border-warning-line bg-warning-soft px-4 py-3 text-sm text-ink-2">
          <TriangleAlert className="mt-0.5 size-4 shrink-0 text-warning" aria-hidden />
          <span>
            <strong className="font-semibold text-ink">Le compte de cette campagne a été déconnecté : choisissez un autre compte</strong>
            {accounts.length === 0 ? (
              <>
                {" "}
                après en avoir connecté un dans{" "}
                <Link href="/accounts" className="font-medium text-brand-700 underline underline-offset-2 hover:text-brand-800">
                  Comptes LinkedIn
                </Link>
              </>
            ) : null}
            .
          </span>
        </p>
      ) : null}
      <CampaignForm
        aiEnabled={agentMode() === "claude"}
        campaignId={campaign.id}
        accounts={accounts}
        workspace={{ offer: workspace.offer, persona: workspace.persona, bookingUrl: workspace.bookingUrl }}
        values={{
          name: campaign.name,
          accountId: disconnected ? "" : campaign.accountId,
          sources: campaign.sources,
          titles: campaign.titles,
          keywords: campaign.keywords,
          industries: campaign.industries,
          locations: campaign.locations,
          companySizes: campaign.companySizes,
          signals: campaign.signals,
          postUrls: campaign.postUrls,
          searchUrl: campaign.searchUrl,
          exclusions: campaign.exclusions,
          aiPersonalization: campaign.aiPersonalization,
          minScore: campaign.minScore,
          weeklyProspectTarget: campaign.weeklyProspectTarget,
          offer: campaign.offer,
          persona: campaign.persona,
          inviteNote: campaign.inviteNote ?? "",
          firstMessage: campaign.firstMessage,
          followUps: parseFollowUps(campaign.followUps),
          setterMode: campaign.setterMode,
          bookingUrl: campaign.bookingUrl,
        }}
      />
    </>
  );
}
