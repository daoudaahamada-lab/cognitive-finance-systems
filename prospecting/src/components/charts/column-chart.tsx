"use client";

import { useState } from "react";

export type ColumnPoint = { label: string; value: number };

const HEIGHT = 96;

function niceMax(value: number): number {
  if (value <= 4) return 4;
  const magnitude = 10 ** Math.floor(Math.log10(value));
  for (const step of [1, 2, 2.5, 5, 10]) {
    if (step * magnitude >= value) return step * magnitude;
  }
  return 10 * magnitude;
}

/** Small single-series column chart: one hue, 4px rounded caps, 2px gaps, per-column tooltip. */
export function ColumnChart({ title, points, total }: { title: string; points: ColumnPoint[]; total: number }) {
  const [active, setActive] = useState<number | null>(null);
  const max = niceMax(Math.max(0, ...points.map((p) => p.value)));
  const hovered = active !== null ? points[active] : null;

  return (
    <figure className="min-w-0">
      <figcaption className="mb-2 flex items-baseline justify-between gap-2">
        <span className="text-sm text-muted">{title}</span>
        <span className="text-lg font-semibold text-ink">{total}</span>
      </figcaption>
      <div className="relative">
        <div className="pointer-events-none absolute inset-x-0 top-0 border-t border-line" />
        <span className="pointer-events-none absolute -top-2 right-0 bg-surface pl-1 text-[10px] text-muted tabular-nums">{max}</span>
        <div className="flex items-end gap-[2px] border-b border-line" style={{ height: HEIGHT }}>
          {points.map((p, i) => (
            <button
              key={p.label}
              type="button"
              className="group flex h-full flex-1 items-end justify-center outline-none"
              onPointerEnter={() => setActive(i)}
              onPointerLeave={() => setActive(null)}
              onFocus={() => setActive(i)}
              onBlur={() => setActive(null)}
              aria-label={`${p.label} : ${p.value}`}
            >
              <span
                className="block w-full max-w-6 rounded-t-[4px] bg-brand-600 transition-opacity group-focus-visible:ring-2 group-focus-visible:ring-brand-500/40"
                style={{ height: p.value === 0 ? 0 : Math.max(2, (p.value / max) * HEIGHT), opacity: active === null || active === i ? 1 : 0.45 }}
              />
            </button>
          ))}
        </div>
        {hovered ? (
          <div
            role="tooltip"
            className="pointer-events-none absolute -top-9 z-10 -translate-x-1/2 whitespace-nowrap rounded-md bg-ink px-2 py-1 text-xs text-white shadow"
            style={{ left: `${((active! + 0.5) / points.length) * 100}%` }}
          >
            <strong className="font-semibold">{hovered.value}</strong> <span className="text-white/70">{hovered.label}</span>
          </div>
        ) : null}
      </div>
      <div className="mt-1 flex justify-between text-[10px] text-muted">
        <span>{points[0]?.label}</span>
        <span>{points.at(-1)?.label}</span>
      </div>
    </figure>
  );
}
