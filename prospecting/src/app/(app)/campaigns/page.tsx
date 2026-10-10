import { Megaphone, Plus } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { LabeledBadge } from "@/components/ui/badge";
import { ButtonLink } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState, PageHeader } from "@/components/ui/misc";
import { formatNumber, formatPercent } from "@/lib/format";
import { CAMPAIGN_STATUS, SETTER_MODES } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { listCampaigns } from "@/server/services/campaigns";

export const metadata: Metadata = { title: "Campagnes" };

export default async function CampaignsPage() {
  const { workspace } = await requireContext();
  const campaigns = await listCampaigns(workspace.id);

  return (
    <>
      <PageHeader
        title="Campagnes"
        description="Une campagne = un ciblage, une séquence de messages et un mode de setter, sur un compte LinkedIn."
        actions={<ButtonLink href="/campaigns/new"><Plus className="size-4" /> Nouvelle campagne</ButtonLink>}
      />
      <Card>
        {campaigns.length === 0 ? (
          <EmptyState
            icon={<Megaphone className="size-5" />}
            title="Aucune campagne"
            description="Créez votre première campagne : le moteur trouvera les prospects, les invitera et lancera les conversations."
            action={<ButtonLink href="/campaigns/new">Créer une campagne</ButtonLink>}
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Campagne</th>
                  <th>Statut</th>
                  <th className="text-right">Prospects</th>
                  <th className="text-right">Invités</th>
                  <th className="text-right">Acceptation</th>
                  <th className="text-right">Réponse</th>
                  <th className="text-right">RDV</th>
                  <th>Setter</th>
                </tr>
              </thead>
              <tbody>
                {campaigns.map((c) => (
                  <tr key={c.id}>
                    <td>
                      <Link href={`/campaigns/${c.id}`} className="font-medium hover:underline">
                        {c.name}
                      </Link>
                      <p className="text-xs text-muted">{c.account.fullName}</p>
                    </td>
                    <td><LabeledBadge map={CAMPAIGN_STATUS} value={c.status} /></td>
                    <td className="text-right tabular-nums">{formatNumber(c.funnel.found)}</td>
                    <td className="text-right tabular-nums">{formatNumber(c.funnel.invited)}</td>
                    <td className="text-right tabular-nums">{formatPercent(c.funnel.invited ? c.funnel.connected / c.funnel.invited : null)}</td>
                    <td className="text-right tabular-nums">{formatPercent(c.funnel.connected ? c.funnel.replied / c.funnel.connected : null)}</td>
                    <td className="text-right font-semibold tabular-nums">{c.funnel.meetings}</td>
                    <td className="text-sm text-muted">{SETTER_MODES[c.setterMode]?.label}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </>
  );
}
