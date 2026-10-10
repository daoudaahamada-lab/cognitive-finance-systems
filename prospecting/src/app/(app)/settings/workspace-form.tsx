"use client";

import type { Workspace } from "@prisma/client";
import { useActionState } from "react";
import { Field, FormMessage, Input, Textarea } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { updateWorkspaceAction } from "./actions";

export function WorkspaceForm({ workspace }: { workspace: Workspace }) {
  const [state, action] = useActionState(updateWorkspaceAction, null);
  const err = state?.fieldErrors ?? {};
  return (
    <form action={action} className="space-y-4">
      <FormMessage state={state} />
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Nom de l'espace" htmlFor="name" error={err.name}>
          <Input id="name" name="name" defaultValue={workspace.name} required />
        </Field>
        <Field label="Fuseau horaire" htmlFor="timezone" error={err.timezone} hint="Ex. Europe/Paris">
          <Input id="timezone" name="timezone" defaultValue={workspace.timezone} required />
        </Field>
      </div>
      <Field
        label="Votre offre"
        htmlFor="offer"
        error={err.offer}
        hint="Ce que vous vendez et pour qui. La première phrase sert de réponse courte quand un prospect pose une question."
      >
        <Textarea id="offer" name="offer" rows={4} defaultValue={workspace.offer} placeholder="Nous automatisons le reporting financier des PME de 20 à 200 salariés…" />
      </Field>
      <Field label="Client idéal" htmlFor="persona" error={err.persona} hint="Utilisé par défaut dans les nouvelles campagnes.">
        <Textarea id="persona" name="persona" rows={3} defaultValue={workspace.persona} placeholder="DAF et CFO de PME SaaS ou de conseil, en France…" />
      </Field>
      <Field label="Lien de réservation" htmlFor="bookingUrl" error={err.bookingUrl} hint="Calendly, Cal.com, Google Agenda… Le setter l'envoie aux prospects intéressés.">
        <Input id="bookingUrl" name="bookingUrl" type="url" defaultValue={workspace.bookingUrl} placeholder="https://calendly.com/vous/20min" />
      </Field>
      <SubmitButton pendingLabel="Enregistrement…">Enregistrer</SubmitButton>
    </form>
  );
}
