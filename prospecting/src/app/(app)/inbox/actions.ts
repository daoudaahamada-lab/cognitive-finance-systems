"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { requireContext } from "@/server/auth/context";
import { toActionState, type ActionState } from "@/server/services/errors";
import { approveDraft, closeAsNotInterested, handBackToAi, logMeeting, markHandled, rejectDraft, sendHumanReply, takeOver } from "@/server/services/inbox";
import { afterActionUrl, type DoneKind } from "./navigation";

async function run(fn: (workspaceId: string) => Promise<unknown>, success?: string): Promise<ActionState> {
  const { workspace } = await requireContext();
  try {
    await fn(workspace.id);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/", "layout");
  return { ok: true, message: success };
}

/** Once the thread is dealt with, open the next one of the same tab (the form carries tab, q, next and name). */
function moveOn(state: ActionState, form: FormData | undefined, did: DoneKind): ActionState {
  const url = state?.ok && form ? afterActionUrl(form, did) : null;
  if (url) redirect(url);
  return state;
}

export async function replyAction(conversationId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const state = await run((ws) => sendHumanReply(ws, conversationId, String(form.get("body") ?? ""), form.get("handBack") === "on"), "Message envoyé.");
  return moveOn(state, form, "sent");
}

export async function approveDraftAction(draftId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const state = await run((ws) => approveDraft(ws, draftId, String(form.get("body") ?? "")), "Réponse envoyée.");
  return moveOn(state, form, "sent");
}

export async function rejectDraftAction(draftId: string, _: ActionState): Promise<ActionState> {
  return run((ws) => rejectDraft(ws, draftId));
}

export async function conversationAction(
  conversationId: string,
  prospectId: string,
  kind: "take_over" | "hand_back" | "handled" | "not_interested",
  _: ActionState,
  form?: FormData,
): Promise<ActionState> {
  const state = await run((ws) => {
    switch (kind) {
      case "take_over":
        return takeOver(ws, conversationId);
      case "hand_back":
        return handBackToAi(ws, conversationId);
      case "handled":
        return markHandled(ws, conversationId);
      case "not_interested":
        return closeAsNotInterested(ws, conversationId);
    }
  });
  return kind === "hand_back" ? state : moveOn(state, form, kind);
}

/**
 * "RDV pris" in a thread: records the meeting (the prospect moves to MEETING_BOOKED and the conversation closes).
 * The browser sends the instant as ISO (startsAtIso) so the local time typed is kept whatever the server's zone.
 */
export async function logMeetingFromInboxAction(prospectId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const raw = String(form.get("startsAtIso") || form.get("startsAt") || "").trim();
  if (!raw) return { error: "Indiquez la date et l'heure du rendez-vous." };
  return run((ws) => logMeeting(ws, prospectId, new Date(raw)), "Rendez-vous enregistré.");
}
