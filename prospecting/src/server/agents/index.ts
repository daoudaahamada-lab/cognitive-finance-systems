import { ClaudeScorer } from "./claude/scorer";
import { ClaudeSetter } from "./claude/setter";
import { ClaudeWriter } from "./claude/writer";
import { CLAUDE_MODEL, claudeClient, type ClaudeClient } from "./claude/client";
import { RuleBasedScorer, type ProspectScorer } from "./scorer";
import { RuleBasedSetter, type ReplyAgent } from "./setter";
import { TemplateWriter, type MessageWriter } from "./writer";

export type Agents = { scorer: ProspectScorer; writer: MessageWriter; setter: ReplyAgent };

export type AgentMode = "claude" | "rules";

/** AGENTS=claude|rules; without it, Claude is used whenever an API key is configured. */
export function agentMode(): AgentMode {
  const explicit = process.env.AGENTS?.trim().toLowerCase();
  if (explicit === "claude" || explicit === "rules") return explicit;
  return process.env.ANTHROPIC_API_KEY ? "claude" : "rules";
}

export function agentLabel(): string {
  return agentMode() === "claude" ? `Claude (${CLAUDE_MODEL})` : "règles";
}

export function ruleAgents(): Agents {
  return { scorer: new RuleBasedScorer(), writer: new TemplateWriter(), setter: new RuleBasedSetter() };
}

/** Claude agents fall back to the rule-based ones request by request, so the engine never stalls. */
export function claudeAgents(client: ClaudeClient = claudeClient()): Agents {
  return { scorer: new ClaudeScorer(client), writer: new ClaudeWriter(client), setter: new ClaudeSetter(client) };
}

export function defaultAgents(): Agents {
  return agentMode() === "claude" ? claudeAgents() : ruleAgents();
}
