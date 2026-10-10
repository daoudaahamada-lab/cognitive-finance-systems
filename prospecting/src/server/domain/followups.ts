import { z } from "zod";

export const followUpStepSchema = z.object({
  delayDays: z.number().int().min(1).max(30),
  template: z.string().transform((v) => v.replace(/\r\n?/g, "\n").trim()).pipe(z.string().min(1).max(2000)),
});

export const followUpsSchema = z.array(followUpStepSchema).max(8);

export type FollowUpStep = z.infer<typeof followUpStepSchema>;

/** Reads the JSON column defensively: bad rows yield no follow-ups rather than a crash. */
export function parseFollowUps(value: unknown): FollowUpStep[] {
  const parsed = followUpsSchema.safeParse(value);
  return parsed.success ? parsed.data : [];
}

/** Days to wait after the last follow-up before marking a prospect unresponsive. */
export const FINAL_WAIT_DAYS = 7;
