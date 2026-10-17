import { CirclePause, ExternalLink, MessageSquare, Sparkles } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { Button, ButtonLink, buttonClass } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, PageHeader, ScorePill } from "@/components/ui/misc";
import { Timeline, activityVisual, type TimelineItem } from "@/components/ui/timeline";
import { cn } from "@/lib/cn";
import { ACTIVITY_LABELS, CONVERSATION_STATUS, INTENTS, MEETING_STATUS, SOURCES, STAGE_LABELS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import type { ScoreReason } from "@/server/agents/scorer";
import { getProspect } from "@/server/services/prospects";
import { formatDateTimeIn, formatTime, groupByDay } from "../../meetings/dates";
import { OutcomeButtons } from "../../meetings/meeting-buttons";
import { snoozeAction } from "../actions";
import { SignalBadge } from "../signal-badge";
import { canLogMeeting, canSnooze, manualStageActions } from "../stage-rules";
import { MeetingForm, NotesForm, StageButtons } from "./prospect-actions";

export const metadata: Metadata = { title: "Prospect" };

type Prospect = NonNullable<Awaited<ReturnType<typeof getProspect>>>;
type Activity = Prospect["activities"][number];

export default async function ProspectPage({ params }: { params: Promise<{ id: string }> }) {
  const { workspace } = await requireContext();
  const { id } = await params;
  const p = await getProspect(workspace.id, id);
  if (!p) notFound();
  const now = new Date();
  const timeZone = workspace.timezone;
  const reasons = (p.scoreReasons ?? []) as ScoreReason[];
  const snoozed = p.snoozedUntil !== null && p.snoozedUntil > now;
  const name = `${p.firstName} ${p.lastName}`;

  // Each block of the Actions card shows only when it applies; with none, the card is left out.
  const hasStageButtons = manualStageActions(p.stage).length > 0;
  const showSnooze = canSnooze(p.stage) || snoozed;
  const showMeetingForm = canLogMeeting(p.stage);

  return (
    <>
      <PageHeader
        title={
          <span className="flex items-center gap-4">
            <Avatar first={p.firstName} last={p.lastName} size="lg" />
            <span className="min-w-0">
              <span className="block">{name}</span>
              <span className="block text-sm font-normal text-muted">{p.headline}</span>
            </span>
          </span>
        }
        actions={
          <>
            {p.conversation ? (
              <ButtonLink href={`/inbox?c=${p.conversation.id}`} variant="secondary">
                <MessageSquare className="size-4" aria-hidden /> Conversation
              </ButtonLink>
            ) : null}
            <a href={p.profileUrl} target="_blank" rel="noopener noreferrer" className={buttonClass({ variant: "ghost" })}>
              Profil LinkedIn <ExternalLink className="size-3.5" aria-hidden />
              <span className="sr-only"> (nouvel onglet)</span>
            </a>
          </>
        }
      />

      {/* Three grid children: on phones Profil and Score, then the actions column, then Historique;
          from xl the actions column sits on the right across both rows. */}
      <div className="grid gap-6 xl:grid-cols-3 xl:grid-rows-[auto_1fr] xl:items-start">
        <div className="min-w-0 space-y-6 xl:col-span-2">
          <Card>
            <CardHeader
              title="Profil"
              actions={
                <>
                  <ScorePill score={p.score} />
                  <LabeledBadge map={STAGE_LABELS} value={p.stage} />
                </>
              }
            />
            <CardBody className="grid grid-cols-2 gap-4 text-sm sm:grid-cols-3">
              <Info label="Poste">{p.title || "—"}</Info>
              <Info label="Entreprise">
                {p.company || "—"} {p.companySize ? <span className="text-muted">({p.companySize} sal.)</span> : null}
              </Info>
              <Info label="Secteur">{p.industry || "—"}</Info>
              <Info label="Zone">{p.location || "—"}</Info>
              <Info label="Origine">{SOURCES[p.source]?.label ?? p.source}</Info>
              <Info label="Signal">
                {p.signal ? <SignalBadge signal={p.signal} /> : "—"}
                {p.signalDetail ? <span className="mt-1 block text-xs text-muted">{p.signalDetail}</span> : null}
              </Info>
              <Info label="Campagne">
                <Link href={`/campaigns/${p.campaign.id}`} className="hover:underline">
                  {p.campaign.name}
                </Link>
              </Info>
              <Info label="Compte">{p.account.fullName}</Info>
              <Info label="Relances envoyées">{p.followUpsSent}</Info>
            </CardBody>
          </Card>

          <Card>
            <CardHeader
              title="Pourquoi ce score"
              description={`Minimum de la campagne : ${p.campaign.minScore}/100${p.disqualifiedReason ? ` · ${p.disqualifiedReason}` : ""}`}
              actions={
                p.scoredBy ? (
                  p.scoredBy === "claude" ? (
                    <Badge tone="ai">
                      <Sparkles className="size-3" aria-hidden /> Note de Claude
                    </Badge>
                  ) : (
                    <Badge tone="neutral">Note calculée par critères</Badge>
                  )
                ) : null
              }
            />
            <CardBody>
              {p.scoreSummary ? <p className="mb-3 rounded-control bg-surface-2 px-3 py-2 text-sm text-ink-2">{p.scoreSummary}</p> : null}
              {reasons.length === 0 ? (
                <p className="text-sm text-muted">Pas encore évalué.</p>
              ) : (
                <ul className="divide-y divide-line text-sm">
                  {reasons.map((r) => (
                    <ReasonRow key={r.label} reason={r} />
                  ))}
                </ul>
              )}
            </CardBody>
          </Card>
        </div>

        <div className="min-w-0 space-y-6 xl:col-start-3 xl:row-span-2 xl:row-start-1">
          {hasStageButtons || showSnooze || showMeetingForm ? (
            <Card>
              <CardHeader title="Actions" />
              <CardBody className="space-y-5">
                <StageButtons prospectId={p.id} stage={p.stage} />
                {showSnooze ? <SnoozeControl prospectId={p.id} stage={p.stage} until={snoozed ? p.snoozedUntil : null} timeZone={timeZone} /> : null}
                {showMeetingForm ? <MeetingForm prospectId={p.id} /> : null}
              </CardBody>
            </Card>
          ) : null}

          {p.conversation ? (
            <Card>
              <CardHeader title="Conversation" actions={<LabeledBadge map={CONVERSATION_STATUS} value={p.conversation.status} />} />
              <CardBody>
                <ButtonLink href={`/inbox?c=${p.conversation.id}`} variant="secondary" size="sm">
                  Ouvrir dans la boîte
                </ButtonLink>
              </CardBody>
            </Card>
          ) : null}

          {p.meetings.length > 0 ? (
            <Card>
              <CardHeader title="Rendez-vous" />
              <CardBody className="space-y-4">
                {p.meetings.map((m) => {
                  // A passed meeting still SCHEDULED waits for its outcome: never show it as 'Planifié'.
                  const toConfirm = m.status === "SCHEDULED" && m.startsAt < now;
                  return (
                    <div key={m.id} className="space-y-2">
                      <div className="flex items-center justify-between gap-2 text-sm">
                        <time dateTime={m.startsAt.toISOString()}>{formatDateTimeIn(m.startsAt, timeZone)}</time>
                        {toConfirm ? <Badge tone="warning">À confirmer</Badge> : <LabeledBadge map={MEETING_STATUS} value={m.status} />}
                      </div>
                      {toConfirm ? <OutcomeButtons meetingId={m.id} name={name} className="md:grid" /> : null}
                    </div>
                  );
                })}
              </CardBody>
            </Card>
          ) : null}

          <Card>
            <CardHeader title="Notes" />
            <CardBody>
              <NotesForm prospectId={p.id} notes={p.notes} />
            </CardBody>
          </Card>
        </div>

        <div className="min-w-0 xl:col-span-2">
          <Card>
            <CardHeader title="Historique" />
            <CardBody className="space-y-5">
              {p.activities.length === 0 ? (
                <p className="text-sm text-muted">Aucune activité pour l&apos;instant.</p>
              ) : (
                groupByDay(p.activities, (a) => a.createdAt, now, timeZone).map((day) => (
                  <section key={day.key} aria-labelledby={`jour-${day.key}`}>
                    <h3 id={`jour-${day.key}`} className="mb-3 text-xs font-semibold tracking-wide text-muted uppercase">
                      {day.label}
                    </h3>
                    <Timeline items={day.items.map((a) => activityItem(a, timeZone))} />
                  </section>
                ))
              )}
            </CardBody>
          </Card>
        </div>
      </div>
    </>
  );
}

function Info({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="min-w-0">
      <p className="text-xs text-muted">{label}</p>
      <div className="mt-0.5 break-words">{children}</div>
    </div>
  );
}

/** Label, a bar filled to points / max (success when full), then "x / y". AI reasons have no scale: favourable or not. */
function ReasonRow({ reason }: { reason: ScoreReason }) {
  const { label, points, max } = reason;
  if (!max) {
    return (
      <li className="flex items-center justify-between gap-3 py-2">
        <span className={points > 0 ? "text-ink" : "text-muted"}>{label}</span>
        <span className={cn("shrink-0", points > 0 ? "text-success" : "text-muted")}>{points > 0 ? "Favorable" : "Défavorable"}</span>
      </li>
    );
  }
  const ratio = Math.min(1, Math.max(0, points / max));
  const fill = ratio >= 1 ? "bg-success" : ratio <= 0 ? "bg-line-strong" : "bg-brand-600";
  return (
    <li className="flex items-center gap-3 py-2">
      <span className={cn("min-w-0 flex-1", points <= 0 ? "text-muted" : "text-ink")}>{label}</span>
      <span aria-hidden className="h-1.5 w-20 shrink-0 overflow-hidden rounded-full bg-surface-2 ring-1 ring-line ring-inset sm:w-[120px]">
        <span className={cn("block h-full rounded-full", fill)} style={{ width: `${ratio * 100}%` }} />
      </span>
      <span className="min-w-14 shrink-0 text-right whitespace-nowrap tabular-nums text-muted">
        {points} / {max}
      </span>
    </li>
  );
}

function SnoozeControl({ prospectId, stage, until, timeZone }: { prospectId: string; stage: string; until: Date | null; timeZone: string }) {
  return (
    <div role="group" aria-labelledby="envois-titre" aria-describedby="envois-aide">
      <p id="envois-titre" className="text-sm font-medium text-ink">
        Suspendre les envois
      </p>
      <p id="envois-aide" className="mt-0.5 text-xs text-muted">
        Aucune invitation ni relance pendant cette durée. Ses réponses arrivent toujours dans votre boîte.
      </p>
      {until ? (
        <p className="mt-2 inline-flex items-center gap-1.5 rounded-control bg-warning-soft px-2.5 py-1 text-xs font-medium text-warning">
          <CirclePause className="size-3.5 shrink-0" aria-hidden /> Envois suspendus jusqu&apos;au {formatDateTimeIn(until, timeZone)}
        </p>
      ) : null}
      <div className="mt-2 flex flex-wrap gap-2">
        {canSnooze(stage)
          ? [3, 7, 30].map((days) => (
              <form key={days} action={snoozeAction.bind(null, prospectId, days)}>
                <Button type="submit" variant="secondary" size="sm">
                  {days} jours
                </Button>
              </form>
            ))
          : null}
        {until ? (
          <form action={snoozeAction.bind(null, prospectId, 0)}>
            <Button type="submit" variant="ghost" size="sm">
              Reprendre maintenant
            </Button>
          </form>
        ) : null}
      </div>
    </div>
  );
}

/** One Historique entry: kit Timeline icon and tone, time and the details the engine recorded. */
function activityItem(a: Activity, timeZone: string): TimelineItem {
  const data = (a.data ?? {}) as Record<string, unknown>;
  const { icon, tone } = activityVisual(a.type);
  const details = [formatTime(a.createdAt, timeZone)];
  if (a.type === "FOLLOW_UP_SENT" && typeof data.step === "number") details.push(`relance ${data.step}`);
  if (typeof data.intent === "string" && INTENTS[data.intent]) details.push(INTENTS[data.intent]!);
  if (typeof data.startsAt === "string" && !Number.isNaN(Date.parse(data.startsAt))) {
    details.push(`RDV le ${formatDateTimeIn(new Date(data.startsAt), timeZone)}`);
  }
  if (typeof data.reason === "string") details.push(data.reason);
  if (typeof data.message === "string") details.push(data.message);
  if (typeof data.score === "number") details.push(`note ${data.score}/100`);
  return {
    id: a.id,
    icon,
    tone,
    title: ACTIVITY_LABELS[a.type] ?? a.type,
    meta: <time dateTime={a.createdAt.toISOString()}>{details.join(" · ")}</time>,
    body: typeof data.note === "string" ? <p className="rounded-control bg-surface-2 px-3 py-2 text-xs">{data.note}</p> : undefined,
  };
}
