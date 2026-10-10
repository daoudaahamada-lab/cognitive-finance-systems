import type { ClaudeClient } from "@/server/agents/claude/client";

export type FakeCall = {
  model: string;
  betas?: string[];
  fallbacks?: unknown;
  system: { text: string; cache_control?: unknown }[];
  output_config: { effort?: string };
  messages: { content: string }[];
};

type Responder = (call: FakeCall) => unknown | Promise<unknown>;

/** Stands in for the SDK: records every request and answers with `respond`'s parsed output. */
export function fakeClaude(respond: Responder, stopReason = "end_turn") {
  const calls: FakeCall[] = [];
  const client = {
    beta: {
      messages: {
        parse: async (params: FakeCall) => {
          calls.push(params);
          const parsed = await respond(params);
          return { stop_reason: stopReason, stop_details: stopReason === "refusal" ? { category: "cyber" } : null, parsed_output: parsed, content: [] };
        },
      },
    },
  } as unknown as ClaudeClient;
  return { client, calls, input: (i = calls.length - 1) => calls[i]!.messages[0]!.content };
}

export function failingClaude() {
  return fakeClaude(() => {
    throw new Error("network down");
  });
}
