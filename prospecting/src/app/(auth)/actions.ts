"use server";

import { redirect } from "next/navigation";
import { createSession, destroySession } from "@/server/auth/session";
import { login, loginSchema, signup, signupSchema } from "@/server/services/auth";
import { toActionState, type ActionState } from "@/server/services/errors";

export async function signupAction(_: ActionState, form: FormData): Promise<ActionState> {
  const parsed = signupSchema.safeParse(Object.fromEntries(form));
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };
  try {
    const user = await signup(parsed.data);
    await createSession(user.id);
  } catch (error) {
    return toActionState(error);
  }
  redirect("/dashboard");
}

export async function loginAction(_: ActionState, form: FormData): Promise<ActionState> {
  const parsed = loginSchema.safeParse(Object.fromEntries(form));
  if (!parsed.success) return { error: parsed.error.issues[0]?.message ?? "Formulaire invalide" };
  try {
    const user = await login(parsed.data);
    await createSession(user.id);
  } catch (error) {
    return toActionState(error);
  }
  redirect("/dashboard");
}

export async function logoutAction() {
  await destroySession();
  redirect("/login");
}
