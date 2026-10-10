"use client";

import { useActionState } from "react";
import { Field, FormMessage, Input, Textarea } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { importProspectsAction } from "../actions";

export function ImportForm({ campaignId }: { campaignId: string }) {
  const [state, action] = useActionState(importProspectsAction.bind(null, campaignId), null);
  return (
    <form action={action} className="space-y-3">
      <FormMessage state={state} />
      <Field label="URLs de profils" htmlFor="urls" hint="Une par ligne, ou collez un export (Sales Navigator, CRM…) : toutes les URLs linkedin.com/in/ sont reprises.">
        <Textarea id="urls" name="urls" rows={4} placeholder="https://www.linkedin.com/in/camille-durand" />
      </Field>
      <Field label="ou un fichier CSV" htmlFor="file">
        <Input id="file" name="file" type="file" accept=".csv,.txt,text/csv,text/plain" className="py-1.5 file:mr-3 file:rounded file:border-0 file:bg-canvas file:px-2 file:py-1 file:text-xs" />
      </Field>
      <SubmitButton variant="secondary" pendingLabel="Import…">Importer</SubmitButton>
    </form>
  );
}
