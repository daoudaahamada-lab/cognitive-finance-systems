/** An error whose message is safe and useful to show to the user. */
export class UserError extends Error {}

export type ActionState = { ok?: boolean; error?: string; message?: string; fieldErrors?: Record<string, string> } | null;

export function toActionState(error: unknown): ActionState {
  if (error instanceof UserError) return { error: error.message };
  // Next.js uses thrown errors for redirect()/notFound(): let them through.
  throw error;
}
