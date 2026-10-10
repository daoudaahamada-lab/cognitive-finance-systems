"use client";

import Link from "next/link";
import { useActionState } from "react";
import { Field, FormMessage, Input } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { loginAction, signupAction } from "./actions";

export function LoginForm({ signupOpen }: { signupOpen: boolean }) {
  const [state, action] = useActionState(loginAction, null);
  return (
    <form action={action} className="space-y-4">
      <FormMessage state={state} />
      <Field label="Email" htmlFor="email">
        <Input id="email" name="email" type="email" autoComplete="email" required />
      </Field>
      <Field label="Mot de passe" htmlFor="password">
        <Input id="password" name="password" type="password" autoComplete="current-password" required />
      </Field>
      <SubmitButton className="w-full" pendingLabel="Connexion…">Se connecter</SubmitButton>
      {signupOpen ? (
        <p className="text-center text-sm text-muted">
          Pas encore de compte ?{" "}
          <Link href="/signup" className="font-medium text-brand-700 hover:underline">
            Créer le compte
          </Link>
        </p>
      ) : null}
    </form>
  );
}

export function SignupForm() {
  const [state, action] = useActionState(signupAction, null);
  return (
    <form action={action} className="space-y-4">
      <FormMessage state={state} />
      <Field label="Votre nom" htmlFor="name">
        <Input id="name" name="name" autoComplete="name" required />
      </Field>
      <Field label="Entreprise" htmlFor="company">
        <Input id="company" name="company" autoComplete="organization" required />
      </Field>
      <Field label="Email professionnel" htmlFor="email">
        <Input id="email" name="email" type="email" autoComplete="email" required />
      </Field>
      <Field label="Mot de passe" htmlFor="password" hint="8 caractères minimum">
        <Input id="password" name="password" type="password" autoComplete="new-password" minLength={8} required />
      </Field>
      <SubmitButton className="w-full" pendingLabel="Création…">Créer mon compte</SubmitButton>
      <p className="text-center text-sm text-muted">
        Déjà inscrit ?{" "}
        <Link href="/login" className="font-medium text-brand-700 hover:underline">
          Se connecter
        </Link>
      </p>
    </form>
  );
}
