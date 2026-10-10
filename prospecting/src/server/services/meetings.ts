import type { MeetingStatus } from "@prisma/client";
import { db } from "@/server/db";
import { UserError } from "./errors";

export async function listMeetings(workspaceId: string, now = new Date()) {
  const include = { prospect: { select: { id: true, firstName: true, lastName: true, title: true, company: true, profileUrl: true } }, campaign: { select: { name: true } } };
  const [upcoming, past] = await Promise.all([
    db.meeting.findMany({ where: { workspaceId, startsAt: { gte: now }, status: "SCHEDULED" }, include, orderBy: { startsAt: "asc" } }),
    db.meeting.findMany({
      where: { workspaceId, OR: [{ startsAt: { lt: now } }, { status: { not: "SCHEDULED" } }] },
      include,
      orderBy: { startsAt: "desc" },
      take: 100,
    }),
  ]);
  return { upcoming, past };
}

export async function setMeetingStatus(workspaceId: string, meetingId: string, status: MeetingStatus) {
  const { count } = await db.meeting.updateMany({ where: { id: meetingId, workspaceId }, data: { status } });
  if (count === 0) throw new UserError("Rendez-vous introuvable.");
}
