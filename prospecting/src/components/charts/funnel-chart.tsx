"use client";

import { useState } from "react";
import { formatNumber } from "@/lib/format";

export type FunnelStep = { label: string; value: number };

/**
 * Horizontal funnel: one hue (magnitude), value at the bar tip,
 * step-to-step conversion on hover/focus and in the table view.
 */
export function FunnelChart({ steps }: { steps: FunnelStep[] }) {
  const [active, setActive] = useState<number | null>(null);
  const max = Math.max(1, ...steps.map((s) => s.value));

  return (
    <div>
      <ul className="space-y-3">
        {steps.map((step, i) => {
          const prev = i > 0 ? steps[i - 1]!.value : null;
          const conversion = prev ? Math.round((step.value / prev) * 100) : null;
          const width = step.value === 0 ? 0 : Math.max(1.5, (step.value / max) * 100);
          return (
            <li
              key={step.label}
              tabIndex={0}
              onPointerEnter={() => setActive(i)}
              onPointerLeave={() => setActive(null)}
              onFocus={() => setActive(i)}
              onBlur={() => setActive(null)}
              className="group grid grid-cols-[110px_1fr] items-center gap-3 rounded-md outline-none focus-visible:ring-2 focus-visible:ring-brand-500/40 sm:grid-cols-[140px_1fr]"
              aria-label={`${step.label} : ${step.value}${conversion !== null ? `, ${conversion} % de l'étape précédente` : ""}`}
            >
              <span className="truncate text-sm text-muted">{step.label}</span>
              <div className="relative flex h-6 items-center">
                <div
                  className="h-5 rounded-r-[4px] bg-brand-600 transition-opacity"
                  style={{ width: `${width}%`, opacity: active === null || active === i ? 1 : 0.45 }}
                />
                <span className="ml-2 text-sm font-medium text-ink tabular-nums">{formatNumber(step.value)}</span>
                {active === i && conversion !== null ? (
                  <span className="ml-2 rounded-md bg-ink px-2 py-0.5 text-xs text-white">
                    <strong className="font-semibold">{conversion} %</strong> <span className="text-white/70">de l&apos;étape précédente</span>
                  </span>
                ) : null}
              </div>
            </li>
          );
        })}
      </ul>
      <details className="mt-4 text-xs text-muted">
        <summary className="cursor-pointer select-none hover:text-ink">Voir le tableau</summary>
        <table className="data-table mt-2">
          <thead>
            <tr>
              <th>Étape</th>
              <th className="text-right">Prospects</th>
              <th className="text-right">Conversion</th>
            </tr>
          </thead>
          <tbody>
            {steps.map((s, i) => {
              const prev = i > 0 ? steps[i - 1]!.value : null;
              return (
                <tr key={s.label}>
                  <td>{s.label}</td>
                  <td className="text-right tabular-nums">{formatNumber(s.value)}</td>
                  <td className="text-right tabular-nums">{prev ? `${Math.round((s.value / prev) * 100)} %` : "—"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </details>
    </div>
  );
}
