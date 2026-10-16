import { cn } from "@/lib/cn";
import { formatNumber } from "@/lib/format";

export type FunnelStep = { label: string; value: number };

function conversion(steps: FunnelStep[], i: number): number | null {
  const prev = i > 0 ? steps[i - 1]!.value : 0;
  return prev > 0 ? Math.round((steps[i]!.value / prev) * 100) : null;
}

/**
 * Horizontal funnel: one hue (magnitude), the last step in success, and the step-to-step
 * conversion always visible. Screen readers get the same figures as a table.
 */
export function FunnelChart({ steps }: { steps: FunnelStep[] }) {
  const max = Math.max(1, ...steps.map((s) => s.value));

  return (
    <div className="min-w-0">
      <ul aria-hidden className="space-y-2.5">
        {steps.map((step, i) => {
          const rate = conversion(steps, i);
          const width = step.value === 0 ? 0 : Math.max(2, (step.value / max) * 100);
          return (
            <li
              key={step.label}
              className="grid grid-cols-[88px_minmax(0,1fr)_44px_44px] items-center gap-2 sm:grid-cols-[130px_minmax(0,1fr)_56px_64px] sm:gap-3"
            >
              <span className="truncate text-sm text-muted">{step.label}</span>
              <span className="h-3.5 overflow-hidden rounded-full bg-canvas">
                <span
                  className={cn("block h-full rounded-full", i === steps.length - 1 ? "bg-success" : "bg-brand-500")}
                  style={{ width: `${width}%` }}
                />
              </span>
              <span className="text-right text-sm font-medium text-ink tabular-nums">{formatNumber(step.value)}</span>
              <span className="text-right text-xs text-muted tabular-nums">{i === 0 ? "—" : rate === null ? "—" : `${rate} %`}</span>
            </li>
          );
        })}
      </ul>
      <p aria-hidden className="mt-3 text-right text-2xs text-muted">
        % : part de l&apos;étape précédente
      </p>
      {/* The wrapper clips: a table ignores width: 1px and would widen the page. */}
      <div className="sr-only">
        <table>
          <thead>
            <tr>
              <th>Étape</th>
              <th>Prospects</th>
              <th>Conversion depuis l&apos;étape précédente</th>
            </tr>
          </thead>
          <tbody>
            {steps.map((s, i) => {
              const rate = conversion(steps, i);
              return (
                <tr key={s.label}>
                  <td>{s.label}</td>
                  <td>{formatNumber(s.value)}</td>
                  <td>{rate === null ? "—" : `${rate} %`}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
