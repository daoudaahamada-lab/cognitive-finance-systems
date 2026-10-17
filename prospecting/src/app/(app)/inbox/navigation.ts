/** Moving through the inbox: tab parsing, thread position, the thread to open after an action, and its banner. */

import { INBOX_TABS, type InboxTab } from "@/server/services/inbox";

export type DoneKind = "sent" | "handled" | "not_interested" | "take_over";

export function parseTab(value: unknown): InboxTab {
  return INBOX_TABS.includes(value as InboxTab) ? (value as InboxTab) : "todo";
}

/**
 * Where the current thread sits in the list (newest first).
 * `afterId` is the thread to open once this one is dealt with: the next (older) one, else the newest other one.
 */
export function threadNavigation(ids: string[], currentId?: string | null) {
  const index = currentId ? ids.indexOf(currentId) : -1;
  return {
    /** 1-based; 0 when the thread is not in the list (search, other tab). */
    position: index + 1,
    prevId: index > 0 ? ids[index - 1]! : null,
    nextId: index >= 0 ? (ids[index + 1] ?? null) : null,
    afterId: ids[index + 1] ?? ids.find((id) => id !== currentId) ?? null,
  };
}

const text = (value: FormDataEntryValue | null) => (typeof value === "string" ? value.trim() : "");

/**
 * URL to land on after acting on a thread, from the hidden fields the thread forms carry (tab, q, next, name).
 * Keeps the current tab and search; null when the form did not come from the inbox page.
 */
export function afterActionUrl(form: FormData, did: DoneKind): string | null {
  if (!form.has("tab")) return null;
  const params = new URLSearchParams({ tab: parseTab(text(form.get("tab"))) });
  const q = text(form.get("q")).slice(0, 100);
  const next = text(form.get("next"));
  const name = text(form.get("name")).slice(0, 60);
  if (q) params.set("q", q);
  if (next) params.set("c", next);
  if (name) params.set("done", name);
  params.set("did", did);
  return `/inbox?${params.toString()}`;
}

/** Confirmation shown after an action, e.g. "Réponse envoyée à Alexandre". */
export function doneMessage(did: string | undefined, name: string): string {
  switch (did) {
    case "handled":
      return `Conversation avec ${name} marquée comme traitée`;
    case "not_interested":
      return `Conversation avec ${name} classée « Pas intéressé »`;
    case "take_over":
      return `Vous avez la main sur la conversation avec ${name}`;
    default:
      return `Réponse envoyée à ${name}`;
  }
}

/**
 * Folds the opening run of sequence messages when a thread holds more than `threshold` of them,
 * keeping the last one (the message the prospect answered) in view.
 */
export function foldSequence<T extends { author: string }>(messages: T[], threshold = 3): { folded: T[]; visible: T[] } {
  const sequence = messages.filter((m) => m.author === "SEQUENCE").length;
  let run = 0;
  while (run < messages.length && messages[run]!.author === "SEQUENCE") run++;
  const fold = run - 1;
  if (sequence <= threshold || fold < 2) return { folded: [], visible: messages };
  return { folded: messages.slice(0, fold), visible: messages.slice(fold) };
}
