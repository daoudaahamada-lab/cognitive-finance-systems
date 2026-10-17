/** Calendar helpers for meetings and the prospect history, in the workspace time zone. Safe on server and client. */

const DAY = 86_400_000;

/** The time zone if the runtime knows it, else undefined (the runtime's own zone). */
export function knownTimeZone(timeZone?: string | null): string | undefined {
  if (!timeZone) return undefined;
  try {
    new Intl.DateTimeFormat("fr-FR", { timeZone });
    return timeZone;
  } catch {
    return undefined;
  }
}

function parts(date: Date, timeZone?: string) {
  const values = new Intl.DateTimeFormat("en-CA", { timeZone, year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(date);
  const get = (type: string) => Number(values.find((p) => p.type === type)?.value);
  return { year: get("year"), month: get("month"), day: get("day") };
}

/** Calendar day of `date` in the zone, as "2026-10-19": the key used to group by day. */
export function dayKey(date: Date, timeZone?: string | null): string {
  const { year, month, day } = parts(date, knownTimeZone(timeZone));
  return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
}

function dayNumber(date: Date, timeZone?: string): number {
  const { year, month, day } = parts(date, timeZone);
  return Date.UTC(year, month - 1, day) / DAY;
}

/** "Aujourd'hui", "Demain", "Hier", else "lun. 19 oct." (the year is added when it differs from now). */
export function dayLabel(date: Date, now = new Date(), timeZone?: string | null): string {
  const zone = knownTimeZone(timeZone);
  const offset = dayNumber(date, zone) - dayNumber(now, zone);
  if (offset === 0) return "Aujourd'hui";
  if (offset === 1) return "Demain";
  if (offset === -1) return "Hier";
  const sameYear = parts(date, zone).year === parts(now, zone).year;
  return new Intl.DateTimeFormat("fr-FR", { timeZone: zone, weekday: "short", day: "numeric", month: "short", ...(sameYear ? {} : { year: "numeric" }) }).format(date);
}

/** "14:30". */
export function formatTime(date: Date, timeZone?: string | null): string {
  return new Intl.DateTimeFormat("fr-FR", { timeZone: knownTimeZone(timeZone), hour: "2-digit", minute: "2-digit" }).format(date);
}

/** "19 oct. 2026, 14:30". */
export function formatDateTimeIn(date: Date | null | undefined, timeZone?: string | null): string {
  if (!date) return "—";
  return new Intl.DateTimeFormat("fr-FR", { timeZone: knownTimeZone(timeZone), dateStyle: "medium", timeStyle: "short" }).format(date);
}

/** Day number and short month for a calendar-style date block: { day: "19", month: "oct." }. */
export function dateBlock(date: Date, timeZone?: string | null): { day: string; month: string } {
  const zone = knownTimeZone(timeZone);
  return {
    day: new Intl.DateTimeFormat("fr-FR", { timeZone: zone, day: "numeric" }).format(date),
    month: new Intl.DateTimeFormat("fr-FR", { timeZone: zone, month: "short" }).format(date),
  };
}

export type DayGroup<T> = { key: string; label: string; items: T[] };

/** Groups items by calendar day, keeping their order (sort them first). */
export function groupByDay<T>(items: T[], dateOf: (item: T) => Date, now = new Date(), timeZone?: string | null): DayGroup<T>[] {
  const groups: DayGroup<T>[] = [];
  for (const item of items) {
    const date = dateOf(item);
    const key = dayKey(date, timeZone);
    const last = groups.at(-1);
    if (last?.key === key) last.items.push(item);
    else groups.push({ key, label: dayLabel(date, now, timeZone), items: [item] });
  }
  return groups;
}
