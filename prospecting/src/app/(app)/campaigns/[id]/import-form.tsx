"use client";

import { startTransition, useActionState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { FileDrop } from "@/components/ui/file-drop";
import { Field, FormMessage, Textarea } from "@/components/ui/form";
import { importProspectsAction } from "../actions";

export function ImportForm({ campaignId }: { campaignId: string }) {
  const [state, action, pending] = useActionState(importProspectsAction.bind(null, campaignId), null);
  const form = useRef<HTMLFormElement>(null);

  // Submitted outside a form action, so React does not clear the pasted URLs when the import fails;
  // the form is emptied only once it succeeded.
  useEffect(() => {
    if (state?.ok) form.current?.reset();
  }, [state]);

  return (
    <form
      ref={form}
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        startTransition(() => action(data));
      }}
    >
      <Field label="URLs de profils" htmlFor="urls" hint="Une par ligne, ou collez un export (Sales Navigator, CRM…) : toutes les URLs linkedin.com/in/ sont reprises.">
        <Textarea id="urls" name="urls" rows={4} placeholder="https://www.linkedin.com/in/camille-durand" />
      </Field>
      <Field label="Ou un fichier" htmlFor="file">
        <FileDrop id="file" name="file" accept=".csv,.txt,text/csv,text/plain" hint="CSV ou texte, 2 Mo maximum" />
      </Field>
      <div className="flex flex-wrap items-center justify-end gap-3">
        <div className="min-w-0 flex-1">
          <FormMessage state={state} />
        </div>
        <Button type="submit" disabled={pending} aria-busy={pending}>
          {pending ? "Import…" : "Importer"}
        </Button>
      </div>
    </form>
  );
}
