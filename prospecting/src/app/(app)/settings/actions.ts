"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import type { ActionState } from "@/server/services/errors";
import { parseForm } from "@/server/services/forms";
import { changePlan, updateWorkspace, workspaceSettingsSchema } from "@/server/services/workspace";

export async function updateWorkspaceAction(_: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(workspaceSettingsSchema, Object.fromEntries(form));
  if ("state" in parsed) return parsed.state;
  await updateWorkspace(workspace.id, parsed.data);
  revalidatePath("/", "layout");
  return { ok: true, message: "Réglages enregistrés." };
}

export async function changePlanAction(plan: "STARTER" | "PRO" | "AGENCY") {
  const { workspace, role } = await requireContext();
  if (role !== "OWNER") return;
  await changePlan(workspace.id, plan);
  revalidatePath("/", "layout");
}
