"use client";

import { useState, type KeyboardEvent } from "react";
import { cn } from "@/lib/cn";
import { formatNumber } from "@/lib/format";

/** `weekend` shades the column, for daily series. */
export type ColumnPoint = { label: string; value: number; weekend?: boolean };

const HEIGHT = 96;
const decimal = new Intl.NumberFormat("fr-FR", { maximumFractionDigits: 1 });

function niceMax(value: number): number {
  if (value <= 4) return 4;
  const magnitude = 10 ** Math.floor(Math.log10(value));
  for (const step of [1, 2, 2.5, 5, 10]) {
    if (step * magnitude >= value) return step * magnitude;
  }
  return 10 * magnitude;
}

/**
 * Small single-series column chart: one hue, 50 % and 100 % gridlines, a tooltip under the bars.
 * The bars form a single tab stop; arrow keys, Home and End move between them and announce each value.
 * `per` names the period of one column ("j" for days, "sem." for weeks).
 */
export function ColumnChart({ title, points, total, per = "j" }: { title: string; points: ColumnPoint[]; total: number; per?: string }) {
  const [active, setActive] = useState<number | null>(null);
  const [announced, setAnnounced] = useState("");
  const max = niceMax(Math.max(0, ...points.map((p) => p.value)));
  const hovered = active !== null ? points[active] : null;
  const average = points.length ? total / points.length : 0;

  const move = (index: number) => {
    const p = points[index];
    if (!p) return;
    setActive(index);
    setAnnounced(`${p.label} : ${formatNumber(p.value)}`);
  };

  const onKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    const last = points.length - 1;
    const current = active ?? last;
    const next =
      e.key === "ArrowRight" ? Math.min(last, current + 1)
      : e.key === "ArrowLeft" ? Math.max(0, current - 1)
      : e.key === "Home" ? 0
      : e.key === "End" ? last
      : null;
    if (next === null) return;
    e.preventDefault();
    move(next);
  };

  return (
    <figure className="min-w-0">
      <figcaption className="mb-3 flex items-start justify-between gap-2">
        <span className="text-sm text-muted">{title}</span>
        <span className="text-right">
          <span className="block text-lg font-semibold leading-tight text-ink tabular-nums">{formatNumber(total)}</span>
          <span className="block text-2xs text-muted tabular-nums">
            moy. {decimal.format(average)}/{per}
          </span>
        </span>
      </figcaption>
      <div className="relative">
        <div
          role="group"
          tabIndex={0}
          aria-label={`${title}, ${points.length} valeurs. Flèches gauche et droite pour les parcourir.`}
          onKeyDown={onKeyDown}
          onFocus={() => move(active ?? points.length - 1)}
          onBlur={() => setActive(null)}
          onPointerLeave={() => setActive(null)}
          className="relative flex items-end gap-[2px] border-b border-line outline-none focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-600"
          style={{ height: HEIGHT }}
        >
          {points.map((p, i) =>
            p.weekend ? (
              <span key={`we-${p.label}`} aria-hidden className="absolute inset-y-0 bg-canvas" style={{ left: `${(i / points.length) * 100}%`, width: `${100 / points.length}%` }} />
            ) : null,
          )}
          {[1, 0.5].map((level) => (
            <span key={level} aria-hidden className="pointer-events-none absolute inset-x-0 border-t border-dashed border-line" style={{ bottom: level * HEIGHT }} />
          ))}
          {points.map((p, i) => (
            <span key={p.label} aria-hidden onPointerEnter={() => setActive(i)} className="relative flex h-full flex-1 items-end justify-center">
              <span
                className="block w-full max-w-6 rounded-t-[4px] bg-brand-600 transition-opacity"
                style={{ height: p.value === 0 ? 0 : Math.max(2, (p.value / max) * HEIGHT), opacity: active === null || active === i ? 1 : 0.45 }}
              />
            </span>
          ))}
          {[1, 0.5].map((level) => (
            <span
              key={`label-${level}`}
              aria-hidden
              className="pointer-events-none absolute left-0 bg-surface/80 pr-1 text-2xs leading-4 text-muted tabular-nums"
              style={{ top: HEIGHT - level * HEIGHT }}
            >
              {decimal.format(max * level)}
            </span>
          ))}
        </div>
        <span className="sr-only" aria-live="polite">
          {announced}
        </span>
        {hovered ? (
          <div
            aria-hidden
            className={cn(
              "pointer-events-none absolute top-full z-10 mt-1 whitespace-nowrap rounded-md bg-ink px-2 py-1 text-xs text-white shadow-pop",
              active! < points.length / 4 ? "" : active! >= (points.length * 3) / 4 ? "-translate-x-full" : "-translate-x-1/2",
            )}
            style={{ left: `${((active! + 0.5) / points.length) * 100}%` }}
          >
            <strong className="font-semibold">{formatNumber(hovered.value)}</strong> <span className="text-white/70">{hovered.label}</span>
          </div>
        ) : null}
      </div>
      <div aria-hidden className="mt-1 flex justify-between text-2xs text-muted">
        <span>{points[0]?.label}</span>
        <span>{points.at(-1)?.label}</span>
      </div>
    </figure>
  );
}
