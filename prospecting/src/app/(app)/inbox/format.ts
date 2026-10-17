/** Inbox date helpers, safe on server and client. Dates follow the workspace time zone when one is given. */

const MINUTE = 60_000;
const HOUR = 3_600_000;
const DAY = 86_400_000;

/** The time zone if the runtime knows it, else undefined (the runtime's own zone). */
export function safeTimeZone(timeZone?: string | null): string | undefined {
  if (!timeZone) return undefined;
  try {
    new Intl.DateTimeFormat("fr-FR", { timeZone });
    return timeZone;
  } catch {
    return undefined;
  }
}

function calendarDay(date: Date, timeZone?: string): { day: number; year: number } {
  const parts = new Intl.DateTimeFormat("en-CA", { timeZone, year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(date);
  const part = (type: string) => Number(parts.find((p) => p.type === type)?.value);
  const year = part("year");
  return { day: Date.UTC(year, part("month") - 1, part("day")) / DAY, year };
}

/** Compact time for the conversation list: "à l'instant", "59 min", "11 h", "hier", "12 oct." (year added when it differs). */
export function formatCompactTime(date: Date | string | null | undefined, now = new Date(), timeZone?: string | null): string {
  if (!date) return "—";
  const at = new Date(date);
  const diff = now.getTime() - at.getTime();
  if (diff < MINUTE) return "à l'instant";
  if (diff < HOUR) return `${Math.floor(diff / MINUTE)} min`;
  if (diff < DAY) return `${Math.floor(diff / HOUR)} h`;
  const zone = safeTimeZone(timeZone);
  const today = calendarDay(now, zone);
  const then = calendarDay(at, zone);
  if (today.day - then.day <= 1) return "hier";
  return new Intl.DateTimeFormat("fr-FR", {
    timeZone: zone,
    day: "numeric",
    month: "short",
    ...(today.year === then.year ? {} : { year: "numeric" }),
  }).format(at);
}

/** Date and time under a message bubble: "12 oct. 2026, 10:24". */
export function formatMessageTime(date: Date | string, timeZone?: string | null): string {
  return new Intl.DateTimeFormat("fr-FR", { timeZone: safeTimeZone(timeZone), dateStyle: "medium", timeStyle: "short" }).format(new Date(date));
}

/** Full date for tooltips: "vendredi 16 octobre 2026 à 10:24". */
export function formatFullTime(date: Date | string, timeZone?: string | null): string {
  return new Intl.DateTimeFormat("fr-FR", { timeZone: safeTimeZone(timeZone), dateStyle: "full", timeStyle: "short" }).format(new Date(date));
}
