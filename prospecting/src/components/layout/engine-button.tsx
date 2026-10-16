"use client";

import { RefreshCw, X } from "lucide-react";
import Link from "next/link";
import { useActionState, useEffect, useState } from "react";
import { runEngineNow, type EngineRunState } from "@/app/(app)/engine-actions";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/cn";

/**
 * Forces an engine pass now and shows its one-line summary under the button: a success for a few seconds,
 * an error (with a link to the accounts) until it is closed, since it covers the account banner.
 */
export function EngineButton() {
  const [state, action, pending] = useActionState(runEngineNow, null);
  const [dismissed, setDismissed] = useState<EngineRunState>(null);
  const visible = state !== null && state !== dismissed;
  const dismiss = () => setDismissed(state);

  useEffect(() => {
    if (!state?.ok) return;
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
        <span className="hidden xl:inline">{label}</span>
      </Button>
      <div
        className={
          visible
            ? cn(
                "absolute right-0 top-full z-30 mt-2 flex w-max max-w-[min(24rem,calc(100vw-2rem))] items-start gap-2 rounded-control border py-1.5 pr-1.5 pl-3 text-xs shadow-pop",
                state.ok ? "border-line bg-surface text-ink" : "border-danger-line bg-danger-soft text-danger",
              )
            : "sr-only"
        }
      >
        <p role="status" className="min-w-0 flex-1 py-0.5">
          {visible ? state.message : ""}
          {visible && !state.ok ? (
            <>
              {" · "}
              <Link href="/accounts" onClick={dismiss} className="font-semibold underline underline-offset-2 hover:no-underline">
                Voir les comptes
              </Link>
            </>
          ) : null}
        </p>
        {visible ? (
          <button
            type="button"
            onClick={dismiss}
            aria-label="Fermer"
            className="shrink-0 rounded p-0.5 opacity-70 hover:opacity-100 focus-visible:outline-2 focus-visible:outline-brand-600 pointer-coarse:p-2"
          >
            <X className="size-3.5" aria-hidden />
          </button>
        ) : null}
      </div>
    </form>
  );
}
