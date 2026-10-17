import { db } from "@/server/db";
import { rates } from "@/server/domain/rates";
import { DAY } from "@/server/domain/time";
import { funnelFromStages, stageCounts } from "./campaigns";
import { inboxCounts } from "./inbox";

/** Activity of one column: a day, or a week starting on `day` (YYYY-MM-DD in the workspace's timezone). */
export type SeriesPoint = { day: string; invites: number; messages: number; replies: number; meetings: number };
export type SeriesGranularity = "day" | "week";

/** Periods longer than this are charted by week, so 90 days still fit as about 13 columns. */
const DAILY_MAX_DAYS = 31;

export type PeriodKpis = {
  found: number;
  invited: number;
  /** Of the people invited in the period, the share who accepted (null: nobody invited). */
  acceptanceRate: number | null;
  /** Of the people first messaged in the period, the share who replied (null: nobody messaged). */
  replyRate: number | null;
  /** Meetings booked in the period, cancellations excluded. */
  meetings: number;
  /** Of those meetings, the ones marked as held. */
  meetingsCompleted: number;
};

/** KPIs of the window [from, to); `to` null leaves it open (the current period). */
async function periodKpis(workspaceId: string, from: Date, to: Date | null): Promise<PeriodKpis> {
  const window = to ? { gte: from, lt: to } : { gte: from };
  // Cohort rates: of the people invited (messaged) in the period, how many accepted (replied).
  const [found, invited, connected, messaged, replied, meetings, meetingsCompleted] = await Promise.all([
    db.prospect.count({ where: { workspaceId, createdAt: window } }),
    db.prospect.count({ where: { workspaceId, invitedAt: window } }),
    db.prospect.count({ where: { workspaceId, invitedAt: window, connectedAt: { not: null } } }),
    db.prospect.count({ where: { workspaceId, firstMessagedAt: window } }),
    db.prospect.count({ where: { workspaceId, firstMessagedAt: window, repliedAt: { not: null } } }),
    db.meeting.count({ where: { workspaceId, createdAt: window, status: { not: "CANCELED" } } }),
    db.meeting.count({ where: { workspaceId, createdAt: window, status: "COMPLETED" } }),
  ]);
  const r = rates({ invited, connected, messaged, replied, meetings });
  return { found, invited, acceptanceRate: r.acceptance, replyRate: r.reply, meetings, meetingsCompleted };
}

export async function dashboard(workspaceId: string, days: number, now = new Date()) {
  const since = new Date(now.getTime() - days * DAY);
  const previousSince = new Date(since.getTime() - days * DAY);
  const workspace = await db.workspace.findUniqueOrThrow({ where: { id: workspaceId } });

  const [kpis, previousKpis, funnelStages, daily, inbox, upcomingMeetings] = await Promise.all([
    periodKpis(workspaceId, since, null),
    periodKpis(workspaceId, previousSince, since),
    stageCounts({ workspaceId, createdAt: { gte: since } }),
    dailySeries(workspaceId, workspace.timezone, days, now),
    inboxCounts(workspaceId),
    db.meeting.findMany({
      where: { workspaceId, startsAt: { gte: now }, status: "SCHEDULED" },
      include: { prospect: { select: { id: true, firstName: true, lastName: true, company: true } } },
      orderBy: { startsAt: "asc" },
      take: 5,
    }),
  ]);
  const granularity: SeriesGranularity = days > DAILY_MAX_DAYS ? "week" : "day";

  return {
    kpis,
    /** Same KPIs over the window just before, for the delta chips. */
    previousKpis,
    funnel: funnelFromStages(funnelStages),
    granularity,
    series: granularity === "week" ? byWeek(daily) : daily,
    inbox,
    upcomingMeetings,
  };
}

/** Sums days into 7-day columns ending today; only the oldest column can be shorter. */
export function byWeek(points: SeriesPoint[]): SeriesPoint[] {
  const weeks: SeriesPoint[] = [];
  for (let end = points.length; end > 0; end -= 7) {
    const chunk = points.slice(Math.max(0, end - 7), end);
    weeks.unshift(
      chunk.reduce(
        (week, p) => ({ ...week, invites: week.invites + p.invites, messages: week.messages + p.messages, replies: week.replies + p.replies, meetings: week.meetings + p.meetings }),
        { day: chunk[0]!.day, invites: 0, messages: 0, replies: 0, meetings: 0 },
      ),
    );
  }
  return weeks;
}

/** Per-day activity in the workspace's timezone, zero-filled. */
async function dailySeries(workspaceId: string, timezone: string, days: number, now: Date): Promise<SeriesPoint[]> {
  const since = new Date(now.getTime() - days * DAY);
  const rows = await db.$queryRaw<{ day: string; type: string; n: bigint }[]>`
    SELECT to_char(("createdAt" AT TIME ZONE 'UTC') AT TIME ZONE ${timezone}, 'YYYY-MM-DD') AS day, type::text AS type, count(*) AS n
    FROM "Activity"
    WHERE "workspaceId" = ${workspaceId} AND "createdAt" >= ${since}
      AND type IN ('INVITE_SENT', 'MESSAGE_SENT', 'FOLLOW_UP_SENT', 'AI_REPLY_SENT', 'HUMAN_REPLY_SENT', 'REPLY_RECEIVED', 'MEETING_BOOKED')
    GROUP BY 1, 2`;

  const fmt = new Intl.DateTimeFormat("en-CA", { timeZone: timezone, year: "numeric", month: "2-digit", day: "2-digit" });
  const points = new Map<string, SeriesPoint>();
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
