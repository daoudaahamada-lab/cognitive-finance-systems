import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import type { Tone } from "@/lib/labels";

const TONES: Record<Tone, string> = {
  gray: "bg-zinc-100 text-zinc-700 ring-zinc-200",
  blue: "bg-sky-50 text-sky-800 ring-sky-200",
  indigo: "bg-brand-50 text-brand-700 ring-brand-200",
  violet: "bg-violet-50 text-violet-800 ring-violet-200",
  green: "bg-emerald-50 text-emerald-800 ring-emerald-200",
  amber: "bg-amber-50 text-amber-800 ring-amber-200",
  red: "bg-red-50 text-red-700 ring-red-200",
};

export function Badge({ tone = "gray", className, children }: { tone?: Tone; className?: string; children: ReactNode }) {
  return (
    <span className={cn("inline-flex items-center gap-1 rounded-md px-2 py-0.5 text-xs font-medium ring-1 ring-inset whitespace-nowrap", TONES[tone], className)}>
      {children}
    </span>
  );
}

export function LabeledBadge({ map, value }: { map: Record<string, { label: string; tone: Tone }>; value: string }) {
  const entry = map[value] ?? { label: value, tone: "gray" as const };
  return <Badge tone={entry.tone}>{entry.label}</Badge>;
}
