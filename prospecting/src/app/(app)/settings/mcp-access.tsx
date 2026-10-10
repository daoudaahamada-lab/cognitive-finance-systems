"use client";

import { Check, Copy } from "lucide-react";
import { useActionState, useState } from "react";
import { Button } from "@/components/ui/button";
import { Field, FormMessage, Input } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { createTokenAction } from "./actions";

function CopyBlock({ label, text }: { label: string; text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <div>
      <div className="mb-1 flex items-center justify-between">
        <p className="text-xs font-medium text-muted">{label}</p>
        <Button
          variant="ghost"
          size="sm"
          onClick={async () => {
            await navigator.clipboard.writeText(text);
            setCopied(true);
            setTimeout(() => setCopied(false), 1500);
          }}
        >
          {copied ? <Check className="size-3.5" aria-hidden /> : <Copy className="size-3.5" aria-hidden />} {copied ? "Copié" : "Copier"}
        </Button>
      </div>
      <pre className="overflow-x-auto rounded-lg bg-ink px-3 py-2.5 text-xs leading-relaxed text-white">{text}</pre>
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
