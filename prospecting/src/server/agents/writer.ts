import { INVITE_NOTE_MAX, renderTemplate, type TemplateVars } from "@/server/domain/templates";

export type SequenceStep = { kind: "invite_note" } | { kind: "first_message" } | { kind: "follow_up"; index: number };

/** Writes sequence messages. The AI writer will personalize from the profile; this one renders templates. */
export interface MessageWriter {
  write(template: string, step: SequenceStep, vars: TemplateVars, prospectId: string): string;
}

export class TemplateWriter implements MessageWriter {
  write(template: string, step: SequenceStep, vars: TemplateVars, prospectId: string): string {
    const seed = `${prospectId}:${step.kind}:${"index" in step ? step.index : 0}`;
    const text = renderTemplate(template, vars, seed);
    return step.kind === "invite_note" ? text.slice(0, INVITE_NOTE_MAX) : text;
  }
}
