import { INVITE_NOTE_MAX, renderTemplate, type TemplateVars } from "@/server/domain/templates";

export type SequenceStep = { kind: "invite_note" } | { kind: "first_message" } | { kind: "follow_up"; index: number };

export type WriteInput = {
  template: string;
  step: SequenceStep;
  vars: TemplateVars;
  prospectId: string;
  /** Facts an AI writer may draw on; it must not invent anything beyond them. */
  profile: { headline: string; title: string; company: string; industry: string; location: string; signal: string | null; signalDetail: string | null };
  offer: string;
  /** Campaign setting: false sends the rendered template as written. */
  personalize: boolean;
};

/** Writes sequence messages (invitation note, first message, follow-ups). */
export interface MessageWriter {
  write(input: WriteInput): Promise<string>;
}

/** The template with variables and spintax resolved; stable for a given prospect and step. */
export function renderStep({ template, step, vars, prospectId }: Pick<WriteInput, "template" | "step" | "vars" | "prospectId">): string {
  const seed = `${prospectId}:${step.kind}:${"index" in step ? step.index : 0}`;
  const text = renderTemplate(template, vars, seed);
  return step.kind === "invite_note" ? text.slice(0, INVITE_NOTE_MAX) : text;
}

export class TemplateWriter implements MessageWriter {
  async write(input: WriteInput): Promise<string> {
    return renderStep(input);
  }
}
