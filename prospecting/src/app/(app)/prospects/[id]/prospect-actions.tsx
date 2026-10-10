"use client";

import { useActionState } from "react";
import { Field, FormMessage, Input, Textarea } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { logMeetingAction, manualStageAction, notesAction } from "../actions";

export function StageButtons({ prospectId, stage }: { prospectId: string; stage: string }) {
  const [exState, exclude] = useActionState(manualStageAction.bind(null, prospectId, "exclude"), null);
  const [rqState, requalify] = useActionState(manualStageAction.bind(null, prospectId, "requalify"), null);
  const [niState, notInterested] = useActionState(manualStageAction.bind(null, prospectId, "not_interested"), null);
  const state = exState?.error ? exState : rqState?.error ? rqState : niState?.error ? niState : null;
  return (
    <div className="space-y-2">
      <FormMessage state={state} />
      <div className="flex flex-wrap gap-2">
        {["NEW", "QUALIFIED", "INVITED"].includes(stage) ? (
          <form action={exclude}><SubmitButton variant="danger" size="sm">Ne pas contacter</SubmitButton></form>
        ) : null}
        {stage === "DISQUALIFIED" ? (
          <form action={requalify}><SubmitButton variant="secondary" size="sm">Requalifier</SubmitButton></form>
        ) : null}
        {!["NOT_INTERESTED", "DISQUALIFIED", "MEETING_BOOKED"].includes(stage) ? (
          <form action={notInterested}><SubmitButton variant="secondary" size="sm">Pas intéressé</SubmitButton></form>
        ) : null}
      </div>
    </div>
  );
}

export function MeetingForm({ prospectId }: { prospectId: string }) {
  const [state, action] = useActionState(logMeetingAction.bind(null, prospectId), null);
  return (
    <form action={action} className="space-y-2">
      <FormMessage state={state} />
      <Field label="Rendez-vous pris hors setter" htmlFor="startsAt">
        <Input id="startsAt" name="startsAt" type="datetime-local" required />
      </Field>
      <SubmitButton variant="secondary" size="sm">Enregistrer le RDV</SubmitButton>
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
