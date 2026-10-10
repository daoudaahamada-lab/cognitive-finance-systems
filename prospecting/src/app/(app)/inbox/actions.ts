"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { requireContext } from "@/server/auth/context";
import { toActionState, type ActionState } from "@/server/services/errors";
import { approveDraft, handBackToAi, markHandled, rejectDraft, sendHumanReply, takeOver } from "@/server/services/inbox";
import { applyManualStage } from "@/server/services/prospects";

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

export async function replyAction(conversationId: string, _: ActionState, form: FormData): Promise<ActionState> {
  return run((ws) => sendHumanReply(ws, conversationId, String(form.get("body") ?? ""), form.get("handBack") === "on"), "Message envoyé.");
}

export async function approveDraftAction(draftId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const state = await run((ws) => approveDraft(ws, draftId, String(form.get("body") ?? "")), "Réponse envoyée.");
  // The draft card disappears once sent, so confirm on the thread itself.
  if (state?.ok) redirect(`/inbox?c=${String(form.get("conversationId") ?? "")}&sent=1`);
  return state;
}

export async function rejectDraftAction(draftId: string, _: ActionState): Promise<ActionState> {
  return run((ws) => rejectDraft(ws, draftId));
}

export async function conversationAction(
  conversationId: string,
  prospectId: string,
  kind: "take_over" | "hand_back" | "handled" | "not_interested",
  _: ActionState,
): Promise<ActionState> {
  return run((ws) => {
    switch (kind) {
      case "take_over":
        return takeOver(ws, conversationId);
      case "hand_back":
        return handBackToAi(ws, conversationId);
      case "handled":
        return markHandled(ws, conversationId);
      case "not_interested":
        return applyManualStage(ws, prospectId, "not_interested");
    }
  });
}
