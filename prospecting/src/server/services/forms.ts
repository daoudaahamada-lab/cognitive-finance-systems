import type { z } from "zod";
import type { ActionState } from "./errors";

/** Validates form data; on failure returns an ActionState with per-field messages. */
export function parseForm<S extends z.ZodType>(schema: S, data: unknown): { data: z.infer<S> } | { state: ActionState } {
  const parsed = schema.safeParse(data);
  if (parsed.success) return { data: parsed.data };
  const fieldErrors: Record<string, string> = {};
  for (const issue of parsed.error.issues) {
    const key = String(issue.path[0] ?? "form");
    fieldErrors[key] ??= issue.message;
  }
  return { state: { error: "Certains champs sont invalides.", fieldErrors } };
}
