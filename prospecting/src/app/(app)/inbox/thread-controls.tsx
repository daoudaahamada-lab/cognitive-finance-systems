"use client";

import { Bot, CalendarCheck, Check, Hand, Link2, PenLine, Send, Sparkles, ThumbsDown, UserRound, X } from "lucide-react";
import { startTransition, useActionState, useRef, useState, type FormEvent, type KeyboardEvent } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Field, FormMessage, Input, Textarea, checkbox } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { cn } from "@/lib/cn";
import { INTENTS, INTENT_TONES } from "@/lib/labels";
import { approveDraftAction, conversationAction, logMeetingFromInboxAction, rejectDraftAction, replyAction } from "./actions";
import { insertAt, nextBusinessDayAt10 } from "./compose";

/** Hidden fields that let an action open the next thread of the same tab (see navigation.ts). */
export type ThreadNav = { tab: string; q: string; next: string; name: string };

function NavFields({ nav }: { nav: ThreadNav }) {
  return (
    <>
      <input type="hidden" name="tab" value={nav.tab} />
      <input type="hidden" name="q" value={nav.q} />
      <input type="hidden" name="next" value={nav.next} />
      <input type="hidden" name="name" value={nav.name} />
    </>
  );
}

/** Thread header actions: take over or hand back, mark handled, close as not interested, and log a booked meeting. */
export function ThreadToolbar({
  conversationId,
  prospectId,
  status,
  unread,
  stage,
  hasDraft,
  nav,
}: {
  conversationId: string;
  prospectId: string;
  status: string;
  unread: boolean;
  stage: string;
  hasDraft: boolean;
  nav: ThreadNav;
}) {
  const [takeState, take] = useActionState(conversationAction.bind(null, conversationId, prospectId, "take_over"), null);
  const [backState, back] = useActionState(conversationAction.bind(null, conversationId, prospectId, "hand_back"), null);
  const [doneState, done] = useActionState(conversationAction.bind(null, conversationId, prospectId, "handled"), null);
  const [niState, notInterested] = useActionState(conversationAction.bind(null, conversationId, prospectId, "not_interested"), null);
  const [meetingState, logMeeting, savingMeeting] = useActionState(logMeetingFromInboxAction.bind(null, prospectId), null);
  const [meetingOpen, setMeetingOpen] = useState(false);
  const [startsAt, setStartsAt] = useState("");
  const error = [takeState, backState, doneState, niState].find((s) => s?.error) ?? null;
  const showMeetingForm = meetingOpen && !meetingState?.ok;

  const toggleMeeting = () => {
    // Prefilled in the browser, so "10:00" is the user's own time.
    if (!startsAt) setStartsAt(nextBusinessDayAt10(new Date()));
    setMeetingOpen((open) => !open);
  };

  const submitMeeting = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData();
    form.set("startsAt", startsAt);
    const at = new Date(startsAt);
    if (!Number.isNaN(at.getTime())) form.set("startsAtIso", at.toISOString());
    // Dispatched by hand: a form action would reset the field if the save fails.
    startTransition(() => logMeeting(form));
  };

  return (
    <div className="mt-3 space-y-2">
      <FormMessage state={error} />
      {/* One row that scrolls sideways on phones, wraps from sm. py-1 keeps focus rings visible inside the scroller. */}
      <div className="-mx-4 flex gap-2 overflow-x-auto px-4 py-1 sm:mx-0 sm:flex-wrap sm:overflow-visible sm:px-0">
        {status === "AI_ACTIVE" ? (
          <form action={take}>
            <NavFields nav={nav} />
            <SubmitButton size="sm" variant="secondary" pendingLabel="Prise en main…"><Hand className="size-3.5" aria-hidden /> Prendre la main</SubmitButton>
          </form>
        ) : status !== "CLOSED" ? (
          <form action={back}>
            <SubmitButton size="sm" variant="secondary" pendingLabel="Retour au setter…"><Bot className="size-3.5 text-ai" aria-hidden /> Rendre au setter</SubmitButton>
          </form>
        ) : null}
        {(status === "NEEDS_HUMAN" || unread) && !hasDraft ? (
          <form action={done}>
            <NavFields nav={nav} />
            <SubmitButton size="sm" variant="secondary" pendingLabel="Enregistrement…"><Check className="size-3.5" aria-hidden /> Marquer comme traité</SubmitButton>
          </form>
        ) : null}
        {!["NOT_INTERESTED", "MEETING_BOOKED"].includes(stage) ? (
          <form action={notInterested}>
            <NavFields nav={nav} />
            <SubmitButton size="sm" variant="secondary" pendingLabel="Classement…"><ThumbsDown className="size-3.5" aria-hidden /> Classer « Pas intéressé »</SubmitButton>
          </form>
        ) : null}
        {stage !== "MEETING_BOOKED" ? (
          <Button size="sm" variant="secondary" onClick={toggleMeeting} aria-expanded={showMeetingForm} aria-controls="inbox-meeting-form">
            <CalendarCheck className="size-3.5 text-success" aria-hidden /> RDV pris
          </Button>
        ) : null}
      </div>
      {showMeetingForm ? (
        <form id="inbox-meeting-form" onSubmit={submitMeeting} className="flex flex-wrap items-end gap-2 rounded-control border border-line bg-surface-2 p-3">
          <Field label="Date et heure du rendez-vous" htmlFor="inbox-meeting-starts-at" error={meetingState?.error} className="min-w-0 flex-1 basis-56">
            <Input
              id="inbox-meeting-starts-at"
              type="datetime-local"
              required
              autoFocus
              value={startsAt}
              onChange={(event) => setStartsAt(event.target.value)}
            />
          </Field>
          <div className="flex gap-2">
            <Button type="submit" disabled={savingMeeting} aria-busy={savingMeeting}>
              {savingMeeting ? "Enregistrement…" : "Enregistrer"}
            </Button>
            <Button variant="ghost" onClick={() => setMeetingOpen(false)}>
              Annuler
            </Button>
          </div>
        </form>
      ) : null}
      {meetingState?.ok ? <FormMessage state={meetingState} /> : null}
    </div>
  );
}

type Draft = { id: string; body: string; intent: string; rationale: string; author: string };

/**
 * The only text box of a thread. With a pending proposal it holds the setter's text (send or refuse it);
 * "Écrire moi-même" empties it and switches to a plain reply.
 */
export function ReplyBox({
  conversationId,
  status,
  draft,
  bookingUrl,
  firstName,
  nav,
}: {
  conversationId: string;
  status: string;
  draft: Draft | null;
  bookingUrl: string;
  firstName: string;
  nav: ThreadNav;
}) {
  const [mode, setMode] = useState<"proposal" | "reply">(draft ? "proposal" : "reply");
  const [body, setBody] = useState(draft?.body ?? "");
  const [last, setLast] = useState<"approve" | "reject" | "reply" | null>(null);
  const textarea = useRef<HTMLTextAreaElement>(null);
  // Until the user has placed the cursor, insert chips append to the end.
  const caretPlaced = useRef(false);
  const [approveState, approve, approving] = useActionState(approveDraftAction.bind(null, draft?.id ?? ""), null);
  const [rejectState, reject, rejecting] = useActionState(rejectDraftAction.bind(null, draft?.id ?? ""), null);
  const [replyState, reply, replying] = useActionState(replyAction.bind(null, conversationId), null);
  const pending = approving || rejecting || replying;
  const proposing = mode === "proposal" && draft !== null;
  const state = last === "approve" ? approveState : last === "reject" ? rejectState : last === "reply" ? replyState : null;

  // Dispatched by hand rather than through a form action, so a failed send never clears the text.
  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (pending) return;
    const form = new FormData(event.currentTarget);
    setLast(proposing ? "approve" : "reply");
    startTransition(() => (proposing ? approve(form) : reply(form)));
  };

  const refuse = () => {
    if (pending) return;
    setLast("reject");
    startTransition(() => reject());
  };

  const writeMyself = () => {
    setMode("reply");
    setBody("");
    setLast(null);
    caretPlaced.current = false;
    textarea.current?.focus();
  };

  const backToProposal = () => {
    setMode("proposal");
    setBody(draft?.body ?? "");
    setLast(null);
  };

  const insert = (text: string) => {
    const el = textarea.current;
    const start = el && caretPlaced.current ? el.selectionStart : body.length;
    const end = el && caretPlaced.current ? el.selectionEnd : body.length;
    const next = insertAt(body, start, end, text);
    setBody(next.value);
    requestAnimationFrame(() => {
      el?.focus();
      el?.setSelectionRange(next.caret, next.caret);
      caretPlaced.current = true;
    });
  };

  const onKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
      event.preventDefault();
      event.currentTarget.form?.requestSubmit();
    }
  };

  return (
    <form onSubmit={submit} className="space-y-2" aria-label={proposing ? "Réponse proposée par le setter" : `Répondre à ${firstName}`}>
      <NavFields nav={nav} />
      <input type="hidden" name="conversationId" value={conversationId} />
      <FormMessage state={state?.error ? state : null} />

      {proposing ? (
        <div className="flex min-w-0 items-start gap-2 text-xs">
          <span className="inline-flex shrink-0 items-center gap-1 font-medium text-ai" title={draft.author === "claude" ? "Rédigée par Claude" : "Modèle de réponse du setter"}>
            <Sparkles className="size-3.5" aria-hidden /> Réponse proposée
          </span>
          <Badge tone={INTENT_TONES[draft.intent] ?? "neutral"} className="shrink-0">{INTENTS[draft.intent] ?? draft.intent}</Badge>
          {draft.rationale ? <span className="min-w-0 text-muted line-clamp-1 sm:line-clamp-2">{draft.rationale}</span> : null}
        </div>
      ) : (
        <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1">
          <label htmlFor="inbox-reply-body" className="text-sm font-medium text-ink">
            Votre réponse
          </label>
          <label className="flex items-center gap-2 text-xs text-muted">
            <input type="checkbox" name="handBack" defaultChecked={status === "AI_ACTIVE"} className={checkbox} />
            Rendre la main au setter après envoi
          </label>
        </div>
      )}

      <Textarea
        ref={textarea}
        id="inbox-reply-body"
        name="body"
        rows={3}
        required
        value={body}
        onChange={(event) => setBody(event.target.value)}
        onSelect={() => {
          caretPlaced.current = true;
        }}
        onKeyDown={onKeyDown}
        aria-label={proposing ? "Réponse proposée (modifiable)" : undefined}
        placeholder={proposing ? undefined : `Votre message à ${firstName}…`}
        className={cn("max-h-64 resize-y max-lg:max-h-40", proposing && "border-ai-line")}
      />

      <div className="flex flex-wrap items-center justify-between gap-2">
        <div role="group" aria-label="Insérer dans le message" className="flex flex-wrap gap-2">
          {bookingUrl ? (
            <Button size="sm" variant="secondary" className="rounded-full" onClick={() => insert(bookingUrl)}>
              <Link2 className="size-3.5" aria-hidden /> Lien de réservation
            </Button>
          ) : null}
          <Button size="sm" variant="secondary" className="rounded-full" onClick={() => insert(firstName)}>
            <UserRound className="size-3.5" aria-hidden /> Prénom
          </Button>
        </div>
        <div className="ml-auto flex flex-wrap items-center justify-end gap-2">
          {proposing ? (
            <>
              <Button size="sm" variant="ghost" onClick={writeMyself} disabled={pending}>
                <PenLine className="size-3.5" aria-hidden /> Écrire<span className="max-sm:hidden"> moi-même</span>
              </Button>
              <Button size="sm" variant="secondary" onClick={refuse} disabled={pending} aria-busy={rejecting}>
                {rejecting ? (
                  "Refus…"
                ) : (
                  <>
                    <X className="size-3.5" aria-hidden /> Refuser<span className="max-sm:hidden"> la proposition</span>
                  </>
                )}
              </Button>
            </>
          ) : draft ? (
            <Button size="sm" variant="ghost" onClick={backToProposal} disabled={pending}>
              <Sparkles className="size-3.5 text-ai" aria-hidden /> Reprendre la proposition
            </Button>
          ) : null}
          <Button type="submit" size="sm" disabled={pending} aria-busy={approving || replying} title="Envoyer (Ctrl + Entrée)">
            {approving || replying ? (
              "Envoi…"
            ) : (
              <>
                <Send className="size-3.5" aria-hidden /> Envoyer
              </>
            )}
          </Button>
        </div>
      </div>
    </form>
  );
}
