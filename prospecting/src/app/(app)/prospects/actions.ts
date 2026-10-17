"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import { toActionState, type ActionState } from "@/server/services/errors";
import { logMeeting } from "@/server/services/inbox";
import { applyManualStage, saveNotes, snoozeProspect, type ManualStageAction } from "@/server/services/prospects";

export async function manualStageAction(prospectId: string, action: ManualStageAction, _: ActionState): Promise<ActionState> {
  const { workspace } = await requireContext();
  try {
    await applyManualStage(workspace.id, prospectId, action);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath(`/prospects/${prospectId}`);
  return { ok: true };
}

export async function snoozeAction(prospectId: string, days: number) {
  const { workspace } = await requireContext();
  await snoozeProspect(workspace.id, prospectId, days);
  revalidatePath(`/prospects/${prospectId}`);
}

export async function notesAction(prospectId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  await saveNotes(workspace.id, prospectId, String(form.get("notes") ?? ""));
  revalidatePath(`/prospects/${prospectId}`);
  return { ok: true, message: "Notes enregistrées." };
}

/** The form sends the browser's instant as ISO (startsAtIso); the raw local value is the fallback without JavaScript. */
export async function logMeetingAction(prospectId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const raw = String(form.get("startsAtIso") || form.get("startsAt") || "").trim();
  if (!raw) return { error: "Indiquez la date et l'heure du rendez-vous." };
  try {
    await logMeeting(workspace.id, prospectId, new Date(raw));
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/", "layout");
  return { ok: true, message: "Rendez-vous enregistré." };
}
