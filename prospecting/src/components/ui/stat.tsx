import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { formatDelta } from "@/lib/format";

/** Changes smaller than this read as stable. */
const STABLE = 0.03;

/**
 * KPI tile. `delta` is the relative change against the previous period (0.12 = +12 %, see deltaRatio);
 * null or undefined hides the chip. `lead` highlights the tile that matters most.
 */
export function Stat({
  label,
  value,
  delta,
  deltaLabel = "par rapport à la période précédente",
  hint,
  lead = false,
  className,
}: {
  label: ReactNode;
  value: ReactNode;
  delta?: number | null;
  deltaLabel?: string;
  hint?: ReactNode;
  lead?: boolean;
  className?: string;
}) {
  return (
    <div className={cn("min-w-0 rounded-card border px-4 py-3 shadow-card", lead ? "border-brand-200 bg-brand-50" : "border-line bg-surface", className)}>
      <p className={cn("truncate text-xs", lead ? "text-brand-700" : "text-muted")}>{label}</p>
      <div className="mt-1 flex flex-wrap items-baseline gap-x-2 gap-y-1">
        <p className={cn("text-kpi font-semibold tabular-nums", lead ? "text-brand-900" : "text-ink")}>{value}</p>
        {delta !== undefined && delta !== null ? <DeltaChip delta={delta} label={deltaLabel} /> : null}
      </div>
      {hint ? <p className={cn("mt-0.5 text-2xs", lead ? "text-brand-700" : "text-muted")}>{hint}</p> : null}
    </div>
  );
}

export function DeltaChip({ delta, label }: { delta: number; label?: string }) {
  const stable = Math.abs(delta) < STABLE;
  const Icon = stable ? Minus : delta > 0 ? ArrowUpRight : ArrowDownRight;
  return (
    <span
      title={label}
      className={cn(
        "inline-flex items-center gap-0.5 rounded-md px-1.5 py-0.5 text-2xs font-semibold tabular-nums",
        stable ? "bg-canvas text-ink-2" : delta > 0 ? "bg-success-soft text-success" : "bg-danger-soft text-danger",
      )}
    >
      <Icon className="size-3" aria-hidden />
      {formatDelta(delta)}
      {label ? <span className="sr-only"> {label}</span> : null}
    </span>
  );
}
