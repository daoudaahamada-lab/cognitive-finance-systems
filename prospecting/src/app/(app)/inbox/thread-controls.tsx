"use client";

import { Bot, CalendarCheck, Check, Hand, Link2, PenLine, Send, Sparkles, ThumbsDown, UserRound, X } from "lucide-react";
import { startTransition, useActionState, useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Field, FormMessage, Input, Textarea, checkbox } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { cn } from "@/lib/cn";
import { INTENTS, INTENT_TONES } from "@/lib/labels";
import { approveDraftAction, conversationAction, logMeetingFromInboxAction, rejectDraftAction, replyAction } from "./actions";
import { insertAt, nextBusinessDayAt10, proposalChange } from "./compose";

/** Hidden fields that let an action open the next thread of the same tab (see navigation.ts). */
export type ThreadNav = { tab: string; q: string; next: string; name: string };

/** The thread's only text box (ReplyBox); "Prendre la main" focuses it. */
const REPLY_BODY_ID = "inbox-reply-body";

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

  // "Prendre la main" stays on the thread because the user is about to write: put the cursor in the reply box.
  useEffect(() => {
    if (takeState?.ok) document.getElementById(REPLY_BODY_ID)?.focus();
  }, [takeState]);

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
      {/* Every action stays in view: the row wraps, "RDV pris" comes first, and the long labels are shortened on phones. */}
      <div className="flex flex-wrap gap-2">
        {stage !== "MEETING_BOOKED" ? (
          <Button size="sm" variant="secondary" onClick={toggleMeeting} aria-expanded={showMeetingForm} aria-controls="inbox-meeting-form">
            <CalendarCheck className="size-3.5 text-success" aria-hidden /> RDV pris
          </Button>
        ) : null}
        {status === "AI_ACTIVE" ? (
          <form action={take}>
            <SubmitButton size="sm" variant="secondary" pendingLabel="Prise en main…"><Hand className="size-3.5" aria-hidden /> Prendre la main</SubmitButton>
          </form>
        ) : status !== "CLOSED" ? (
          <form action={back}>
            <SubmitButton size="sm" variant="secondary" pendingLabel="Retour au setter…">
              <Bot className="size-3.5 text-ai" aria-hidden />
              <span className="sm:hidden">Au setter</span>
              <span className="max-sm:hidden">Rendre au setter</span>
            </SubmitButton>
          </form>
        ) : null}
        {(status === "NEEDS_HUMAN" || unread) && !hasDraft ? (
          <form action={done}>
            <NavFields nav={nav} />
            <SubmitButton size="sm" variant="secondary" pendingLabel="Enregistrement…">
              <Check className="size-3.5" aria-hidden />
              <span className="sm:hidden">Traité</span>
              <span className="max-sm:hidden">Marquer comme traité</span>
            </SubmitButton>
          </form>
        ) : null}
        {!["NOT_INTERESTED", "MEETING_BOOKED"].includes(stage) ? (
          <form action={notInterested}>
            <NavFields nav={nav} />
            <SubmitButton size="sm" variant="secondary" pendingLabel="Classement…">
              <ThumbsDown className="size-3.5" aria-hidden />
              <span>
                <span className="max-sm:hidden">Classer «&nbsp;</span>Pas intéressé<span className="max-sm:hidden">&nbsp;»</span>
              </span>
            </SubmitButton>
          </form>
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
 * Keyed by thread only: when the proposal changes underneath (the setter drafts again, "Refuser", a refresh), the box adopts
 * the new one unless it holds text of the user's own, which is kept as a plain reply.
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
  // The proposal this box last saw, and whether a newer one arrived while the user kept their own text.
  const [seen, setSeen] = useState(draft);
  const [newProposal, setNewProposal] = useState(false);
  if ((draft?.id ?? null) !== (seen?.id ?? null)) {
    setSeen(draft);
    const change = proposalChange({ body, previous: seen, next: draft, refused: last === "reject" });
    setMode(change.mode);
    setBody(change.body);
    setNewProposal(change.newProposal);
    if (change.adopted) setLast(null);
  }
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
    setNewProposal(false);
    caretPlaced.current = false;
    textarea.current?.focus();
  };

  const backToProposal = () => {
    setMode("proposal");
    setBody(draft?.body ?? "");
    setLast(null);
    setNewProposal(false);
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
          {/* Hidden on phones, where the messages need the room. */}
          {draft.rationale ? <span className="min-w-0 text-muted line-clamp-2 max-sm:hidden">{draft.rationale}</span> : null}
        </div>
      ) : (
        <>
          {newProposal && draft ? (
            <p role="status" className="flex items-start gap-1 text-xs font-medium text-ai">
              <Sparkles className="mt-0.5 size-3.5 shrink-0" aria-hidden /> Le setter a proposé une nouvelle réponse. Votre texte est conservé.
            </p>
          ) : null}
          <div className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1">
            {/* The placeholder says it on phones; the label stays for screen readers. */}
            <label htmlFor={REPLY_BODY_ID} className="text-sm font-medium text-ink max-sm:sr-only">
              Votre réponse
            </label>
            <label className="flex items-center gap-2 text-xs text-muted">
              {/* Keyed by status so it follows the thread (unticked once you have taken over). */}
              <input key={status} type="checkbox" name="handBack" defaultChecked={status === "AI_ACTIVE"} className={checkbox} />
              Rendre la main au setter après envoi
            </label>
          </div>
        </>
      )}

      <Textarea
        ref={textarea}
        id={REPLY_BODY_ID}
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
        // Exactly two lines on phones (2 × 26px + padding and border; rows sets the height from sm), so the thread keeps the screen.
        className={cn("max-h-64 resize-y max-lg:max-h-40 max-sm:h-[4.375rem]", proposing && "border-ai-line")}
      />

      {/* On phones the insert chips and the secondary actions are icons, so everything fits on one row with "Envoyer". */}
      <div className="flex flex-wrap items-center justify-between gap-1.5 sm:gap-2">
        <div role="group" aria-label="Insérer dans le message" className="flex flex-wrap gap-1.5 sm:gap-2">
          {bookingUrl ? (
            <Button size="sm" variant="secondary" className="rounded-full max-sm:w-11 max-sm:px-0" onClick={() => insert(bookingUrl)}>
              <Link2 className="size-3.5 max-sm:size-4" aria-hidden />
              <span className="max-sm:sr-only">Lien de réservation</span>
            </Button>
          ) : null}
          <Button size="sm" variant="secondary" className="rounded-full max-sm:w-11 max-sm:px-0" onClick={() => insert(firstName)}>
            <UserRound className="size-3.5 max-sm:size-4" aria-hidden />
            <span className="max-sm:sr-only">Prénom</span>
          </Button>
        </div>
        <div className="ml-auto flex flex-wrap items-center justify-end gap-1.5 sm:gap-2">
          {proposing ? (
            <>
              <Button size="sm" variant="ghost" className="max-sm:w-11 max-sm:px-0" onClick={writeMyself} disabled={pending}>
                <PenLine className="size-3.5 max-sm:size-4" aria-hidden />
                <span className="max-sm:sr-only">Écrire moi-même</span>
              </Button>
              <Button size="sm" variant="secondary" onClick={refuse} disabled={pending} aria-busy={rejecting}>
                {rejecting ? (
                  "Refus…"
                ) : (
                  <>
                    <X className="size-3.5 max-sm:hidden" aria-hidden />
                    <span>
                      Refuser<span className="max-sm:hidden"> la proposition</span>
                    </span>
                  </>
                )}
              </Button>
            </>
          ) : draft ? (
            <Button size="sm" variant="ghost" onClick={backToProposal} disabled={pending}>
              <Sparkles className="size-3.5 text-ai" aria-hidden />
              <span>
                Reprendre<span className="max-sm:hidden"> la proposition</span>
              </span>
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
