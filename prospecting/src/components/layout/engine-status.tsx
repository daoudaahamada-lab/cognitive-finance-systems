import { Sparkles, TriangleAlert } from "lucide-react";
import Link from "next/link";
import { Badge, Dot } from "@/components/ui/badge";
import { formatAgo } from "@/lib/format";
import type { SemanticTone } from "@/lib/labels";
import { isSimulatorOnly, type EngineStatus } from "@/server/services/engine-status";

function engineSummary(status: EngineStatus, now: Date): { tone: SemanticTone; label: string; title: string } {
  const since = status.lastSyncAt ? `Dernière synchronisation ${formatAgo(status.lastSyncAt, now)}.` : "Aucune synchronisation pour l'instant.";
  if (status.level === "ok") {
    return {
      tone: "success",
      label: status.syncing ? "Moteur actif · synchronisation en cours" : `Moteur actif · synchro ${formatAgo(status.lastSyncAt, now)}`,
      title: "Vela prospecte en continu tant qu'il reste ouvert sur votre ordinateur.",
    };
  }
  if (status.level === "late") {
    return { tone: "warning", label: "Moteur en retard", title: `${since} Vela doit rester ouvert sur votre ordinateur pour prospecter.` };
  }
  return {
    tone: "danger",
    label: "Moteur arrêté",
    title: status.lastSyncAt ? `${since} Vérifiez que Vela est lancé et qu'un compte LinkedIn est actif.` : "Aucun compte LinkedIn actif : connectez ou réactivez un compte.",
  };
}

/** Header chips: engine state, LinkedIn mode and AI mode. Below lg, only the engine dot. */
export function EngineStatusChips({ status, now = new Date() }: { status: EngineStatus; now?: Date }) {
  const engine = engineSummary(status, now);
  const simulated = isSimulatorOnly(status);
  return (
    <>
      <Link
        href="/accounts"
        title={engine.title}
        className="flex size-9 items-center justify-center rounded-full hover:bg-canvas focus-visible:outline-2 focus-visible:outline-brand-600 pointer-coarse:size-11 lg:hidden"
      >
        <Dot tone={engine.tone} className="size-2.5" />
        <span className="sr-only">{engine.label}</span>
      </Link>
      <div className="hidden min-w-0 flex-wrap items-center gap-2 lg:flex">
        {status.level === "ok" ? (
          <span title={engine.title} className="inline-flex items-center gap-1.5 text-xs font-medium text-ink-2">
            <Dot tone="success" />
            {engine.label}
          </span>
        ) : (
          <Link href="/accounts" title={engine.title} className="inline-flex items-center gap-1.5 text-xs font-medium text-ink-2 hover:text-ink hover:underline">
            <Dot tone={engine.tone} />
            {engine.label}
          </Link>
        )}
        {simulated ? (
          <Badge tone="warning">
            <TriangleAlert className="size-3" aria-hidden /> Mode test · LinkedIn simulé
          </Badge>
        ) : status.providers.length > 0 ? (
          <Badge tone="neutral">LinkedIn : votre compte</Badge>
        ) : (
          <Link href="/accounts" className="rounded-md hover:opacity-80">
            <Badge tone="neutral">LinkedIn : aucun compte</Badge>
          </Link>
        )}
        {status.agentMode === "claude" ? (
          <Badge tone="ai">
            <Sparkles className="size-3" aria-hidden /> IA : Claude
          </Badge>
        ) : (
          <Badge tone="neutral">IA : réponses types</Badge>
        )}
      </div>
    </>
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
