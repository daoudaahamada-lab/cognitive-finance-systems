/** Client-safe helpers for the reply box and the "RDV pris" form. */

/** Inserts `text` over the selection [start, end), adding a space on each side when it would touch a word. */
export function insertAt(value: string, start: number, end: number, text: string): { value: string; caret: number } {
  const before = value.slice(0, start);
  const after = value.slice(end);
  const lead = before && !/[\s(«"']$/.test(before) ? " " : "";
  const trail = after && !/^[\s.,;:!?)»]/.test(after) ? " " : "";
  const inserted = `${lead}${text}${trail}`;
  return { value: `${before}${inserted}${after}`, caret: before.length + lead.length + text.length };
}

export type ProposalChange = { mode: "proposal" | "reply"; body: string; newProposal: boolean; adopted: boolean };

/**
 * What the reply box does when the pending proposal changes underneath it (the setter drafts again, "Refuser", a refresh).
 * It adopts the new proposal (or empties for a plain reply) unless it holds text of the user's own:
 * that text, or their edit of a proposal that no longer exists, is kept to send as their reply.
 */
export function proposalChange(input: { body: string; previous: { body: string } | null; next: { body: string } | null; refused: boolean }): ProposalChange {
  const untouched = !input.body.trim() || input.body === input.previous?.body;
  if (untouched || (input.refused && !input.next)) {
    return { mode: input.next ? "proposal" : "reply", body: input.next?.body ?? "", newProposal: false, adopted: true };
  }
  return { mode: "reply", body: input.body, newProposal: input.next !== null, adopted: false };
}

const pad = (n: number) => String(n).padStart(2, "0");

/** datetime-local value (local time) for the next business day (Monday to Friday) at 10:00. */
export function nextBusinessDayAt10(now: Date): string {
  const day = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 10, 0);
  while (day.getDay() === 0 || day.getDay() === 6) day.setDate(day.getDate() + 1);
  return `${day.getFullYear()}-${pad(day.getMonth() + 1)}-${pad(day.getDate())}T10:00`;
}
