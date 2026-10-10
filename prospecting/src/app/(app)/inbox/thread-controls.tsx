"use client";

import { Bot, Check, Hand, Send, Sparkles, X } from "lucide-react";
import { useActionState, useEffect, useRef } from "react";
import { Field, FormMessage, Textarea } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { INTENTS } from "@/lib/labels";
import { approveDraftAction, conversationAction, rejectDraftAction, replyAction } from "./actions";

export function DraftCard({ draft }: { draft: { id: string; conversationId: string; body: string; intent: string; rationale: string } }) {
  const [approveState, approve] = useActionState(approveDraftAction.bind(null, draft.id), null);
  const [rejectState, reject] = useActionState(rejectDraftAction.bind(null, draft.id), null);
  return (
    <div className="rounded-xl border border-brand-200 bg-brand-50/60 p-4">
      <div className="mb-2 flex flex-wrap items-center gap-2 text-sm">
        <Sparkles className="size-4 text-brand-600" aria-hidden />
        <span className="font-medium text-brand-900">Brouillon du setter</span>
        <span className="rounded-md bg-surface px-1.5 py-0.5 text-xs text-muted">{INTENTS[draft.intent] ?? draft.intent}</span>
      </div>
      <p className="mb-3 text-xs text-muted">{draft.rationale}</p>
      <FormMessage state={approveState?.error ? approveState : rejectState} />
      <form action={approve} className="space-y-2">
        <input type="hidden" name="conversationId" value={draft.conversationId} />
        <Textarea name="body" rows={4} defaultValue={draft.body} aria-label="Brouillon (modifiable)" />
        <div className="flex flex-wrap gap-2">
          <SubmitButton size="sm" pendingLabel="Envoi…"><Check className="size-3.5" /> Valider et envoyer</SubmitButton>
          <SubmitButton size="sm" variant="secondary" formAction={reject} pendingLabel="…"><X className="size-3.5" /> Refuser</SubmitButton>
        </div>
      </form>
    </div>
  );
}

export function Composer({ conversationId, status }: { conversationId: string; status: string }) {
  const [state, action] = useActionState(replyAction.bind(null, conversationId), null);
  const formRef = useRef<HTMLFormElement>(null);
  useEffect(() => {
    if (state?.ok) formRef.current?.reset();
  }, [state]);
  return (
    <form ref={formRef} action={action} className="space-y-2">
      <FormMessage state={state?.error ? state : null} />
      <Field label="Répondre" htmlFor="reply-body">
        <Textarea id="reply-body" name="body" rows={3} placeholder="Votre message…" required />
      </Field>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <label className="flex items-center gap-2 text-xs text-muted">
          <input type="checkbox" name="handBack" defaultChecked={status === "AI_ACTIVE"} className="accent-brand-600" />
          Rendre la main au setter après envoi
        </label>
        <SubmitButton size="sm" pendingLabel="Envoi…"><Send className="size-3.5" /> Envoyer</SubmitButton>
      </div>
    </form>
  );
}

export function ConversationButtons({ conversationId, prospectId, status, unread, stage }: { conversationId: string; prospectId: string; status: string; unread: boolean; stage: string }) {
  const [takeState, take] = useActionState(conversationAction.bind(null, conversationId, prospectId, "take_over"), null);
  const [backState, back] = useActionState(conversationAction.bind(null, conversationId, prospectId, "hand_back"), null);
  const [doneState, done] = useActionState(conversationAction.bind(null, conversationId, prospectId, "handled"), null);
  const [niState, notInterested] = useActionState(conversationAction.bind(null, conversationId, prospectId, "not_interested"), null);
  const error = [takeState, backState, doneState, niState].find((s) => s?.error) ?? null;
  return (
    <div className="space-y-2">
      <FormMessage state={error} />
      <div className="flex flex-wrap gap-2">
        {status === "AI_ACTIVE" ? (
          <form action={take}><SubmitButton size="sm" variant="secondary"><Hand className="size-3.5" /> Prendre la main</SubmitButton></form>
        ) : status !== "CLOSED" ? (
          <form action={back}><SubmitButton size="sm" variant="secondary"><Bot className="size-3.5" /> Rendre au setter</SubmitButton></form>
        ) : null}
        {status === "NEEDS_HUMAN" || unread ? (
          <form action={done}><SubmitButton size="sm" variant="secondary"><Check className="size-3.5" /> Marquer traité</SubmitButton></form>
        ) : null}
        {!["NOT_INTERESTED", "MEETING_BOOKED"].includes(stage) ? (
          <form action={notInterested}><SubmitButton size="sm" variant="ghost">Pas intéressé</SubmitButton></form>
        ) : null}
      </div>
    </div>
  );
}
