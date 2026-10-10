import Anthropic from "@anthropic-ai/sdk";
import { betaZodOutputFormat } from "@anthropic-ai/sdk/helpers/beta/zod";
import type * as z from "zod/v4";

/** Model used by every agent; override with ANTHROPIC_MODEL. */
export const CLAUDE_MODEL = process.env.ANTHROPIC_MODEL ?? "claude-opus-5-5";

/**
 * Server-side fallback: if a safety classifier declines a request, the API re-runs it
 * on the model Anthropic recommends for that refusal category, inside the same call.
 */
const FALLBACK_BETA = "server-side-fallback-2026-07-01";

/** The slice of the SDK the agents use, so tests can inject a fake. */
export type ClaudeClient = Pick<Anthropic, "beta">;

let shared: Anthropic | null = null;

export function claudeClient(): ClaudeClient {
  // Credentials come from ANTHROPIC_API_KEY (or the other sources the SDK resolves).
  shared ??= new Anthropic({ timeout: 90_000, maxRetries: 2 });
  return shared;
}

/** Thrown when Claude produced no usable answer; callers fall back to the rule-based agent. */
export class AgentUnavailable extends Error {}

/** After a credentials error, skip Claude for a while instead of failing every single call. */
const CREDENTIALS_PAUSE_MS = 5 * 60_000;
let pausedUntil = 0;

export function resetClaudePause() {
  pausedUntil = 0;
}

type StructuredCall<S extends z.ZodType> = {
  /** Stable instructions: cached across calls. */
  system: string;
  /** Per-request content. */
  input: string;
  schema: S;
  effort: "low" | "medium" | "high";
};

/** One request whose answer is parsed and validated against a Zod schema. */
export async function structuredCall<S extends z.ZodType>(
  client: ClaudeClient,
  { system, input, schema, effort }: StructuredCall<S>,
): Promise<z.infer<S>> {
  if (Date.now() < pausedUntil) throw new AgentUnavailable("Claude paused after a credentials error");
  let response;
  try {
    response = await client.beta.messages.parse({
      model: CLAUDE_MODEL,
      max_tokens: 16000,
      betas: [FALLBACK_BETA],
      fallbacks: "default",
      system: [{ type: "text", text: system, cache_control: { type: "ephemeral" } }],
      output_config: { effort, format: betaZodOutputFormat(schema) },
      messages: [{ role: "user", content: input }],
    });
  } catch (error) {
    if (error instanceof Anthropic.AuthenticationError || error instanceof Anthropic.PermissionDeniedError) {
      pausedUntil = Date.now() + CREDENTIALS_PAUSE_MS;
      console.error(`[agents] Anthropic credentials rejected (${error.status}): Claude paused for 5 minutes, rules in use. Check ANTHROPIC_API_KEY.`);
    }
    throw error;
  }
  if (response.stop_reason === "refusal") {
    throw new AgentUnavailable(`Claude declined (${response.stop_details?.category ?? "no category"})`);
  }
  if (response.stop_reason === "max_tokens") throw new AgentUnavailable("Claude ran out of output tokens");
  if (response.parsed_output === null || response.parsed_output === undefined) {
    throw new AgentUnavailable("Claude's answer did not match the expected format");
  }
  return response.parsed_output;
}

/** Logs why an agent fell back to rules, without failing the engine. */
export function logFallback(agent: string, error: unknown) {
  if (Date.now() < pausedUntil) return; // already reported once
  const reason =
    error instanceof Anthropic.APIError ? `API ${error.status ?? "connection"} error: ${error.message}`
    : error instanceof Error ? error.message
    : String(error);
  console.warn(`[agents] ${agent}: Claude unavailable, using rules (${reason})`);
}
