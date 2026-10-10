const dateTime = new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" });
const dateOnly = new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium" });
const relative = new Intl.RelativeTimeFormat("fr-FR", { numeric: "auto" });

export function formatDateTime(date: Date | string | null | undefined): string {
  return date ? dateTime.format(new Date(date)) : "—";
}

export function formatDate(date: Date | string | null | undefined): string {
  return date ? dateOnly.format(new Date(date)) : "—";
}

export function formatRelative(date: Date | string | null | undefined, now = new Date()): string {
  if (!date) return "—";
  const diff = new Date(date).getTime() - now.getTime();
  const abs = Math.abs(diff);
  if (abs < 60_000) return "à l'instant";
  if (abs < 3_600_000) return relative.format(Math.round(diff / 60_000), "minute");
  if (abs < 86_400_000) return relative.format(Math.round(diff / 3_600_000), "hour");
  return relative.format(Math.round(diff / 86_400_000), "day");
}

export function formatPercent(value: number | null): string {
  return value === null ? "—" : `${Math.round(value * 100)} %`;
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("fr-FR").format(value);
}

export function initials(first: string, last = ""): string {
  return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase();
}

/** Whole days from now until `date` (negative once passed). */
export function daysUntil(date: Date, now = new Date()): number {
  return Math.ceil((date.getTime() - now.getTime()) / 86_400_000);
}
