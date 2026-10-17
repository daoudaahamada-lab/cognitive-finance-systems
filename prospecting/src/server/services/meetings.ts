import type { MeetingStatus, Prisma } from "@prisma/client";
import { db } from "@/server/db";
import { UserError } from "./errors";

const include = {
  prospect: { select: { id: true, firstName: true, lastName: true, title: true, company: true, profileUrl: true } },
  campaign: { select: { name: true } },
} satisfies Prisma.MeetingInclude;

/** Share of resolved meetings that took place (completed / (completed + no-show)), null before any outcome. */
export function showRate(completed: number, noShow: number): number | null {
  const resolved = completed + noShow;
  return resolved > 0 ? completed / resolved : null;
}

/**
 * Meetings split by what they need:
 * - toConfirm: passed but still SCHEDULED (did it happen?), oldest first;
 * - upcoming: SCHEDULED and still ahead, soonest first;
 * - history: every resolved meeting (held, no-show, canceled), newest first, the last 100;
 * - past: toConfirm and history merged, newest first (the last 100), as list_meetings returns it;
 * - stats: outcome counts over the whole workspace and the show rate.
 */
export async function listMeetings(workspaceId: string, now = new Date()) {
  const [toConfirm, upcoming, history, counts] = await Promise.all([
    db.meeting.findMany({ where: { workspaceId, status: "SCHEDULED", startsAt: { lt: now } }, include, orderBy: { startsAt: "asc" } }),
    db.meeting.findMany({ where: { workspaceId, status: "SCHEDULED", startsAt: { gte: now } }, include, orderBy: { startsAt: "asc" } }),
    db.meeting.findMany({ where: { workspaceId, status: { not: "SCHEDULED" } }, include, orderBy: { startsAt: "desc" }, take: 100 }),
    db.meeting.groupBy({ by: ["status"], where: { workspaceId, status: { not: "SCHEDULED" } }, _count: { _all: true } }),
  ]);
  const count = (status: MeetingStatus) => counts.find((c) => c.status === status)?._count._all ?? 0;
  const completed = count("COMPLETED");
  const noShow = count("NO_SHOW");
  const past = [...toConfirm, ...history].sort((a, b) => b.startsAt.getTime() - a.startsAt.getTime()).slice(0, 100);
  return {
    toConfirm,
    upcoming,
    history,
    past,
    stats: { completed, noShow, canceled: count("CANCELED"), showRate: showRate(completed, noShow) },
  };
}

export async function setMeetingStatus(workspaceId: string, meetingId: string, status: MeetingStatus) {
  const { count } = await db.meeting.updateMany({ where: { id: meetingId, workspaceId }, data: { status } });
  if (count === 0) throw new UserError("Rendez-vous introuvable.");
}
