export type SendingWindow = {
  timezone: string;
  /** ISO weekdays, 1 = Monday ... 7 = Sunday. */
  sendingDays: number[];
  /** "HH:MM" local time, inclusive. */
  sendingStart: string;
  /** "HH:MM" local time, exclusive. Equal to the start means all day. */
  sendingEnd: string;
};

const WEEKDAYS: Record<string, number> = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 };

export function parseHourMinute(value: string): number {
  const match = /^(\d{1,2}):(\d{2})$/.exec(value.trim());
  if (!match) throw new Error(`Invalid time "${value}", expected HH:MM`);
  const hours = Number(match[1]);
  const minutes = Number(match[2]);
  if (hours > 24 || minutes > 59 || (hours === 24 && minutes > 0)) {
    throw new Error(`Invalid time "${value}"`);
  }
  return hours * 60 + minutes;
}

export function localParts(date: Date, timezone: string): { weekday: number; minutes: number } {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: timezone,
    weekday: "short",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(date);
  const get = (type: string) => parts.find((p) => p.type === type)?.value ?? "";
  const weekday = WEEKDAYS[get("weekday")];
  if (!weekday) throw new Error(`Cannot read weekday for timezone ${timezone}`);
  return { weekday, minutes: Number(get("hour")) * 60 + Number(get("minute")) };
}

/** Length of the daily sending window in minutes (same start and end: all day). */
export function sendingWindowMinutes(window: Pick<SendingWindow, "sendingStart" | "sendingEnd">): number {
  const start = parseHourMinute(window.sendingStart);
  const end = parseHourMinute(window.sendingEnd);
  return start === end ? 24 * 60 : (end - start + 24 * 60) % (24 * 60);
}

export function isWithinSendingWindow(window: SendingWindow, at: Date): boolean {
  const { weekday, minutes } = localParts(at, window.timezone);
  if (!window.sendingDays.includes(weekday)) return false;
  const start = parseHourMinute(window.sendingStart);
  const end = parseHourMinute(window.sendingEnd);
  if (start === end) return true;
  // Windows may wrap past midnight (e.g. 22:00 to 02:00).
  return start < end ? minutes >= start && minutes < end : minutes >= start || minutes < end;
}

export function isValidTimezone(timezone: string): boolean {
  try {
    new Intl.DateTimeFormat("en-US", { timeZone: timezone });
    return true;
  } catch {
    return false;
  }
}
