import { db } from "@/server/db";
import { DAY } from "@/server/domain/time";
import { funnelFromStages, stageCounts } from "./campaigns";
import { inboxCounts } from "./inbox";

export type DailyPoint = { day: string; invites: number; messages: number; replies: number; meetings: number };

function rate(part: number, whole: number): number | null {
  return whole > 0 ? part / whole : null;
}

export async function dashboard(workspaceId: string, days: number, now = new Date()) {
  const since = new Date(now.getTime() - days * DAY);
  const workspace = await db.workspace.findUniqueOrThrow({ where: { id: workspaceId } });

  // Cohort rates: of the people invited (messaged) in the period, how many accepted (replied).
  const [found, invited, accepted, messaged, replied, meetings, funnelStages] = await Promise.all([
    db.prospect.count({ where: { workspaceId, createdAt: { gte: since } } }),
    db.prospect.count({ where: { workspaceId, invitedAt: { gte: since } } }),
    db.prospect.count({ where: { workspaceId, invitedAt: { gte: since }, connectedAt: { not: null } } }),
    db.prospect.count({ where: { workspaceId, firstMessagedAt: { gte: since } } }),
    db.prospect.count({ where: { workspaceId, firstMessagedAt: { gte: since }, repliedAt: { not: null } } }),
    db.meeting.count({ where: { workspaceId, createdAt: { gte: since }, status: { not: "CANCELED" } } }),
    stageCounts({ workspaceId, createdAt: { gte: since } }),
  ]);

  const series = await dailySeries(workspaceId, workspace.timezone, Math.min(days, 30), now);
  const inbox = await inboxCounts(workspaceId);
  const upcomingMeetings = await db.meeting.findMany({
    where: { workspaceId, startsAt: { gte: now }, status: "SCHEDULED" },
    include: { prospect: { select: { id: true, firstName: true, lastName: true, company: true } } },
    orderBy: { startsAt: "asc" },
    take: 5,
  });

  return {
    kpis: {
      found,
      invited,
      acceptanceRate: rate(accepted, invited),
      replyRate: rate(replied, messaged),
      meetings,
    },
    funnel: funnelFromStages(funnelStages),
    series,
    inbox,
    upcomingMeetings,
  };
}

/** Per-day activity in the workspace's timezone, zero-filled. */
async function dailySeries(workspaceId: string, timezone: string, days: number, now: Date): Promise<DailyPoint[]> {
  const since = new Date(now.getTime() - days * DAY);
  const rows = await db.$queryRaw<{ day: string; type: string; n: bigint }[]>`
    SELECT to_char(("createdAt" AT TIME ZONE 'UTC') AT TIME ZONE ${timezone}, 'YYYY-MM-DD') AS day, type::text AS type, count(*) AS n
    FROM "Activity"
    WHERE "workspaceId" = ${workspaceId} AND "createdAt" >= ${since}
      AND type IN ('INVITE_SENT', 'MESSAGE_SENT', 'FOLLOW_UP_SENT', 'AI_REPLY_SENT', 'HUMAN_REPLY_SENT', 'REPLY_RECEIVED', 'MEETING_BOOKED')
    GROUP BY 1, 2`;

  const fmt = new Intl.DateTimeFormat("en-CA", { timeZone: timezone, year: "numeric", month: "2-digit", day: "2-digit" });
  const points = new Map<string, DailyPoint>();
  for (let i = days - 1; i >= 0; i--) {
    const day = fmt.format(new Date(now.getTime() - i * DAY));
    points.set(day, { day, invites: 0, messages: 0, replies: 0, meetings: 0 });
  }
  for (const row of rows) {
    const point = points.get(row.day);
    if (!point) continue;
    const n = Number(row.n);
    if (row.type === "INVITE_SENT") point.invites += n;
    else if (row.type === "REPLY_RECEIVED") point.replies += n;
    else if (row.type === "MEETING_BOOKED") point.meetings += n;
    else point.messages += n;
  }
  return [...points.values()];
}
