import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { currentUser } from "@/server/auth/session";
import { signupOpen } from "@/server/services/auth";
import { LoginForm } from "../auth-forms";

export const metadata: Metadata = { title: "Connexion" };

export default async function LoginPage() {
  if (await currentUser()) redirect("/dashboard");
  return (
    <>
      <h1 className="text-h1 font-semibold text-ink">Connexion</h1>
      <p className="mb-6 mt-1 text-sm text-muted">Connectez-vous pour suivre votre prospection.</p>
      <LoginForm signupOpen={await signupOpen()} />
    </>
  );
}
