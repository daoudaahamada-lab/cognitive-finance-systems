import Link from "next/link";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { formatNumber } from "@/lib/format";

export type SegmentItem = {
  href: string;
  label: ReactNode;
  count?: number;
  /** Compared with `value`; defaults to href. */
  value?: string;
  icon?: ReactNode;
};

/**
 * Link-based tabs (view switches, periods, inbox tabs). `fill` gives every item the same width;
 * `stacked` puts the count under the label instead of beside it.
 */
export function SegmentedControl({
  items,
  value,
  label,
  fill = false,
  stacked = false,
  className,
}: {
  items: SegmentItem[];
  value: string;
  label: string;
  fill?: boolean;
  stacked?: boolean;
  className?: string;
}) {
  return (
    <div
      role="group"
      aria-label={label}
      className={cn(
        fill ? "grid w-full auto-cols-fr grid-flow-col" : "inline-flex max-w-full",
        "gap-1 rounded-control border border-line bg-surface-2 p-1",
        className,
      )}
    >
      {items.map((item) => {
        const active = (item.value ?? item.href) === value;
        return (
          <Link
            key={item.href}
            href={item.href}
            aria-current={active ? "page" : undefined}
            className={cn(
              "flex min-w-0 items-center justify-center gap-1.5 rounded-md px-3 py-1.5 text-sm font-medium whitespace-nowrap transition-colors pointer-coarse:min-h-11",
              "focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-brand-600",
              stacked && "flex-col gap-0 px-2 py-1 leading-tight",
              active ? "bg-surface text-ink shadow-card ring-1 ring-line" : "text-muted hover:text-ink",
            )}
          >
            {item.icon}
            <span className="truncate">{item.label}</span>
            {item.count !== undefined ? (
              <span
                className={cn(
                  "text-2xs font-semibold tabular-nums",
                  !stacked && "rounded-full px-1.5",
                  !stacked && (active ? "bg-brand-50 text-brand-700" : "bg-line text-ink-2"),
                  stacked && (active ? "text-brand-700" : "text-muted"),
                )}
              >
                {formatNumber(item.count)}
              </span>
            ) : null}
          </Link>
        );
      })}
    </div>
  );
}
