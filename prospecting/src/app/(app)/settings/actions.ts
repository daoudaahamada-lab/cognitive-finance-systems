"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import type { ActionState } from "@/server/services/errors";
import { parseForm } from "@/server/services/forms";
import { createToken, revokeToken, tokenNameSchema } from "@/server/services/tokens";
import { updateWorkspace, workspaceSettingsSchema } from "@/server/services/workspace";

export async function updateWorkspaceAction(_: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(workspaceSettingsSchema, Object.fromEntries(form));
  if ("state" in parsed) return parsed.state;
  await updateWorkspace(workspace.id, parsed.data);
  revalidatePath("/", "layout");
  return { ok: true, message: "Réglages enregistrés." };
}

export async function createTokenAction(_: ActionState, form: FormData): Promise<ActionState> {
  const { workspace, user } = await requireContext();
  const parsed = parseForm(tokenNameSchema, Object.fromEntries(form));
  if ("state" in parsed) return parsed.state;
  const { token } = await createToken(workspace.id, user.id, parsed.data.name);
  revalidatePath("/settings");
  return { ok: true, message: "Jeton créé. Copiez-le maintenant : il ne sera plus affiché.", secret: token };
}

export async function revokeTokenAction(tokenId: string) {
  const { workspace } = await requireContext();
  await revokeToken(workspace.id, tokenId);
  revalidatePath("/settings");
}
