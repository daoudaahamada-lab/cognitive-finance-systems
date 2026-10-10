import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { hashColor } from "@/lib/colors";
import { initials } from "@/lib/format";

export function PageHeader({ title, description, actions }: { title: ReactNode; description?: ReactNode; actions?: ReactNode }) {
  return (
    <header className="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div className="min-w-0">
        <h1 className="text-xl font-semibold tracking-tight text-ink">{title}</h1>
        {description ? <p className="mt-1 max-w-2xl text-sm text-muted">{description}</p> : null}
      </div>
      {actions ? <div className="flex flex-wrap items-center gap-2">{actions}</div> : null}
    </header>
  );
}

export function EmptyState({ icon, title, description, action }: { icon?: ReactNode; title: string; description?: string; action?: ReactNode }) {
  return (
    <div className="flex flex-col items-center px-6 py-14 text-center">
      {icon ? <div className="mb-3 flex size-10 items-center justify-center rounded-full bg-brand-50 text-brand-600">{icon}</div> : null}
      <p className="text-sm font-semibold text-ink">{title}</p>
      {description ? <p className="mt-1 max-w-sm text-sm text-muted">{description}</p> : null}
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}

export function Avatar({ first, last, size = "md" }: { first: string; last?: string; size?: "sm" | "md" | "lg" }) {
  const sizes = { sm: "size-7 text-[11px]", md: "size-9 text-xs", lg: "size-14 text-base" };
  return (
    <span
      aria-hidden
      className={cn("inline-flex shrink-0 items-center justify-center rounded-full font-semibold text-white", sizes[size])}
      style={{ backgroundColor: hashColor(`${first} ${last ?? ""}`) }}
    >
      {initials(first, last)}
    </span>
  );
}

export function Meter({ value, max, label }: { value: number; max: number; label: string }) {
  const ratio = max > 0 ? Math.min(1, value / max) : 1;
  const tone = ratio >= 1 ? "bg-amber-500" : "bg-brand-600";
  return (
    <div>
      <div className="mb-1 flex justify-between text-xs">
        <span className="text-muted">{label}</span>
        <span className="font-medium tabular-nums text-ink">
          {value} / {max}
        </span>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-zinc-100" role="meter" aria-valuenow={value} aria-valuemin={0} aria-valuemax={max} aria-label={label}>
        <div className={cn("h-full rounded-full", tone)} style={{ width: `${ratio * 100}%` }} />
      </div>
    </div>
  );
}

export function ScorePill({ score }: { score: number | null }) {
  if (score === null) return <span className="text-xs text-muted">—</span>;
  const tone = score >= 75 ? "text-emerald-700 bg-emerald-50" : score >= 50 ? "text-amber-800 bg-amber-50" : "text-zinc-600 bg-zinc-100";
  return <span className={cn("inline-flex min-w-9 justify-center rounded-md px-1.5 py-0.5 text-xs font-semibold tabular-nums", tone)}>{score}</span>;
}
