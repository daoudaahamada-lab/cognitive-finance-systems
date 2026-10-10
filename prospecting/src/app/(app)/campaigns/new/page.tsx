import type { Metadata } from "next";
import { ButtonLink } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState, PageHeader } from "@/components/ui/misc";
import { agentMode } from "@/server/agents";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { planLimits } from "@/server/domain/plans";
import { CampaignForm } from "../campaign-form";
import { DEFAULT_FIRST_MESSAGE, DEFAULT_FOLLOW_UPS, DEFAULT_INVITE_NOTE } from "../defaults";

export const metadata: Metadata = { title: "Nouvelle campagne" };

export default async function NewCampaignPage() {
  const { workspace } = await requireContext();
  const accounts = await db.linkedInAccount.findMany({ where: { workspaceId: workspace.id, status: { not: "DISCONNECTED" } }, select: { id: true, fullName: true } });
  const limits = planLimits(workspace.plan);

  if (accounts.length === 0) {
    return (
      <>
        <PageHeader title="Nouvelle campagne" />
        <Card>
          <EmptyState title="Connectez d'abord un compte LinkedIn" description="Une campagne s'exécute depuis un compte LinkedIn." action={<ButtonLink href="/accounts">Connecter un compte</ButtonLink>} />
        </Card>
      </>
    );
  }

  return (
    <>
      <PageHeader title="Nouvelle campagne" description="La campagne est créée en brouillon : vous la lancez quand tout est prêt." />
      <CampaignForm
        aiEnabled={agentMode() === "claude"}
        campaignId={null}
        accounts={accounts}
        plan={{ label: limits.label, setter: limits.setter, maxFollowUps: limits.maxFollowUps }}
        senderFirstName={accounts[0]!.fullName.split(" ")[0] ?? ""}
        values={{
          name: "",
          accountId: accounts[0]!.id,
          sources: ["SEARCH", "SIGNALS"],
          titles: [],
          keywords: [],
          industries: [],
          locations: [],
          companySizes: [],
          signals: ["NEW_ROLE", "HIRING", "FUNDRAISING"],
          postUrls: [],
          exclusions: [],
          aiPersonalization: true,
          minScore: 60,
          weeklyProspectTarget: 100,
          offer: workspace.offer,
          persona: workspace.persona,
          inviteNote: DEFAULT_INVITE_NOTE,
          firstMessage: DEFAULT_FIRST_MESSAGE,
          followUps: DEFAULT_FOLLOW_UPS.slice(0, limits.maxFollowUps),
          setterMode: limits.setter ? "APPROVAL" : "OFF",
          bookingUrl: workspace.bookingUrl,
        }}
      />
    </>
  );
}
