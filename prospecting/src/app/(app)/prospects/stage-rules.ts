/** Which controls of the prospect page apply to a stage. Client-safe: the page and its client buttons share it. */

import type { ManualStageAction } from "@/server/services/prospects";

/** Manual stage changes offered for a stage (the service checks them again). */
export function manualStageActions(stage: string): ManualStageAction[] {
  const actions: ManualStageAction[] = [];
  if (["NEW", "QUALIFIED", "INVITED"].includes(stage)) actions.push("exclude");
  if (stage === "DISQUALIFIED") actions.push("requalify");
  if (!["NOT_INTERESTED", "DISQUALIFIED", "MEETING_BOOKED"].includes(stage)) actions.push("not_interested");
  return actions;
}

/** Stages where the engine still has invitations or follow-ups to send, so suspending them means something. */
export const SNOOZABLE_STAGES = ["NEW", "QUALIFIED", "INVITED", "CONNECTED", "MESSAGED"];

export function canSnooze(stage: string): boolean {
  return SNOOZABLE_STAGES.includes(stage);
}

/**
 * The 'Suspendre les envois' block, or null where it does not apply. A snooze still running on a later stage
 * (MCP can set one anywhere) is not shown there, since nothing reads it; it shows again, with
 * 'Reprendre maintenant', if the prospect returns to a stage where sends resume.
 */
export function snoozeControl(stage: string, snoozedUntil: Date | null, now: Date): { until: Date | null } | null {
  if (!canSnooze(stage)) return null;
  return { until: snoozedUntil !== null && snoozedUntil > now ? snoozedUntil : null };
}

/** A meeting agreed outside Vela can be logged until one is booked. */
export function canLogMeeting(stage: string): boolean {
  return stage !== "MEETING_BOOKED";
}
