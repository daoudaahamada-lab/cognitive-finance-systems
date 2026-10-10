"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import type { ActionState } from "@/server/services/errors";
import { parseForm } from "@/server/services/forms";
import { updateWorkspace, workspaceSettingsSchema } from "@/server/services/workspace";

export async function updateWorkspaceAction(_: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(workspaceSettingsSchema, Object.fromEntries(form));
  if ("state" in parsed) return parsed.state;
  await updateWorkspace(workspace.id, parsed.data);
  revalidatePath("/", "layout");
  return { ok: true, message: "Réglages enregistrés." };
}
