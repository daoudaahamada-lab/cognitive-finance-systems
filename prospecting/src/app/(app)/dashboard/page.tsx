import {
  ArrowRight,
  CalendarClock,
  ChevronRight,
  CircleAlert,
  CircleCheck,
  CirclePause,
  Inbox,
  PowerOff,
  SearchX,
  Sparkles,
  TriangleAlert,
  Unplug,
  type LucideIcon,
} from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { ColumnChart } from "@/components/charts/column-chart";
import { FunnelChart } from "@/components/charts/funnel-chart";
import { ButtonLink } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, Meter, PageHeader } from "@/components/ui/misc";
import { SegmentedControl } from "@/components/ui/segmented-control";
import { Stat } from "@/components/ui/stat";
import { BRAND } from "@/lib/brand";
import { cn } from "@/lib/cn";
import { deltaRatio, formatNumber, formatPercent, plural } from "@/lib/format";
import type { SemanticTone } from "@/lib/labels";
import { toneClasses } from "@/lib/tones";
import { requireContext } from "@/server/auth/context";
import { listAccounts } from "@/server/services/accounts";
import { dashboard, type SeriesPoint } from "@/server/services/analytics";
import { attentionItems, type AttentionItem, type AttentionKind } from "@/server/services/attention";
import { onboardingStatus, type OnboardingStatus } from "@/server/services/workspace";

export const metadata: Metadata = { title: "Tableau de bord" };

const PERIODS = [7, 30, 90] as const;

const SERIES: { key: keyof Omit<SeriesPoint, "day">; title: string }[] = [
  { key: "invites", title: "Invitations" },
  { key: "messages", title: "Messages envoyés" },
  { key: "replies", title: "Réponses reçues" },
  { key: "meetings", title: "Rendez-vous" },
];

export default async function DashboardPage({ searchParams }: { searchParams: Promise<{ days?: string }> }) {
  const { workspace } = await requireContext();
  const requested = Number((await searchParams).days);
  const days = PERIODS.includes(requested as (typeof PERIODS)[number]) ? requested : 30;
  const now = new Date();

  const [data, onboarding, accounts, attention] = await Promise.all([
    dashboard(workspace.id, days, now),
    onboardingStatus(workspace.id),
    listAccounts(workspace.id, now),
    attentionItems(workspace.id, now),
  ]);
  const steps = onboardingSteps(onboarding);
  const header = (actions?: ReactNode) => (
    <PageHeader
      title="Tableau de bord"
      description="Ce que votre machine de prospection a produit, et ce qui attend une décision de votre part."
      actions={actions}
    />
  );

  // First run: nothing to chart yet, so no zero-filled KPIs or charts.
  if (!onboarding.campaignLaunched && data.kpis.found === 0) {
    return (
      <>
        {header()}
        <Onboarding steps={steps} />
        <Card className="border-dashed shadow-none">
          <CardBody className="py-6">
            <p className="text-sm text-muted">
              Vos statistiques apparaîtront ici après les premières invitations. Comptez 24 à 48 h pour les premières acceptations.
            </p>
          </CardBody>
        </Card>
      </>
    );
  }

  const { kpis, previousKpis: prev } = data;
  const deltaLabel = `par rapport aux ${days} jours précédents`;
  const rateDelta = (current: number | null, previous: number | null) => (current === null || previous === null ? null : deltaRatio(current, previous));
  const weekly = data.granularity === "week";
  const shortDate = (day: string) => new Date(`${day}T12:00:00Z`).toLocaleDateString("fr-FR", { day: "numeric", month: "short", timeZone: "UTC" });
  const isWeekend = (day: string) => [0, 6].includes(new Date(`${day}T12:00:00Z`).getUTCDay());

  return (
    <>
      {header(
        <SegmentedControl
          label="Période"
          value={String(days)}
          items={PERIODS.map((p) => ({ href: `/dashboard?days=${p}`, label: `${p} jours`, value: String(p) }))}
        />,
      )}

      {steps.every((s) => s.done) ? null : <Onboarding steps={steps} />}

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
        <Stat
          lead
          className="col-span-2"
          label="Rendez-vous réservés"
          value={formatNumber(kpis.meetings)}
          delta={deltaRatio(kpis.meetings, prev.meetings)}
          deltaLabel={deltaLabel}
          hint={plural(kpis.meetingsCompleted, "effectué")}
        />
        <Stat label="Prospects trouvés" value={formatNumber(kpis.found)} delta={deltaRatio(kpis.found, prev.found)} deltaLabel={deltaLabel} />
        <Stat label="Invitations envoyées" value={formatNumber(kpis.invited)} delta={deltaRatio(kpis.invited, prev.invited)} deltaLabel={deltaLabel} />
        <Stat
          label="Taux d'acceptation"
          value={formatPercent(kpis.acceptanceRate)}
          delta={rateDelta(kpis.acceptanceRate, prev.acceptanceRate)}
          deltaLabel={deltaLabel}
          hint="des invitations de la période"
        />
        <Stat
          label="Taux de réponse"
          value={formatPercent(kpis.replyRate)}
          delta={rateDelta(kpis.replyRate, prev.replyRate)}
          deltaLabel={deltaLabel}
          hint="des premiers messages"
        />
      </div>

      {/* The attention column comes first in reading order; from xl it sits on the right. */}
      <div className="mt-6 grid items-start gap-6 xl:grid-cols-3">
        <div className="min-w-0 space-y-6 xl:col-start-3 xl:row-start-1">
          <AttentionCard items={attention} />
          <UpcomingMeetings meetings={data.upcomingMeetings} timezone={workspace.timezone} />
        </div>

        <div className="min-w-0 space-y-6 xl:col-span-2 xl:col-start-1 xl:row-start-1">
          <Card>
            <CardHeader title="Entonnoir" description={`Prospects trouvés sur les ${days} derniers jours, par étape atteinte`} />
            <CardBody>
              <FunnelChart
                steps={[
                  { label: "Trouvés", value: data.funnel.found },
                  { label: "Qualifiés", value: data.funnel.qualified },
                  { label: "Invités", value: data.funnel.invited },
                  { label: "En relation", value: data.funnel.connected },
                  { label: "Ont répondu", value: data.funnel.replied },
                  { label: "RDV réservés", value: data.funnel.meetings },
                ]}
              />
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Activité" description={`${weekly ? "Par semaine" : "Par jour"}, sur les ${days} derniers jours`} />
            <CardBody className="grid gap-8 pt-6 sm:grid-cols-2">
              {SERIES.map(({ key, title }) => (
                <ColumnChart
                  key={key}
                  title={title}
                  per={weekly ? "sem." : "j"}
                  total={data.series.reduce((sum, p) => sum + p[key], 0)}
                  points={data.series.map((p) => ({
                    label: weekly ? `sem. du ${shortDate(p.day)}` : shortDate(p.day),
                    value: p[key],
                    weekend: !weekly && isWeekend(p.day),
                  }))}
                />
              ))}
            </CardBody>
          </Card>
        </div>
      </div>

      <Card className="mt-6">
        <CardHeader
          title="Quotas LinkedIn"
          description="Envois des dernières 24 h et des 7 derniers jours. Vela s'arrête toujours avant la limite."
          actions={<ButtonLink href="/accounts" variant="ghost" size="sm">Gérer</ButtonLink>}
        />
        <CardBody>
          {accounts.length === 0 ? (
            <p className="text-sm text-muted">Aucun compte connecté.</p>
          ) : (
            <div className="grid gap-6 md:grid-cols-[repeat(auto-fill,minmax(320px,1fr))]">
              {accounts.map((a) => (
                <div key={a.id} className="min-w-0 space-y-3">
                  <p className="truncate text-sm font-medium text-ink">{a.fullName}</p>
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

// ------------------------------------------------------------------ À traiter

const ATTENTION_VISUALS: Record<AttentionKind, { icon: LucideIcon; tone: SemanticTone }> = {
  account_paused: { icon: CirclePause, tone: "danger" },
  account_error: { icon: TriangleAlert, tone: "danger" },
  engine_down: { icon: PowerOff, tone: "danger" },
  account_disconnected: { icon: Unplug, tone: "warning" },
  action_failed: { icon: CircleAlert, tone: "warning" },
  campaign_exhausted: { icon: SearchX, tone: "warning" },
  inbox_todo: { icon: Inbox, tone: "brand" },
  drafts: { icon: Sparkles, tone: "ai" },
  meetings_to_confirm: { icon: CalendarClock, tone: "info" },
};

function AttentionCard({ items }: { items: AttentionItem[] }) {
  // The drafts are part of the inbox total: they show as an indented line under it, never as a second count.
  const inbox = items.some((i) => i.kind === "inbox_todo");
  const drafts = items.find((i) => i.kind === "drafts");
  const rows = items.filter((i) => i.kind !== "drafts" || !inbox);
  return (
    <Card>
      <CardHeader title="À traiter" />
      {rows.length === 0 ? (
        <CardBody>
          <p className="flex items-center gap-2 text-sm text-muted">
            <CircleCheck className="size-4 shrink-0 text-success" aria-hidden />
            Rien ne vous attend.
          </p>
        </CardBody>
      ) : (
        <ul className="divide-y divide-line">
          {rows.map((item, i) => (
            <li key={`${item.kind}-${i}`}>
              <AttentionRow item={item} />
              {item.kind === "inbox_todo" && drafts ? <AttentionRow item={drafts} nested /> : null}
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

function AttentionRow({ item, nested = false }: { item: AttentionItem; nested?: boolean }) {
  const visual = ATTENTION_VISUALS[item.kind];
  // A failure Vela already handled (a prospect it skipped) is information, not a warning.
  const tone: SemanticTone = item.kind === "action_failed" && item.severity === "low" ? "neutral" : visual.tone;
  const Icon = visual.icon;
  return (
    <Link
      href={item.href}
      className={cn(
        "group flex gap-3 px-5 hover:bg-surface-2 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand-600",
        nested ? "-mt-1 items-center pb-3 pl-16 pointer-coarse:min-h-11" : "items-start py-3",
      )}
    >
      {nested ? null : (
        <span className={cn("flex size-8 shrink-0 items-center justify-center rounded-control", toneClasses(tone).soft)}>
          <Icon className="size-4" aria-hidden />
        </span>
      )}
      <span className={cn("min-w-0 flex-1", !nested && "py-1.5")}>
        <span className={cn("block text-sm", nested ? "text-muted" : "font-medium text-ink")}>
          {item.severity === "high" ? <span className="sr-only">Urgent : </span> : null}
          {item.label}
        </span>
        {item.detail ? <span className="mt-0.5 block text-xs break-words text-muted">{item.detail}</span> : null}
      </span>
      {item.kind === "inbox_todo" ? (
        <span className="mt-1.5 shrink-0 rounded-full bg-brand-600 px-1.5 text-2xs font-semibold text-white tabular-nums">{formatNumber(item.count)}</span>
      ) : item.kind === "drafts" ? (
        <span className="shrink-0 text-sm text-muted tabular-nums">{formatNumber(item.count)}</span>
      ) : null}
      <ChevronRight className={cn("size-4 shrink-0 text-muted group-hover:text-ink", !nested && "mt-2")} aria-hidden />
    </Link>
  );
}

// --------------------------------------------------------- Prochains rendez-vous

type UpcomingMeeting = Awaited<ReturnType<typeof dashboard>>["upcomingMeetings"][number];

function UpcomingMeetings({ meetings, timezone }: { meetings: UpcomingMeeting[]; timezone: string }) {
  const dayFormat = new Intl.DateTimeFormat("fr-FR", { weekday: "long", day: "numeric", month: "long", timeZone: timezone });
  const timeFormat = new Intl.DateTimeFormat("fr-FR", { hour: "2-digit", minute: "2-digit", timeZone: timezone });
  const days: { label: string; meetings: UpcomingMeeting[] }[] = [];
  for (const m of meetings) {
    const day = dayFormat.format(m.startsAt);
    const label = day.charAt(0).toUpperCase() + day.slice(1);
    const last = days.at(-1);
    if (last?.label === label) last.meetings.push(m);
    else days.push({ label, meetings: [m] });
  }

  return (
    <Card>
      <CardHeader title="Rendez-vous à venir" actions={<ButtonLink href="/meetings" variant="ghost" size="sm">Tout voir</ButtonLink>} />
      <CardBody className="space-y-4">
        {days.length === 0 ? (
          <p className="text-sm text-muted">Aucun rendez-vous à venir pour l&apos;instant.</p>
        ) : (
          days.map((day) => (
            <div key={day.label}>
              <h3 className="mb-2 text-xs font-medium text-muted">{day.label}</h3>
              <ul className="space-y-3">
                {day.meetings.map((m) => (
                  <li key={m.id} className="flex items-center gap-3">
                    <time dateTime={m.startsAt.toISOString()} className="w-12 shrink-0 text-sm font-medium text-ink tabular-nums">
                      {timeFormat.format(m.startsAt)}
                    </time>
                    <Avatar first={m.prospect.firstName} last={m.prospect.lastName} size="sm" />
                    <div className="min-w-0 flex-1">
                      <Link href={`/prospects/${m.prospect.id}`} className="block truncate text-sm font-medium text-ink hover:underline">
                        {m.prospect.firstName} {m.prospect.lastName}
                      </Link>
                      <p className="truncate text-xs text-muted">{m.prospect.company}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </CardBody>
    </Card>
  );
}

// ------------------------------------------------------------------ Démarrage

type Step = { label: string; action: string; href: string; done: boolean; issue?: string };

function onboardingSteps(s: OnboardingStatus): Step[] {
  const steps: (Step | null)[] = [
    {
      label: "Connecter votre compte LinkedIn",
      action: "Connecter",
      href: s.accountIssue ? `/accounts#${s.accountIssue.accountId}` : "/accounts",
      done: s.accountReady,
      issue: s.accountIssue?.reason,
    },
    s.simulatorOnly
      ? null
      : {
          label: "Vérifier la connexion LinkedIn",
          action: "Vérifier",
          href: s.sessionIssue ? `/accounts#${s.sessionIssue.accountId}` : "/accounts",
          done: s.sessionVerified,
          issue: s.sessionIssue?.reason,
        },
    { label: "Décrire votre offre et votre lien de réservation", action: "Décrire", href: "/settings", done: s.offerDescribed },
    { label: "Créer une campagne", action: "Créer", href: "/campaigns/new", done: s.campaignCreated },
    { label: "Lancer la campagne", action: "Lancer", href: s.draftCampaignId ? `/campaigns/${s.draftCampaignId}` : "/campaigns", done: s.campaignLaunched },
  ];
  return steps.filter((step): step is Step => step !== null);
}

const COUNT_WORDS: Record<number, string> = { 4: "Quatre", 5: "Cinq" };

function Onboarding({ steps }: { steps: Step[] }) {
  const done = steps.filter((s) => s.done).length;
  const next = steps.findIndex((s) => !s.done);
  return (
    <Card className="mb-6 border-brand-200">
      <CardHeader
        title="Démarrage"
        description={`${COUNT_WORDS[steps.length] ?? steps.length} étapes pour que ${BRAND.name} commence à prospecter pour vous.`}
        actions={
          <span className="text-sm font-semibold text-ink-2 tabular-nums">
            {done} / {steps.length}
            <span className="sr-only"> étapes terminées</span>
          </span>
        }
      />
      <CardBody>
        <ol className="space-y-2">
          {steps.map((step, i) => (
            <li key={step.label}>
              {i === next ? (
                <div className="flex flex-wrap items-center gap-3 rounded-control border border-brand-200 bg-brand-50 px-3 py-3">
                  <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-brand-600 text-xs font-semibold text-white">{i + 1}</span>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-ink">{step.label}</p>
                    {step.issue ? <StepIssue text={step.issue} /> : null}
                  </div>
                  <ButtonLink href={step.href} size="sm" className="max-sm:w-full">
                    {step.action} <ArrowRight className="size-3.5" aria-hidden />
                  </ButtonLink>
                </div>
              ) : (
                <Link
                  href={step.href}
                  className="flex items-start gap-3 rounded-control border border-line px-3 py-2.5 hover:bg-surface-2 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600"
                >
                  {step.done ? (
                    <CircleCheck className="size-6 shrink-0 text-success" aria-hidden />
                  ) : (
                    <span className="flex size-6 shrink-0 items-center justify-center rounded-full border border-line-strong text-xs text-ink-2">{i + 1}</span>
                  )}
                  <span className="min-w-0 flex-1 pt-0.5">
                    <span className={cn("block text-sm", step.done ? "text-muted" : "text-ink")}>
                      {step.label}
                      {step.done ? <span className="sr-only"> (fait)</span> : null}
                    </span>
                    {!step.done && step.issue ? <StepIssue text={step.issue} /> : null}
                  </span>
                </Link>
              )}
            </li>
          ))}
        </ol>
      </CardBody>
    </Card>
  );
}

function StepIssue({ text }: { text: string }) {
  return (
    <span className="mt-1 flex items-start gap-1.5 text-xs text-danger">
      <TriangleAlert className="mt-px size-3.5 shrink-0" aria-hidden />
      <span className="min-w-0 break-words">{text}</span>
    </span>
  );
}
