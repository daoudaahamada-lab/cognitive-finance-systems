import { RuleBasedScorer, type ProspectScorer } from "./scorer";
import { RuleBasedSetter, type ReplyAgent } from "./setter";
import { TemplateWriter, type MessageWriter } from "./writer";

export type Agents = { scorer: ProspectScorer; writer: MessageWriter; setter: ReplyAgent };

/** Rule-based agents. The LLM-backed versions will be swapped in here. */
export function defaultAgents(): Agents {
  return { scorer: new RuleBasedScorer(), writer: new TemplateWriter(), setter: new RuleBasedSetter() };
}
