import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { ButtonLink } from "@/components/ui/button";
import { currentUser } from "@/server/auth/session";
import { signupOpen } from "@/server/services/auth";
import { SignupForm } from "../auth-forms";

export const metadata: Metadata = { title: "Créer un compte" };

export default async function SignupPage() {
  if (await currentUser()) redirect("/dashboard");
  if (!(await signupOpen())) {
    return (
      <>
        <h1 className="text-h1 font-semibold text-ink">Inscriptions fermées</h1>
        <p className="mb-6 mt-1 text-sm text-muted">Vela est déjà configuré pour son propriétaire. Connectez-vous avec votre compte.</p>
        <ButtonLink href="/login" variant="secondary">Se connecter</ButtonLink>
      </>
    );
  }
  return (
    <>
      <h1 className="text-h1 font-semibold text-ink">Créer votre compte</h1>
      <p className="mb-6 mt-1 text-sm text-muted">Ce premier compte devient le propriétaire de Vela sur cet ordinateur ; les inscriptions se ferment ensuite.</p>
      <SignupForm />
    </>
  );
}
