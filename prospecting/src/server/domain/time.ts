export const MINUTE = 60_000;
export const HOUR = 60 * MINUTE;
export const DAY = 24 * HOUR;
export const WEEK = 7 * DAY;

/**
 * TIME_SCALE speeds up waits (sequence delays, simulated reactions) for demos.
 * It never applies to safety quotas, which always use real time.
 */
export function timeScale(): number {
  const raw = Number(process.env.TIME_SCALE ?? "1");
  return Number.isFinite(raw) && raw >= 1 ? raw : 1;
}

export function scaled(ms: number, scale = timeScale()): number {
  return Math.round(ms / scale);
}

export function addScaled(from: Date, ms: number, scale = timeScale()): Date {
  return new Date(from.getTime() + scaled(ms, scale));
}
