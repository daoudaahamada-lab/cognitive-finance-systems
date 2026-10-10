"use client";

import { Archive, Pause, Play } from "lucide-react";
import { useActionState } from "react";
import { FormMessage } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { setCampaignStatusAction } from "../actions";

export function CampaignControls({ campaignId, status }: { campaignId: string; status: string }) {
  const [launchState, launch] = useActionState(setCampaignStatusAction.bind(null, campaignId, "ACTIVE"), null);
  const [pauseState, pause] = useActionState(setCampaignStatusAction.bind(null, campaignId, "PAUSED"), null);
  const [archiveState, archive] = useActionState(setCampaignStatusAction.bind(null, campaignId, "ARCHIVED"), null);
  const state = launchState ?? pauseState ?? archiveState;

  return (
    <div className="flex flex-col items-end gap-2">
      <div className="flex flex-wrap gap-2">
        {status === "ACTIVE" ? (
          <form action={pause}>
            <SubmitButton variant="secondary" pendingLabel="…"><Pause className="size-4" /> Mettre en pause</SubmitButton>
          </form>
        ) : (
          <form action={launch}>
            <SubmitButton variant="success" pendingLabel="Lancement…"><Play className="size-4" /> {status === "DRAFT" ? "Lancer la campagne" : "Reprendre"}</SubmitButton>
          </form>
        )}
        <form action={archive} onSubmit={(e) => { if (!confirm("Archiver cette campagne ? Elle s'arrête et disparaît de la liste.")) e.preventDefault(); }}>
          <SubmitButton variant="ghost" pendingLabel="…" aria-label="Archiver"><Archive className="size-4" /></SubmitButton>
        </form>
      </div>
      <FormMessage state={state} />
    </div>
  );
}
