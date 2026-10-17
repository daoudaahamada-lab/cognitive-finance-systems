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
import { rates } from "@/server/domain/rates";
import { listCampaigns } from "@/server/services/campaigns";

export const metadata: Metadata = { title: "Campagnes" };

/** The link covers its whole row or card (the row needs `relative`); its focus ring is drawn on the cover. */
const stretchedLink =
  "after:absolute after:inset-0 focus-visible:outline-none focus-visible:after:rounded-control focus-visible:after:outline-solid " +
  "focus-visible:after:outline-2 focus-visible:after:-outline-offset-2 focus-visible:after:outline-brand-600";

export default async function CampaignsPage() {
  const { workspace } = await requireContext();
  const campaigns = (await listCampaigns(workspace.id)).map((c) => ({ ...c, rates: rates(c.funnel) }));

  return (
    <>
      <PageHeader
        title="Campagnes"
        description="Chaque campagne réunit un ciblage, une séquence de messages et un mode de réponse, sur l'un de vos comptes LinkedIn."
        actions={
          <ButtonLink href="/campaigns/new">
            <Plus className="size-4" aria-hidden /> Nouvelle campagne
          </ButtonLink>
        }
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
          <>
            {/* Phones and small tablets: one card per campaign. */}
            <ul className="divide-y divide-line md:hidden">
              {campaigns.map((c) => (
                <li key={c.id} className="relative px-4 py-3 hover:bg-surface-2">
                  <div className="flex items-start justify-between gap-3">
                    <Link href={`/campaigns/${c.id}`} className={`min-w-0 break-words font-medium text-ink ${stretchedLink}`}>
                      {c.name}
                    </Link>
                    <LabeledBadge map={CAMPAIGN_STATUS} value={c.status} />
                  </div>
                  <p className="mt-0.5 truncate text-xs text-muted">
                    {c.account.fullName} · Setter : {SETTER_MODES[c.setterMode]?.label ?? c.setterMode}
                  </p>
                  <dl className="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs">
                    <Figure label="Prospects" value={formatNumber(c.funnel.found)} />
                    <Figure label="Acceptation" value={formatPercent(c.rates.acceptance)} />
                    <Figure label="Réponse" value={formatPercent(c.rates.reply)} />
                    <Figure label="RDV" value={formatNumber(c.funnel.meetings)} strong />
                  </dl>
                </li>
              ))}
            </ul>

            {/* From md: the table; the whole row opens the campaign. */}
            <div className="hidden overflow-x-auto md:block">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Campagne</th>
                    <th>Statut</th>
                    <th className="text-right">Prospects</th>
                    <th className="text-right">Invités</th>
                    <th className="text-right">Acceptation</th>
                    <th className="text-right" title="Réponses / prospects contactés">Réponse</th>
                    <th className="text-right">RDV</th>
                    <th>Setter</th>
                  </tr>
                </thead>
                <tbody>
                  {campaigns.map((c) => (
                    <tr key={c.id} className="relative">
                      <td>
                        <Link href={`/campaigns/${c.id}`} className={`font-medium text-ink ${stretchedLink}`}>
                          {c.name}
                        </Link>
                        <p className="text-xs text-muted">{c.account.fullName}</p>
                      </td>
                      <td><LabeledBadge map={CAMPAIGN_STATUS} value={c.status} /></td>
                      <td className="text-right tabular-nums">{formatNumber(c.funnel.found)}</td>
                      <td className="text-right tabular-nums">{formatNumber(c.funnel.invited)}</td>
                      <td className="text-right tabular-nums">{formatPercent(c.rates.acceptance)}</td>
                      <td className="text-right tabular-nums">{formatPercent(c.rates.reply)}</td>
                      <td className="text-right font-semibold tabular-nums">{formatNumber(c.funnel.meetings)}</td>
                      <td className="text-sm text-muted">{SETTER_MODES[c.setterMode]?.label}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </Card>
    </>
  );
}

function Figure({ label, value, strong = false }: { label: string; value: string; strong?: boolean }) {
  return (
    <div className="flex items-baseline gap-1">
      <dt className="text-muted">{label}</dt>
      <dd className={strong ? "font-semibold text-ink tabular-nums" : "font-medium text-ink-2 tabular-nums"}>{value}</dd>
    </div>
  );
}
