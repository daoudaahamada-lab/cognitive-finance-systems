import type { MeetingStatus } from "@prisma/client";
import { CalendarCheck } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { LabeledBadge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardHeader } from "@/components/ui/card";
import { Avatar, EmptyState, PageHeader } from "@/components/ui/misc";
import { formatDateTime } from "@/lib/format";
import { MEETING_STATUS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { listMeetings } from "@/server/services/meetings";
import { meetingStatusAction } from "./actions";

export const metadata: Metadata = { title: "Rendez-vous" };

type Meeting = Awaited<ReturnType<typeof listMeetings>>["upcoming"][number];

export default async function MeetingsPage() {
  const { workspace } = await requireContext();
  const { upcoming, past } = await listMeetings(workspace.id);

  return (
    <>
      <PageHeader title="Rendez-vous" description="Les appels réservés par vos prospects via votre lien, ou enregistrés à la main." />
      <Card className="mb-6">
        <CardHeader title={`À venir (${upcoming.length})`} />
        {upcoming.length === 0 ? (
          <EmptyState icon={<CalendarCheck className="size-5" />} title="Aucun rendez-vous à venir" description="Dès qu'un prospect réserve un créneau, il apparaît ici." />
        ) : (
          <MeetingTable meetings={upcoming} actions={["CANCELED"]} />
        )}
      </Card>
      <Card>
        <CardHeader title="Passés" description="Indiquez si l'appel a eu lieu pour suivre votre taux de présence." />
        {past.length === 0 ? <p className="px-5 py-6 text-sm text-muted">Aucun rendez-vous passé.</p> : <MeetingTable meetings={past} actions={["COMPLETED", "NO_SHOW"]} />}
      </Card>
    </>
  );
}

const ACTION_LABELS: Partial<Record<MeetingStatus, string>> = { COMPLETED: "Effectué", NO_SHOW: "Absent", CANCELED: "Annuler" };

function MeetingTable({ meetings, actions }: { meetings: Meeting[]; actions: MeetingStatus[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="data-table">
        <thead>
          <tr>
            <th>Prospect</th>
            <th>Date</th>
            <th>Campagne</th>
            <th>Statut</th>
            <th className="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          {meetings.map((m) => (
            <tr key={m.id}>
              <td>
                <Link href={`/prospects/${m.prospect.id}`} className="flex items-center gap-3">
                  <Avatar first={m.prospect.firstName} last={m.prospect.lastName} size="sm" />
                  <span>
                    <span className="block font-medium hover:underline">{m.prospect.firstName} {m.prospect.lastName}</span>
                    <span className="block text-xs text-muted">{m.prospect.title} · {m.prospect.company}</span>
                  </span>
                </Link>
              </td>
              <td className="whitespace-nowrap">{formatDateTime(m.startsAt)} <span className="text-xs text-muted">· {m.durationMin} min</span></td>
              <td className="text-sm text-muted">{m.campaign.name}{m.origin === "manual" ? " · manuel" : ""}</td>
              <td><LabeledBadge map={MEETING_STATUS} value={m.status} /></td>
              <td>
                <div className="flex justify-end gap-1">
                  {actions.filter((a) => a !== m.status).map((a) => (
                    <form key={a} action={meetingStatusAction.bind(null, m.id, a)}>
                      <Button type="submit" size="sm" variant="ghost">{ACTION_LABELS[a]}</Button>
                    </form>
                  ))}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
