"use client";

import { Check, Copy } from "lucide-react";
import { useActionState, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Field, FormMessage, Input } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { createTokenAction } from "./actions";

function CopyBlock({ label, text }: { label: string; text: string }) {
  const [copied, setCopied] = useState<"yes" | "no" | null>(null);
  useEffect(() => {
    if (!copied) return;
    const timer = setTimeout(() => setCopied(null), 2000);
    return () => clearTimeout(timer);
  }, [copied]);
  return (
    <div>
      <div className="mb-1 flex items-center justify-between gap-2">
        <p className="text-xs font-medium text-muted">{label}</p>
        <Button
          variant="ghost"
          size="sm"
          aria-label={`Copier : ${label}`}
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(text);
              setCopied("yes");
            } catch {
              setCopied("no");
            }
          }}
        >
          {copied === "yes" ? <Check className="size-3.5 text-success" aria-hidden /> : <Copy className="size-3.5" aria-hidden />}
          <span aria-hidden>{copied === "yes" ? "Copié" : "Copier"}</span>
        </Button>
      </div>
      <pre className="overflow-x-auto rounded-control bg-ink px-3 py-2.5 text-xs leading-relaxed text-white">{text}</pre>
      <span aria-live="polite" className="sr-only">
        {copied === "yes" ? "Copié dans le presse-papiers" : copied === "no" ? "Copie impossible : sélectionnez le texte à la main." : ""}
      </span>
    </div>
  );
}

export function CreateTokenForm({ endpoint }: { endpoint: string }) {
  const [state, action] = useActionState(createTokenAction, null);
  const token = state?.secret;
  return (
    <div className="space-y-4">
      <form action={action} className="flex flex-wrap items-end gap-2">
        <Field label="Nouveau jeton" htmlFor="token-name" error={state?.fieldErrors?.name} className="min-w-48 flex-1">
          <Input id="token-name" name="name" placeholder="Claude Code sur mon portable" required />
        </Field>
        <SubmitButton variant="secondary" pendingLabel="Création…">Créer</SubmitButton>
      </form>
      <FormMessage state={state?.error ? state : state?.message ? { message: state.message } : null} />
      {token ? (
        <div className="space-y-3">
          <CopyBlock label="Jeton" text={token} />
          <CopyBlock label="Claude Code" text={`claude mcp add --transport http vela ${endpoint} --header "Authorization: Bearer ${token}"`} />
          <CopyBlock
            label="Cursor (.cursor/mcp.json)"
            text={JSON.stringify({ mcpServers: { vela: { url: endpoint, headers: { Authorization: `Bearer ${token}` } } } }, null, 2)}
          />
        </div>
      ) : null}
    </div>
  );
}
