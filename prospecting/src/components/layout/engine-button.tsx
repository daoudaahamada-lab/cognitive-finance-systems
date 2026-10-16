"use client";

import { RefreshCw } from "lucide-react";
import { useActionState, useEffect, useState } from "react";
import { runEngineNow, type EngineRunState } from "@/app/(app)/engine-actions";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/cn";

/** Forces an engine pass now and shows its one-line summary under the button for a few seconds. */
export function EngineButton() {
  const [state, action, pending] = useActionState(runEngineNow, null);
  const [dismissed, setDismissed] = useState<EngineRunState>(null);
  const visible = state !== null && state !== dismissed;

  useEffect(() => {
    if (!state) return;
    const timer = setTimeout(() => setDismissed(state), 10_000);
    return () => clearTimeout(timer);
  }, [state]);

  const label = pending ? "Synchronisation…" : "Synchroniser maintenant";
  return (
    <form action={action} className="relative">
      <Button
        type="submit"
        variant="secondary"
        size="sm"
        disabled={pending}
        aria-busy={pending}
        aria-label={label}
        title="Vela travaille déjà en continu. Ce bouton force une vérification immédiate."
      >
        <RefreshCw className={cn("size-3.5", pending && "animate-spin")} aria-hidden />
        <span className="hidden sm:inline">{label}</span>
      </Button>
      <p
        role="status"
        className={
          visible
            ? cn(
                "absolute right-0 top-full z-30 mt-2 w-max max-w-[min(24rem,calc(100vw-2rem))] rounded-control border px-3 py-2 text-xs shadow-pop",
                state.ok ? "border-line bg-surface text-ink" : "border-danger-line bg-danger-soft text-danger",
              )
            : "sr-only"
        }
      >
        {visible ? state.message : ""}
      </p>
    </form>
  );
}
