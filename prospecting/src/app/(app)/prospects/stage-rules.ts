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

/** A meeting agreed outside Vela can be logged until one is booked. */
export function canLogMeeting(stage: string): boolean {
  return stage !== "MEETING_BOOKED";
}
