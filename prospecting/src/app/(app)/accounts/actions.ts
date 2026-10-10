"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import {
  accountSettingsSchema,
  connectAccount,
  connectAccountSchema,
  setAccountStatus,
  updateAccountSettings,
} from "@/server/services/accounts";
import { toActionState, type ActionState } from "@/server/services/errors";
import { parseForm } from "@/server/services/forms";

export async function connectAccountAction(_: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(connectAccountSchema, Object.fromEntries(form));
  if ("state" in parsed) return parsed.state;
  try {
    await connectAccount(workspace.id, parsed.data);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/", "layout");
  return { ok: true, message: "Compte connecté." };
}

export async function updateAccountAction(accountId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(accountSettingsSchema, { ...Object.fromEntries(form), sendingDays: form.getAll("sendingDays") });
  if ("state" in parsed) return parsed.state;
  try {
    await updateAccountSettings(workspace.id, accountId, parsed.data);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/accounts");
  return { ok: true, message: "Réglages enregistrés." };
}

export async function setAccountStatusAction(accountId: string, status: "ACTIVE" | "PAUSED" | "DISCONNECTED") {
  const { workspace } = await requireContext();
  await setAccountStatus(workspace.id, accountId, status);
  revalidatePath("/", "layout");
}
