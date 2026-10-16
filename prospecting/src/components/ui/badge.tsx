import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import type { Tone } from "@/lib/labels";
import { toneClasses } from "@/lib/tones";

export function Badge({ tone = "neutral", className, children }: { tone?: Tone; className?: string; children: ReactNode }) {
  return (
    <span className={cn("inline-flex items-center gap-1 rounded-md px-2 py-0.5 text-xs font-medium ring-1 ring-inset whitespace-nowrap", toneClasses(tone).badge, className)}>
      {children}
    </span>
  );
}

export function LabeledBadge({ map, value }: { map: Record<string, { label: string; tone: Tone }>; value: string }) {
  const entry = map[value] ?? { label: value, tone: "neutral" as const };
  return <Badge tone={entry.tone}>{entry.label}</Badge>;
}

/** Small status dot; pass a label when no visible text says the same thing. */
export function Dot({ tone = "neutral", label, className }: { tone?: Tone; label?: string; className?: string }) {
  return (
    <span className={cn("inline-block size-2 shrink-0 rounded-full", toneClasses(tone).fill, className)} role={label ? "img" : undefined} aria-label={label} aria-hidden={label ? undefined : true} />
  );
}
