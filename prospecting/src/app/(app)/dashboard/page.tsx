import { ArrowRight, CircleCheck, Inbox, Sparkles } from "lucide-react";
import type { ReactNode } from "react";
import type { Metadata } from "next";
import Link from "next/link";
import { ColumnChart } from "@/components/charts/column-chart";
import { FunnelChart } from "@/components/charts/funnel-chart";
import { ButtonLink } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, Meter, PageHeader } from "@/components/ui/misc";
import { cn } from "@/lib/cn";
import { formatDateTime, formatNumber, formatPercent } from "@/lib/format";
import { requireContext } from "@/server/auth/context";
import { listAccounts } from "@/server/services/accounts";
import { dashboard } from "@/server/services/analytics";
import { onboardingStatus } from "@/server/services/workspace";

export const metadata: Metadata = { title: "Tableau de bord" };

const PERIODS = [7, 30, 90] as const;

export default async function DashboardPage({ searchParams }: { searchParams: Promise<{ days?: string }> }) {
  const { workspace } = await requireContext();
  const requested = Number((await searchParams).days);
  const days = PERIODS.includes(requested as (typeof PERIODS)[number]) ? requested : 30;

  const [data, onboarding, accounts] = await Promise.all([
    dashboard(workspace.id, days),
    onboardingStatus(workspace.id),
    listAccounts(workspace.id),
  ]);
  const shortDate = (day: string) => new Date(`${day}T12:00:00Z`).toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
  const sum = (key: "invites" | "messages" | "replies" | "meetings") => data.series.reduce((s, p) => s + p[key], 0);

  return (
    <>
      <PageHeader title="Tableau de bord" description="Ce que votre machine de prospection a produit, et ce qui attend une décision de votre part." />

      <div className="mb-6 flex gap-1" role="group" aria-label="Période">
        {PERIODS.map((p) => (
          <Link
            key={p}
            href={`/dashboard?days=${p}`}
            aria-current={p === days ? "true" : undefined}
            className={cn(
              "rounded-lg px-3 py-1.5 text-sm font-medium",
              p === days ? "bg-ink text-white" : "text-muted hover:bg-surface hover:text-ink",
            )}
          >
            {p} jours
          </Link>
        ))}
      </div>

      {!Object.values(onboarding).every(Boolean) ? <Onboarding status={onboarding} /> : null}

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-5">
        <Stat label="Prospects trouvés" value={formatNumber(data.kpis.found)} />
        <Stat label="Invitations envoyées" value={formatNumber(data.kpis.invited)} />
        <Stat label="Taux d'acceptation" value={formatPercent(data.kpis.acceptanceRate)} hint="des invitations de la période" />
        <Stat label="Taux de réponse" value={formatPercent(data.kpis.replyRate)} hint="des premiers messages" />
        <Stat label="Rendez-vous réservés" value={formatNumber(data.kpis.meetings)} highlight />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader title="Entonnoir" description={`Prospects trouvés sur les ${days} derniers jours, par étape atteinte`} />
          <CardBody>
            <FunnelChart
              steps={[
                { label: "Trouvés", value: data.funnel.found },
                { label: "Qualifiés", value: data.funnel.qualified },
                { label: "Invités", value: data.funnel.invited },
                { label: "Connectés", value: data.funnel.connected },
                { label: "Ont répondu", value: data.funnel.replied },
                { label: "RDV réservés", value: data.funnel.meetings },
              ]}
            />
          </CardBody>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader title="À traiter" actions={<ButtonLink href="/inbox" variant="ghost" size="sm">Ouvrir <ArrowRight className="size-3.5" /></ButtonLink>} />
            <CardBody className="space-y-2">
              <TodoRow href="/inbox?tab=todo" icon={<Inbox className="size-4" />} label="Conversations à traiter" count={data.inbox.todo} />
              <TodoRow href="/inbox?tab=drafts" icon={<Sparkles className="size-4" />} label="Brouillons du setter à valider" count={data.inbox.drafts} />
            </CardBody>
          </Card>
          <Card>
            <CardHeader title="Prochains rendez-vous" actions={<ButtonLink href="/meetings" variant="ghost" size="sm">Tout voir</ButtonLink>} />
            <CardBody>
              {data.upcomingMeetings.length === 0 ? (
                <p className="text-sm text-muted">Aucun rendez-vous à venir pour l&apos;instant.</p>
              ) : (
                <ul className="space-y-3">
                  {data.upcomingMeetings.map((m) => (
                    <li key={m.id} className="flex items-center gap-3">
                      <Avatar first={m.prospect.firstName} last={m.prospect.lastName} size="sm" />
                      <div className="min-w-0 flex-1">
                        <Link href={`/prospects/${m.prospect.id}`} className="block truncate text-sm font-medium hover:underline">
                          {m.prospect.firstName} {m.prospect.lastName}
                        </Link>
                        <p className="truncate text-xs text-muted">{m.prospect.company}</p>
                      </div>
                      <span className="text-xs text-muted">{formatDateTime(m.startsAt)}</span>
                    </li>
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        </div>
      </div>

      <Card className="mt-6">
        <CardHeader title="Activité quotidienne" description={`${data.series.length} derniers jours`} />
        <CardBody className="grid gap-8 pt-6 sm:grid-cols-2 xl:grid-cols-4">
          <ColumnChart title="Invitations" total={sum("invites")} points={data.series.map((p) => ({ label: shortDate(p.day), value: p.invites }))} />
          <ColumnChart title="Messages envoyés" total={sum("messages")} points={data.series.map((p) => ({ label: shortDate(p.day), value: p.messages }))} />
          <ColumnChart title="Réponses reçues" total={sum("replies")} points={data.series.map((p) => ({ label: shortDate(p.day), value: p.replies }))} />
          <ColumnChart title="Rendez-vous" total={sum("meetings")} points={data.series.map((p) => ({ label: shortDate(p.day), value: p.meetings }))} />
        </CardBody>
      </Card>

      <Card className="mt-6">
        <CardHeader title="Quotas LinkedIn" description="Fenêtres glissantes de 24 h et 7 jours. Le moteur s'arrête avant les plafonds." actions={<ButtonLink href="/accounts" variant="ghost" size="sm">Gérer</ButtonLink>} />
        <CardBody>
          {accounts.length === 0 ? (
            <p className="text-sm text-muted">Aucun compte connecté.</p>
          ) : (
            <div className="grid gap-6 md:grid-cols-2">
              {accounts.map((a) => (
                <div key={a.id} className="space-y-3">
                  <p className="text-sm font-medium">{a.fullName}</p>
                  <Meter label="Invitations (24 h)" value={a.quota.usage.invitesLast24h} max={a.quota.limits.dailyInvites} />
                  <Meter label="Invitations (7 jours)" value={a.quota.usage.invitesLast7d} max={a.quota.limits.weeklyInvites} />
                  <Meter label="Messages (24 h)" value={a.quota.usage.messagesLast24h} max={a.quota.limits.dailyMessages} />
                </div>
              ))}
            </div>
          )}
        </CardBody>
      </Card>
    </>
  );
}

function Stat({ label, value, hint, highlight }: { label: string; value: string; hint?: string; highlight?: boolean }) {
  return (
    <div className={cn("rounded-xl border px-4 py-3", highlight ? "border-brand-200 bg-brand-50" : "border-line bg-surface")}>
      <p className="text-xs text-muted">{label}</p>
      <p className={cn("mt-1 text-2xl font-semibold tracking-tight", highlight ? "text-brand-900" : "text-ink")}>{value}</p>
      {hint ? <p className="text-[11px] text-muted">{hint}</p> : null}
    </div>
  );
}

function TodoRow({ href, icon, label, count }: { href: string; icon: ReactNode; label: string; count: number }) {
  return (
    <Link href={href} className="flex items-center gap-3 rounded-lg px-2 py-2 hover:bg-canvas">
      <span className={cn("flex size-8 items-center justify-center rounded-lg", count > 0 ? "bg-red-50 text-red-700" : "bg-canvas text-muted")}>{icon}</span>
      <span className="flex-1 text-sm">{label}</span>
      <span className="text-sm font-semibold tabular-nums">{count}</span>
    </Link>
  );
}

function Onboarding({ status }: { status: Awaited<ReturnType<typeof onboardingStatus>> }) {
  const steps = [
    { done: status.accountConnected, label: "Connecter votre compte LinkedIn", href: "/accounts" },
    { done: status.offerDescribed, label: "Décrire votre offre et votre lien de réservation", href: "/settings" },
    { done: status.campaignCreated, label: "Créer une campagne (ciblage + séquence)", href: "/campaigns/new" },
    { done: status.campaignLaunched, label: "Lancer la campagne", href: "/campaigns" },
  ];
  return (
    <Card className="mb-6 border-brand-200">
      <CardHeader title="Démarrage" description="Quatre étapes pour que le moteur commence à prospecter pour vous." />
      <CardBody>
        <ol className="grid gap-2 md:grid-cols-2">
          {steps.map((s, i) => (
            <li key={s.label}>
              <Link href={s.href} className="flex items-center gap-3 rounded-lg border border-line px-3 py-2.5 hover:bg-canvas">
                {s.done ? (
                  <CircleCheck className="size-5 text-emerald-600" aria-label="Fait" />
                ) : (
                  <span className="flex size-5 items-center justify-center rounded-full border border-line text-[11px] text-muted">{i + 1}</span>
                )}
                <span className={cn("text-sm", s.done && "text-muted line-through")}>{s.label}</span>
              </Link>
            </li>
          ))}
        </ol>
      </CardBody>
    </Card>
  );
}

