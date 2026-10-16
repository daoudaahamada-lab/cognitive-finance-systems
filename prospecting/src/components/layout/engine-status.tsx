import { Sparkles, TriangleAlert } from "lucide-react";
import Link from "next/link";
import { Badge, Dot } from "@/components/ui/badge";
import { formatAgo } from "@/lib/format";
import type { SemanticTone } from "@/lib/labels";
import { isSimulatorOnly, type EngineStatus } from "@/server/services/engine-status";

function engineSummary(status: EngineStatus, now: Date): { tone: SemanticTone; label: string; short: string; title: string } {
  const since = status.lastSyncAt ? `Dernière synchronisation ${formatAgo(status.lastSyncAt, now)}.` : "Aucune synchronisation pour l'instant.";
  if (status.level === "ok") {
    return {
      tone: "success",
      label: status.syncing ? "Moteur actif · synchronisation en cours" : `Moteur actif · synchro ${formatAgo(status.lastSyncAt, now)}`,
      short: "Actif",
      title: "Vela prospecte en continu tant qu'il reste ouvert sur votre ordinateur.",
    };
  }
  if (status.level === "late") {
    return { tone: "warning", label: "Moteur en retard", short: "En retard", title: `${since} Vela doit rester ouvert sur votre ordinateur pour prospecter.` };
  }
  return {
    tone: "danger",
    label: "Moteur arrêté",
    short: "Arrêté",
    title: status.lastSyncAt ? `${since} Vérifiez que Vela est lancé et qu'un compte LinkedIn est actif.` : "Aucun compte LinkedIn actif : connectez ou réactivez un compte.",
  };
}

/**
 * Header chips: engine state, LinkedIn mode and AI mode. They never wrap (the header has a fixed height):
 * short engine label below sm, LinkedIn chip from md (test mode always), AI chip from lg.
 */
export function EngineStatusChips({ status, now = new Date() }: { status: EngineStatus; now?: Date }) {
  const engine = engineSummary(status, now);
  const simulated = isSimulatorOnly(status);
  const engineText = (
    <>
      <Dot tone={engine.tone} />
      <span className="sm:hidden">
        <span className="sr-only">Moteur </span>
        {engine.short}
      </span>
      <span className="hidden truncate sm:inline">{engine.label}</span>
    </>
  );
  return (
    <div className="flex min-w-0 items-center gap-2">
      {status.level === "ok" ? (
        <span title={engine.title} className="inline-flex min-w-0 items-center gap-1.5 text-xs font-medium text-ink-2">
          {engineText}
        </span>
      ) : (
        <Link
          href="/accounts"
          title={engine.title}
          className="inline-flex min-w-0 items-center gap-1.5 rounded-control text-xs font-medium text-ink-2 hover:text-ink hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 pointer-coarse:min-h-11"
        >
          {engineText}
        </Link>
      )}
      {simulated ? (
        <Badge tone="warning" className="shrink-0">
          <TriangleAlert className="size-3" aria-hidden /> Mode test<span className="sr-only md:not-sr-only"> · LinkedIn simulé</span>
        </Badge>
      ) : status.providers.length > 0 ? (
        <Badge tone="neutral" className="hidden shrink-0 md:inline-flex">
          LinkedIn : votre compte
        </Badge>
      ) : (
        <Link href="/accounts" className="hidden shrink-0 rounded-md hover:opacity-80 md:inline-flex">
          <Badge tone="neutral">LinkedIn : aucun compte</Badge>
        </Link>
      )}
      {status.agentMode === "claude" ? (
        <Badge tone="ai" className="hidden shrink-0 lg:inline-flex">
          <Sparkles className="size-3" aria-hidden /> IA : Claude
        </Badge>
      ) : (
        <Badge tone="neutral" className="hidden shrink-0 lg:inline-flex">
          IA : réponses types
        </Badge>
      )}
    </div>
  );
}

/** One line per paused or failing account, above the page content. */
export function AccountAlerts({ status }: { status: EngineStatus }) {
  const lines = [
    ...status.pausedAccounts
      .filter((a) => a.statusReason)
      .map((a) => ({ id: a.id, text: `${a.fullName} est en pause : ${a.statusReason}` })),
    ...status.erroredAccounts.map((a) => ({ id: a.id, text: `${a.fullName} : la dernière synchronisation a échoué (${a.lastError})` })),
  ];
  if (lines.length === 0) return null;
  return (
    <div role="region" aria-label="Comptes à réparer" className="border-b border-danger-line bg-danger-soft">
      {lines.map((line) => (
        <p key={line.id} className="flex items-start gap-2 px-4 py-2 text-sm text-danger sm:px-8">
          <TriangleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
          <span className="min-w-0 flex-1 break-words">{line.text}</span>
          <Link href={`/accounts#${line.id}`} className="shrink-0 font-semibold underline underline-offset-2 hover:no-underline">
            Réparer
          </Link>
        </p>
      ))}
    </div>
  );
}
