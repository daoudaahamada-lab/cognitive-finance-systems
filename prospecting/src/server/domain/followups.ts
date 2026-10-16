import { z } from "zod";

export const followUpStepSchema = z.object({
  delayDays: z.number().int().min(1).max(30),
  template: z.string().transform((v) => v.replace(/\r\n?/g, "\n").trim()).pipe(z.string().min(1).max(2000)),
});

export const MAX_FOLLOW_UPS = 8;

export const followUpsSchema = z.array(followUpStepSchema).max(MAX_FOLLOW_UPS, `${MAX_FOLLOW_UPS} relances au maximum`);

export type FollowUpStep = z.infer<typeof followUpStepSchema>;

/** Reads the JSON column defensively: bad rows yield no follow-ups rather than a crash. */
export function parseFollowUps(value: unknown): FollowUpStep[] {
  const parsed = followUpsSchema.safeParse(value);
  return parsed.success ? parsed.data : [];
}

/** Days to wait after the last follow-up before marking a prospect unresponsive. */
export const FINAL_WAIT_DAYS = 7;

/** Pause between an accepted invitation and the first message (the engine's FIRST_MESSAGE_DELAY). */
export const FIRST_MESSAGE_DELAY_HOURS = 4;

export type SequenceStepTiming = {
  /** 1-based follow-up number: "Relance 1" has index 1. */
  index: number;
  /** Days after the previous message (the first message for index 1). */
  afterPrevDays: number;
  /** Days after the first message (J+N): delays add up, each one counts from the previous message. */
  dayFromFirst: number;
};

/** When each follow-up goes out, counted from the first message. */
export function sequenceTimeline(followUps: Pick<FollowUpStep, "delayDays">[]): SequenceStepTiming[] {
  let day = 0;
  return followUps.map((step, i) => {
    day += step.delayDays;
    return { index: i + 1, afterPrevDays: step.delayDays, dayFromFirst: day };
  });
}

/** Day (from the first message) when a prospect who never answered is marked unresponsive. */
export function sequenceEndDay(followUps: Pick<FollowUpStep, "delayDays">[]): number {
  return (sequenceTimeline(followUps).at(-1)?.dayFromFirst ?? 0) + FINAL_WAIT_DAYS;
}
