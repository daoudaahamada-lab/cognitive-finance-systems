import type { Plan } from "@prisma/client";

export type PlanLimits = {
  label: string;
  /** LinkedIn accounts included in the plan. */
  includedAccounts: number;
  /** Hard ceiling on connected accounts. */
  maxAccounts: number;
  /** New prospects sourced per campaign per rolling week; null = only bounded by invite quotas. */
  weeklyProspects: number | null;
  maxFollowUps: number;
  setter: boolean;
  listImport: boolean;
};

export const PLANS: Record<Plan, PlanLimits> = {
  STARTER: {
    label: "Starter",
    includedAccounts: 1,
    maxAccounts: 1,
    weeklyProspects: 100,
    maxFollowUps: 6,
    setter: false,
    listImport: false,
  },
  PRO: {
    label: "Pro",
    includedAccounts: 1,
    maxAccounts: 1,
    weeklyProspects: null,
    maxFollowUps: 8,
    setter: true,
    listImport: true,
  },
  AGENCY: {
    label: "Agency",
    includedAccounts: 2,
    maxAccounts: 5,
    weeklyProspects: null,
    maxFollowUps: 8,
    setter: true,
    listImport: true,
  },
};

export const TRIAL_DAYS = 14;

export function planLimits(plan: Plan): PlanLimits {
  return PLANS[plan];
}
