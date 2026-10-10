import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { currentUser } from "@/server/auth/session";
import { SignupForm } from "../auth-forms";

export const metadata: Metadata = { title: "Créer un compte" };

export default async function SignupPage() {
  if (await currentUser()) redirect("/dashboard");
  return (
    <>
      <h1 className="text-2xl font-semibold tracking-tight">Créer votre compte</h1>
      <p className="mb-6 mt-1 text-sm text-muted">14 jours d&apos;essai avec toutes les fonctionnalités Pro, sans carte bancaire.</p>
      <SignupForm />
    </>
  );
}
