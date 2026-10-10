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
        <h1 className="text-2xl font-semibold tracking-tight">Inscriptions fermées</h1>
        <p className="mb-6 mt-1 text-sm text-muted">Cette instance a déjà son compte. Pour en ouvrir d&apos;autres, définissez ALLOW_SIGNUP=true.</p>
        <ButtonLink href="/login" variant="secondary">Se connecter</ButtonLink>
      </>
    );
  }
  return (
    <>
      <h1 className="text-2xl font-semibold tracking-tight">Créer votre compte</h1>
      <p className="mb-6 mt-1 text-sm text-muted">Le premier compte créé devient le propriétaire de cette instance ; les inscriptions se ferment ensuite.</p>
      <SignupForm />
    </>
  );
}
