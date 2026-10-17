import type { Metadata } from "next";
import { ButtonLink } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState, PageHeader } from "@/components/ui/misc";
import { agentMode } from "@/server/agents";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { CampaignForm } from "../campaign-form";
import { DEFAULT_FIRST_MESSAGE, DEFAULT_FOLLOW_UPS, DEFAULT_INVITE_NOTE } from "@/server/domain/campaign-defaults";

export const metadata: Metadata = { title: "Nouvelle campagne" };

export default async function NewCampaignPage() {
  const { workspace } = await requireContext();
  const accounts = await db.linkedInAccount.findMany({
    where: { workspaceId: workspace.id, status: { not: "DISCONNECTED" } },
    select: { id: true, fullName: true, provider: true, accountType: true, status: true },
    orderBy: { createdAt: "asc" },
  });

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

  // Prefer an account that can launch right away.
  const account = accounts.find((a) => a.status === "ACTIVE") ?? accounts[0]!;
  // Buying signals only exist in the simulator: with a real LinkedIn account they would find no one.
  const real = account.provider !== "simulator";

  return (
    <>
      <PageHeader title="Nouvelle campagne" description="La campagne est créée en brouillon : vous la lancez quand tout est prêt." />
      <CampaignForm
        aiEnabled={agentMode() === "claude"}
        campaignId={null}
        accounts={accounts}
        workspace={{ offer: workspace.offer, persona: workspace.persona, bookingUrl: workspace.bookingUrl }}
        values={{
          name: "",
          accountId: account.id,
          sources: real ? ["SEARCH"] : ["SEARCH", "SIGNALS"],
          titles: [],
          keywords: [],
          industries: [],
          locations: [],
          companySizes: [],
          signals: real ? [] : ["NEW_ROLE", "HIRING", "FUNDRAISING"],
          postUrls: [],
          searchUrl: "",
          exclusions: [],
          aiPersonalization: true,
          minScore: 60,
          weeklyProspectTarget: 100,
          // Empty means "use the settings": a later change in Réglages then applies to this campaign too.
          offer: "",
          persona: "",
          inviteNote: DEFAULT_INVITE_NOTE,
          firstMessage: DEFAULT_FIRST_MESSAGE,
          followUps: DEFAULT_FOLLOW_UPS,
          setterMode: "APPROVAL",
          bookingUrl: "",
        }}
      />
    </>
  );
}
