/**
 * Public prices shown on the marketing site. Placeholders to adjust before launch;
 * plan limits themselves live in src/server/domain/plans.ts.
 */
export const PRICING = {
  currency: "€",
  /** Discount applied to annual billing, as a fraction. */
  annualDiscount: 0.2,
  monthly: { STARTER: 49, PRO: 99, AGENCY: 179 },
  /** Agency: price per LinkedIn account beyond the included ones. */
  extraAccount: 79,
  trialDays: 14,
} as const;

export function annualMonthlyPrice(monthly: number): number {
  return Math.round(monthly * (1 - PRICING.annualDiscount));
}
