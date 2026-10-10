import { Pencil } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { FunnelChart } from "@/components/charts/funnel-chart";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { ButtonLink } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, PageHeader, ScorePill } from "@/components/ui/misc";
import { formatDate, formatRelative } from "@/lib/format";
import { CAMPAIGN_STATUS, SETTER_MODES, SIGNALS, SOURCES, STAGE_LABELS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { parseFollowUps } from "@/server/domain/followups";
import { planLimits } from "@/server/domain/plans";
import { funnelFromStages, getCampaign, stageCounts } from "@/server/services/campaigns";
import { CampaignControls } from "./campaign-controls";
import { ImportForm } from "./import-form";

export const metadata: Metadata = { title: "Campagne" };

export default async function CampaignPage({ params }: { params: Promise<{ id: string }> }) {
  const { workspace } = await requireContext();
  const { id } = await params;
  const campaign = await getCampaign(workspace.id, id);
  if (!campaign) notFound();

  const [counts, recent] = await Promise.all([
    stageCounts({ campaignId: campaign.id }),
    db.prospect.findMany({ where: { campaignId: campaign.id }, orderBy: { stageChangedAt: "desc" }, take: 10 }),
  ]);
  const funnel = funnelFromStages(counts);
  const followUps = parseFollowUps(campaign.followUps);
  const limits = planLimits(workspace.plan);

  return (
    <>
      <PageHeader
        title={
          <span className="flex flex-wrap items-center gap-3">
            {campaign.name} <LabeledBadge map={CAMPAIGN_STATUS} value={campaign.status} />
          </span>
        }
        description={`${campaign.account.fullName} · ${campaign.launchedAt ? `lancée le ${formatDate(campaign.launchedAt)}` : "jamais lancée"}`}
        actions={
          <>
            <ButtonLink href={`/campaigns/${campaign.id}/edit`} variant="secondary"><Pencil className="size-4" /> Modifier</ButtonLink>
            <CampaignControls campaignId={campaign.id} status={campaign.status} />
          </>
        }
      />

      <div className="grid gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader title="Entonnoir de la campagne" actions={<ButtonLink href={`/prospects?campaignId=${campaign.id}`} variant="ghost" size="sm">Tous les prospects</ButtonLink>} />
          <CardBody>
            <FunnelChart
              steps={[
                { label: "Trouvés", value: funnel.found },
                { label: "Qualifiés", value: funnel.qualified },
                { label: "Invités", value: funnel.invited },
                { label: "Connectés", value: funnel.connected },
                { label: "Ont répondu", value: funnel.replied },
                { label: "RDV réservés", value: funnel.meetings },
              ]}
            />
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="Réglages" />
          <CardBody className="space-y-3 text-sm">
            <Setting label="Sources">{campaign.sources.map((s) => SOURCES[s]?.label).join(", ") || "Aucune (import uniquement)"}</Setting>
            {campaign.sources.includes("SIGNALS") ? <Setting label="Signaux">{campaign.signals.map((s) => SIGNALS[s]).join(", ") || "Tous"}</Setting> : null}
            <Setting label="Postes"><Tags values={campaign.titles} empty="Tous" /></Setting>
            <Setting label="Secteurs"><Tags values={campaign.industries} empty="Tous" /></Setting>
            <Setting label="Zones"><Tags values={campaign.locations} empty="Toutes" /></Setting>
            <Setting label="Exclusions"><Tags values={campaign.exclusions} empty="Aucune" /></Setting>
            <Setting label="Score minimum">{campaign.minScore}/100 · {campaign.weeklyProspectTarget} prospects/semaine</Setting>
            <Setting label="Séquence">
              {campaign.inviteNote ? "Invitation avec note" : "Invitation sans note"}, premier message, {followUps.length} relance{followUps.length > 1 ? "s" : ""}
              {followUps.length ? ` (J+${followUps.map((f) => f.delayDays).join(", J+")})` : ""}
            </Setting>
            <Setting label="Personnalisation par Claude">{campaign.aiPersonalization ? "Activée" : "Désactivée (modèles envoyés tels quels)"}</Setting>
            <Setting label="Setter">{limits.setter ? SETTER_MODES[campaign.setterMode]?.label : "Non inclus dans le plan"}</Setting>
          </CardBody>
        </Card>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader title="Dernière activité" />
          {recent.length === 0 ? (
            <CardBody><p className="text-sm text-muted">Pas encore de prospect. Lancez la campagne ou importez une liste.</p></CardBody>
          ) : (
            <div className="overflow-x-auto">
              <table className="data-table">
                <tbody>
                  {recent.map((p) => (
                    <tr key={p.id}>
                      <td>
                        <Link href={`/prospects/${p.id}`} className="flex items-center gap-3">
                          <Avatar first={p.firstName} last={p.lastName} size="sm" />
                          <span className="min-w-0">
                            <span className="block truncate font-medium hover:underline">{p.firstName} {p.lastName}</span>
                            <span className="block truncate text-xs text-muted">{p.title} · {p.company}</span>
                          </span>
                        </Link>
                      </td>
                      <td><ScorePill score={p.score} /></td>
                      <td><LabeledBadge map={STAGE_LABELS} value={p.stage} /></td>
                      <td className="text-right text-xs text-muted">{formatRelative(p.stageChangedAt)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>

        <Card>
          <CardHeader title="Importer une liste" description="Les profils importés sont contactés quel que soit leur score. Les exclusions restent appliquées." />
          <CardBody>
            {limits.listImport ? <ImportForm campaignId={campaign.id} /> : <p className="text-sm text-muted">L&apos;import est disponible à partir du plan Pro.</p>}
          </CardBody>
        </Card>
      </div>
    </>
  );
}

function Setting({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-muted">{label}</p>
      <div className="mt-0.5">{children}</div>
    </div>
  );
}

function Tags({ values, empty }: { values: string[]; empty: string }) {
  if (values.length === 0) return <span className="text-muted">{empty}</span>;
  return (
    <span className="flex flex-wrap gap-1">
      {values.map((v) => <Badge key={v}>{v}</Badge>)}
    </span>
  );
}
