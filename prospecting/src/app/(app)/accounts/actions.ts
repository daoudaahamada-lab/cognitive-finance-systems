"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import {
  accountSettingsSchema,
  connectAccount,
  connectAccountSchema,
  diagnoseAccount,
  sessionSchema,
  setAccountStatus,
  updateAccountSession,
  updateAccountSettings,
} from "@/server/services/accounts";
import { toActionState, type ActionState } from "@/server/services/errors";
import type { DiagnosticLine } from "@/server/linkedin/types";
import { parseForm } from "@/server/services/forms";

/** The new account's id lets the form scroll to its card. */
export type ConnectState = (NonNullable<ActionState> & { accountId?: string }) | null;

export async function connectAccountAction(_: ConnectState, form: FormData): Promise<ConnectState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(connectAccountSchema, Object.fromEntries(form));
  if ("state" in parsed) return parsed.state;
  let account;
  try {
    account = await connectAccount(workspace.id, parsed.data);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/", "layout");
  const message =
    account.provider !== "browser"
      ? "Compte connecté."
      : account.status === "ACTIVE"
        ? "Compte connecté. Étape suivante : vérifiez la connexion LinkedIn (≈1 min)."
        : "Compte ajouté. Étape suivante : ouvrez sa session LinkedIn en suivant les étapes de sa carte.";
  return { ok: true, message, accountId: account.id };
}

export async function updateSessionAction(accountId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(sessionSchema, Object.fromEntries(form));
  if ("state" in parsed) return parsed.state;
  try {
    await updateAccountSession(workspace.id, accountId, parsed.data.sessionCookie);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/", "layout");
  return { ok: true, message: "Session ouverte : le compte est actif. Étape suivante : vérifiez la connexion LinkedIn (≈1 min)." };
}

export type DiagnosticState = { lines?: DiagnosticLine[]; error?: string } | null;

export async function diagnoseAccountAction(accountId: string, _: DiagnosticState): Promise<DiagnosticState> {
  const { workspace } = await requireContext();
  let state: DiagnosticState;
  try {
    state = { lines: await diagnoseAccount(workspace.id, accountId) };
  } catch (error) {
    state = toActionState(error) as DiagnosticState;
  }
  // The outcome is stored on the account: the accounts page, dashboard and campaigns read it.
  revalidatePath("/", "layout");
  return state;
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

export async function setAccountStatusAction(accountId: string, status: "ACTIVE" | "PAUSED" | "DISCONNECTED", _: ActionState): Promise<ActionState> {
  const { workspace } = await requireContext();
  try {
    await setAccountStatus(workspace.id, accountId, status);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/", "layout");
  return null;
}
