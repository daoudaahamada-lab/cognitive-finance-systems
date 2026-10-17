"use client";

import { useActionState, useState } from "react";
import { Field, FormMessage, Input, Textarea } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { logMeetingAction, manualStageAction, notesAction } from "../actions";
import { manualStageActions } from "../stage-rules";

/** Manual stage changes; renders nothing when none applies to the stage. */
export function StageButtons({ prospectId, stage }: { prospectId: string; stage: string }) {
  const [exState, exclude] = useActionState(manualStageAction.bind(null, prospectId, "exclude"), null);
  const [rqState, requalify] = useActionState(manualStageAction.bind(null, prospectId, "requalify"), null);
  const [niState, notInterested] = useActionState(manualStageAction.bind(null, prospectId, "not_interested"), null);
  const state = exState?.error ? exState : rqState?.error ? rqState : niState?.error ? niState : null;
  const actions = manualStageActions(stage);
  if (actions.length === 0 && !state) return null;
  return (
    <div className="space-y-2">
      <FormMessage state={state} />
      {actions.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {actions.includes("exclude") ? (
            <form action={exclude}>
              <SubmitButton variant="danger" size="sm">Ne pas contacter</SubmitButton>
            </form>
          ) : null}
          {actions.includes("requalify") ? (
            <form action={requalify}>
              <SubmitButton variant="secondary" size="sm">Requalifier</SubmitButton>
            </form>
          ) : null}
          {actions.includes("not_interested") ? (
            <form action={notInterested}>
              <SubmitButton variant="secondary" size="sm">Pas intéressé</SubmitButton>
            </form>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

/**
 * Logs a meeting agreed outside Vela. The browser also sends the instant as ISO (startsAtIso),
 * so the local time typed is kept whatever the server's time zone.
 */
export function MeetingForm({ prospectId }: { prospectId: string }) {
  const [state, action] = useActionState(logMeetingAction.bind(null, prospectId), null);
  const [iso, setIso] = useState("");
  return (
    <form action={action} className="space-y-2">
      {state?.ok ? <FormMessage state={state} /> : null}
      <Field label="Rendez-vous pris en dehors de Vela" htmlFor="meeting-starts-at" error={state?.error}>
        <Input
          id="meeting-starts-at"
          name="startsAt"
          type="datetime-local"
          required
          onChange={(event) => {
            const local = new Date(event.target.value);
            setIso(Number.isNaN(local.getTime()) ? "" : local.toISOString());
          }}
        />
      </Field>
      <input type="hidden" name="startsAtIso" value={iso} />
      <SubmitButton variant="secondary" size="sm" pendingLabel="Enregistrement…">
        Ajouter le rendez-vous
      </SubmitButton>
    </form>
  );
}

export function NotesForm({ prospectId, notes }: { prospectId: string; notes: string }) {
  const [state, action] = useActionState(notesAction.bind(null, prospectId), null);
  return (
    <form action={action} className="space-y-2">
      <FormMessage state={state} />
      <Textarea name="notes" rows={4} defaultValue={notes} aria-label="Notes" placeholder="Contexte, prochaines étapes…" />
      <SubmitButton variant="secondary" size="sm">Enregistrer</SubmitButton>
    </form>
  );
}
