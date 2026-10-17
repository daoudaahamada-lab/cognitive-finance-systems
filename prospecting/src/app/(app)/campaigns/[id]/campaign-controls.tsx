"use client";

import { Archive, LoaderCircle, Pause, Play } from "lucide-react";
import { useActionState, useState } from "react";
import { useFormStatus } from "react-dom";
import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { setCampaignStatusAction } from "../actions";

type Control = "launch" | "pause" | "archive";

/**
 * Launch, pause and archive. `launchBlocked` (a blocker in the launch checklist) disables
 * 'Lancer la campagne' and 'Reprendre'; the page lists what to fix.
 */
export function CampaignControls({ campaignId, status, launchBlocked = false }: { campaignId: string; status: string; launchBlocked?: boolean }) {
  const [launchState, launch] = useActionState(setCampaignStatusAction.bind(null, campaignId, "ACTIVE"), null);
  const [pauseState, pause] = useActionState(setCampaignStatusAction.bind(null, campaignId, "PAUSED"), null);
  const [archiveState, archive] = useActionState(setCampaignStatusAction.bind(null, campaignId, "ARCHIVED"), null);
  // Show the answer to the last button used, not an older one.
  const [last, setLast] = useState<Control | null>(null);
  const state = last === "launch" ? launchState : last === "pause" ? pauseState : last === "archive" ? archiveState : null;
  const draft = status === "DRAFT";

  return (
    <div className="flex flex-col items-end gap-2">
      <div className="flex flex-wrap justify-end gap-2">
        {status === "ACTIVE" ? (
          <form action={pause} onSubmit={() => setLast("pause")}>
            <SubmitButton variant="secondary" pendingLabel="Mise en pause…">
              <Pause className="size-4" aria-hidden /> Mettre en pause
            </SubmitButton>
          </form>
        ) : (
          <form action={launch} onSubmit={() => setLast("launch")}>
            <SubmitButton
              variant="success"
              pendingLabel={draft ? "Lancement…" : "Reprise…"}
              // Only pass `disabled` when blocked: SubmitButton spreads its props after its own pending state.
              {...(launchBlocked ? { disabled: true, "aria-describedby": "launch-blocked" } : {})}
            >
              <Play className="size-4" aria-hidden /> {draft ? "Lancer la campagne" : "Reprendre"}
            </SubmitButton>
          </form>
        )}
        <form
          action={archive}
          onSubmit={(e) => {
            if (!confirm("Archiver cette campagne ? Elle s'arrête et disparaît de la liste.")) e.preventDefault();
            else setLast("archive");
          }}
        >
          <ArchiveButton />
        </form>
      </div>
      {launchBlocked && status !== "ACTIVE" ? (
        // Screen readers only: the checklist (draft) or the banner (paused) shows what to fix.
        <p id="launch-blocked" className="sr-only">
          {draft ? "Corrigez les points bloquants pour lancer." : "Corrigez les points bloquants pour reprendre."}
        </p>
      ) : null}
      <FormMessage state={state} />
    </div>
  );
}

function ArchiveButton() {
  const { pending } = useFormStatus();
  const label = pending ? "Archivage…" : "Archiver la campagne";
  return (
    <Button type="submit" variant="ghost" size="icon" disabled={pending} aria-busy={pending} aria-label={label} title={label}>
      {pending ? <LoaderCircle className="size-4 animate-spin" aria-hidden /> : <Archive className="size-4" aria-hidden />}
    </Button>
  );
}
