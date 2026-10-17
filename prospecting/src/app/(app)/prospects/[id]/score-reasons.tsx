import { cn } from "@/lib/cn";
import type { ScoreReason } from "@/server/agents/scorer";

/**
 * One criterion of 'Pourquoi ce score': the label, a 120px track filled to points / max, then "x / y".
 * A full criterion fills in success; one worth nothing darkens the whole track (line-strong), since an empty
 * fill would look like the pale track of a criterion not scored yet. AI reasons have no scale: favourable or not.
 */
export function ReasonRow({ reason }: { reason: ScoreReason }) {
  const { label, points, max } = reason;
  if (!max) {
    return (
      <li className="flex items-center justify-between gap-3 py-2">
        <span className={points > 0 ? "text-ink" : "text-muted"}>{label}</span>
        <span className={cn("shrink-0", points > 0 ? "text-success" : "text-muted")}>{points > 0 ? "Favorable" : "Défavorable"}</span>
      </li>
    );
  }
  const ratio = Math.min(1, Math.max(0, points / max));
  return (
    <li className="flex items-center gap-3 py-2">
      <span className={cn("min-w-0 flex-1", points <= 0 ? "text-muted" : "text-ink")}>{label}</span>
      <span
        aria-hidden
        className={cn(
          "h-1.5 w-20 shrink-0 overflow-hidden rounded-full ring-1 ring-line ring-inset sm:w-[120px]",
          ratio <= 0 ? "bg-line-strong" : "bg-surface-2",
        )}
      >
        <span className={cn("block h-full rounded-full", ratio >= 1 ? "bg-success" : "bg-brand-600")} style={{ width: `${ratio * 100}%` }} />
      </span>
      <span className="min-w-14 shrink-0 text-right whitespace-nowrap tabular-nums text-muted">
        {points} / {max}
      </span>
    </li>
  );
}
