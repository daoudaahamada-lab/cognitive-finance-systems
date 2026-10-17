import { CalendarCheck, ChevronDown, Inbox } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { ButtonLink } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState, PageHeader } from "@/components/ui/misc";
import { cn } from "@/lib/cn";
import { formatNumber, formatPercent } from "@/lib/format";
import { MEETING_STATUS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { listMeetings } from "@/server/services/meetings";
import { dateBlock, dayLabel, formatDateTimeIn, formatTime, groupByDay } from "./dates";
import { CancelMeetingButton, CorrectOutcomeButton, OutcomeButtons, RestoreMeetingButton } from "./meeting-buttons";

export const metadata: Metadata = { title: "Rendez-vous" };

type Meeting = Awaited<ReturnType<typeof listMeetings>>["upcoming"][number];

export default async function MeetingsPage() {
  const { workspace } = await requireContext();
  const now = new Date();
  const timeZone = workspace.timezone;
  const [{ toConfirm, upcoming, history, stats }, simulators] = await Promise.all([
    listMeetings(workspace.id, now),
    db.linkedInAccount.count({ where: { workspaceId: workspace.id, provider: "simulator" } }),
  ]);
  // The simulator books meetings through the booking link; a real account never does (Vela does not read calendars).
  const simulated = simulators > 0;
  const header = (
    <PageHeader
      title="Rendez-vous"
      description={
        simulated
          ? "Les appels réservés par vos prospects via votre lien, ou enregistrés à la main."
          : "Vos rendez-vous avec les prospects. Vela ne lit pas votre agenda : enregistrez un RDV depuis la conversation ou la fiche prospect."
      }
    />
  );

  if (toConfirm.length + upcoming.length + history.length === 0) {
    return (
      <>
        {header}
        <Card>
          <EmptyState
            icon={<CalendarCheck className="size-5" aria-hidden />}
            title="Aucun rendez-vous enregistré"
            description={
              simulated
                ? "Dès qu'un prospect réserve un créneau, il apparaît ici."
                : "Quand un prospect accepte un appel, enregistrez-le depuis sa conversation : il apparaîtra ici."
            }
            action={
              <ButtonLink href="/inbox">
                <Inbox className="size-4" aria-hidden /> Ouvrir la boîte de réception
              </ButtonLink>
            }
          />
        </Card>
      </>
    );
  }

  const resolved = stats.completed + stats.noShow + stats.canceled;

  return (
    <>
      {header}
      <div className="space-y-8">
        {toConfirm.length > 0 ? (
          <section id="a-confirmer" aria-labelledby="a-confirmer-titre">
            <SectionTitle id="a-confirmer-titre" description="Ces rendez-vous sont passés : indiquez s'ils ont eu lieu.">
              À confirmer ({formatNumber(toConfirm.length)})
            </SectionTitle>
            <ul className="space-y-3 md:space-y-0 md:divide-y md:divide-line md:overflow-hidden md:rounded-card md:border md:border-line md:bg-surface md:shadow-card">
              {toConfirm.map((m) => (
                <MeetingRow key={m.id} m={m} now={now} timeZone={timeZone} toConfirm />
              ))}
            </ul>
          </section>
        ) : null}

        <section aria-labelledby="a-venir-titre">
          <SectionTitle id="a-venir-titre">À venir ({formatNumber(upcoming.length)})</SectionTitle>
          {upcoming.length === 0 ? (
            <p className="rounded-card border border-line bg-surface px-5 py-6 text-sm text-muted shadow-card">Aucun rendez-vous à venir.</p>
          ) : (
            <div className="space-y-5 md:space-y-0 md:overflow-hidden md:rounded-card md:border md:border-line md:bg-surface md:shadow-card">
              {groupByDay(upcoming, (m) => m.startsAt, now, timeZone).map((day) => (
                <section key={day.key} aria-labelledby={`jour-${day.key}`} className="md:border-t md:border-line md:first:border-t-0">
                  <h3
                    id={`jour-${day.key}`}
                    className="mb-2 px-1 text-xs font-semibold tracking-wide text-muted uppercase md:mb-0 md:border-b md:border-line md:bg-surface-2 md:px-5 md:py-2"
                  >
                    {day.label}
                  </h3>
                  <ul className="space-y-3 md:space-y-0 md:divide-y md:divide-line">
                    {day.items.map((m) => (
                      <MeetingRow key={m.id} m={m} now={now} timeZone={timeZone} />
                    ))}
                  </ul>
                </section>
              ))}
            </div>
          )}
        </section>

        {history.length > 0 ? (
          <details className="group rounded-card border border-line bg-surface shadow-card">
            <summary className="flex cursor-pointer list-none items-center gap-3 rounded-card px-5 py-4 hover:bg-surface-2 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 [&::-webkit-details-marker]:hidden">
              <span className="min-w-0 flex-1">
                <span className="block text-title font-semibold text-ink">Historique</span>
                <span className="block text-sm text-muted">
                  Effectués {formatNumber(stats.completed)} · Non honorés {formatNumber(stats.noShow)} · taux de présence {formatPercent(stats.showRate)}
                  {stats.canceled > 0 ? ` · Annulés ${formatNumber(stats.canceled)}` : ""}
                </span>
              </span>
              <ChevronDown className="size-5 shrink-0 text-muted transition-transform group-open:rotate-180" aria-hidden />
            </summary>
            <ul className="divide-y divide-line border-t border-line">
              {history.map((m) => (
                <HistoryRow key={m.id} m={m} timeZone={timeZone} />
              ))}
            </ul>
            {resolved > history.length ? (
              <p className="border-t border-line px-5 py-3 text-xs text-muted">Les {formatNumber(history.length)} derniers rendez-vous sont affichés.</p>
            ) : null}
          </details>
        ) : null}
      </div>
    </>
  );
}

function SectionTitle({ id, description, children }: { id: string; description?: string; children: ReactNode }) {
  return (
    <div className="mb-3">
      <h2 id={id} className="text-title font-semibold text-ink">
        {children}
      </h2>
      {description ? <p className="mt-0.5 text-sm text-muted">{description}</p> : null}
    </div>
  );
}

function fullName(m: Meeting) {
  return `${m.prospect.firstName} ${m.prospect.lastName}`;
}

/** Calendar-style date: day number over the short month. */
function DateBlock({ date, timeZone, warning }: { date: Date; timeZone: string; warning?: boolean }) {
  const { day, month } = dateBlock(date, timeZone);
  return (
    <time
      dateTime={date.toISOString()}
      className={cn(
        "flex size-11 shrink-0 flex-col items-center justify-center rounded-control leading-none",
        warning ? "bg-warning-soft text-warning" : "bg-brand-50 text-brand-700",
      )}
    >
      <span className="text-base font-semibold tabular-nums">{day}</span>
      <span className="mt-0.5 text-2xs">{month}</span>
    </time>
  );
}

/** One meeting: a card with full-width buttons on phones, a row from md. */
function MeetingRow({ m, now, timeZone, toConfirm = false }: { m: Meeting; now: Date; timeZone: string; toConfirm?: boolean }) {
  const name = fullName(m);
  const time = formatTime(m.startsAt, timeZone);
  const day = dayLabel(m.startsAt, now, timeZone);
  const meta = [
    toConfirm ? `${day} à ${time}` : time,
    `${m.durationMin} min`,
    m.prospect.company,
    m.campaign.name,
    m.origin === "manual" ? "saisi à la main" : null,
  ].filter(Boolean);
  return (
    <li className="flex flex-col gap-3 bg-surface max-md:rounded-card max-md:border max-md:border-line max-md:p-4 max-md:shadow-card md:flex-row md:items-center md:gap-4 md:px-5 md:py-3">
      <div className="flex min-w-0 flex-1 items-center gap-3">
        <DateBlock date={m.startsAt} timeZone={timeZone} warning={toConfirm} />
        <div className="min-w-0 flex-1">
          <div className="flex min-w-0 flex-wrap items-center gap-x-2 gap-y-1">
            <Link href={`/prospects/${m.prospect.id}`} className="min-w-0 truncate font-medium text-ink hover:underline">
              {name}
            </Link>
            {toConfirm ? <Badge tone="warning">À confirmer</Badge> : null}
          </div>
          <p className="mt-0.5 text-xs text-muted">{meta.join(" · ")}</p>
        </div>
      </div>
      {toConfirm ? (
        <OutcomeButtons meetingId={m.id} name={name} />
      ) : (
        <CancelMeetingButton meetingId={m.id} name={name} when={`${day.toLowerCase()} à ${time}`} className="md:shrink-0" />
      )}
    </li>
  );
}

function HistoryRow({ m, timeZone }: { m: Meeting; timeZone: string }) {
  const name = fullName(m);
  return (
    <li className="flex flex-col gap-2 px-5 py-3 sm:flex-row sm:items-center sm:gap-4">
      <div className="min-w-0 flex-1">
        <Link href={`/prospects/${m.prospect.id}`} className="font-medium text-ink hover:underline">
          {name}
        </Link>
        <p className="text-xs text-muted">{[formatDateTimeIn(m.startsAt, timeZone), m.prospect.company, m.campaign.name].filter(Boolean).join(" · ")}</p>
      </div>
      <div className="flex items-center gap-2 sm:shrink-0">
        <LabeledBadge map={MEETING_STATUS} value={m.status} />
        {m.status === "COMPLETED" || m.status === "NO_SHOW" ? (
          <CorrectOutcomeButton meetingId={m.id} name={name} status={m.status} />
        ) : m.status === "CANCELED" ? (
          // A cancellation made by mistake is undone here, not only through MCP.
          <RestoreMeetingButton meetingId={m.id} name={name} />
        ) : null}
      </div>
    </li>
  );
}
