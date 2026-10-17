"use client";

import { Check, RotateCcw, UserX, X } from "lucide-react";
import { SubmitButton } from "@/components/ui/submit-button";
import { cn } from "@/lib/cn";
import { meetingStatusAction } from "./actions";

/** "Effectué" and "Non honoré" for a meeting that has passed. Full width on phones. */
export function OutcomeButtons({ meetingId, name, className }: { meetingId: string; name: string; className?: string }) {
  return (
    <div className={cn("grid grid-cols-2 gap-2 md:flex md:shrink-0", className)}>
      <form action={meetingStatusAction.bind(null, meetingId, "COMPLETED")}>
        <SubmitButton variant="secondary" size="sm" className="w-full" aria-label={`Effectué – ${name}`} pendingLabel="Enregistrement…">
          <Check className="size-3.5 text-success" aria-hidden /> Effectué
        </SubmitButton>
      </form>
      <form action={meetingStatusAction.bind(null, meetingId, "NO_SHOW")}>
        <SubmitButton variant="secondary" size="sm" className="w-full" aria-label={`Non honoré – ${name}`} pendingLabel="Enregistrement…">
          <UserX className="size-3.5 text-warning" aria-hidden /> Non honoré
        </SubmitButton>
      </form>
    </div>
  );
}

/** "Annuler le RDV", after a confirmation. */
export function CancelMeetingButton({ meetingId, name, when, className }: { meetingId: string; name: string; when: string; className?: string }) {
  return (
    <form
      className={className}
      action={meetingStatusAction.bind(null, meetingId, "CANCELED")}
      onSubmit={(event) => {
        if (!confirm(`Annuler le rendez-vous avec ${name} (${when}) ?`)) event.preventDefault();
      }}
    >
      <SubmitButton variant="ghost" size="sm" className="w-full" aria-label={`Annuler le RDV – ${name}`} pendingLabel="Annulation…">
        <X className="size-3.5" aria-hidden /> Annuler le RDV
      </SubmitButton>
    </form>
  );
}

/**
 * Undoes 'Annuler le RDV': the meeting is scheduled again, so it returns to 'À venir',
 * or to 'À confirmer' when its time has passed.
 */
export function RestoreMeetingButton({ meetingId, name }: { meetingId: string; name: string }) {
  return (
    <form action={meetingStatusAction.bind(null, meetingId, "SCHEDULED")}>
      <SubmitButton variant="ghost" size="sm" className="w-full" aria-label={`Rétablir – ${name}`} pendingLabel="Enregistrement…">
        <RotateCcw className="size-3.5" aria-hidden /> Rétablir
      </SubmitButton>
    </form>
  );
}

/** Corrects a recorded outcome: a held meeting becomes a no-show, and the other way round. */
export function CorrectOutcomeButton({ meetingId, name, status }: { meetingId: string; name: string; status: "COMPLETED" | "NO_SHOW" }) {
  const next = status === "COMPLETED" ? "NO_SHOW" : "COMPLETED";
  const label = next === "COMPLETED" ? "Marquer effectué" : "Marquer non honoré";
  return (
    <form action={meetingStatusAction.bind(null, meetingId, next)}>
      <SubmitButton variant="ghost" size="sm" className="w-full" aria-label={`${label} – ${name}`} pendingLabel="Enregistrement…">
        {label}
      </SubmitButton>
    </form>
  );
}
