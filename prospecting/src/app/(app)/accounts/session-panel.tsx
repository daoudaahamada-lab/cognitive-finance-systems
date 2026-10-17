import { CircleCheck, CircleDashed, KeyRound, TriangleAlert } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { SESSION_TO_OPEN_REASON } from "@/server/services/accounts";
import { CopyCommand, SessionCheck, SessionForm } from "./account-forms";

const dayMonth = new Intl.DateTimeFormat("fr-FR", { day: "numeric", month: "short" });
const dayMonthYear = new Intl.DateTimeFormat("fr-FR", { day: "numeric", month: "short", year: "numeric" });
const hourMinute = new Intl.DateTimeFormat("fr-FR", { hour: "2-digit", minute: "2-digit" });

/** "le 16 oct. à 10:42" (with the year when it is not the current one). */
function onDay(date: Date, now: Date): string {
  const day = (date.getFullYear() === now.getFullYear() ? dayMonth : dayMonthYear).format(date);
  return `le ${day} à ${hourMinute.format(date)}`;
}

type SessionAccount = {
  id: string;
  needsSession: boolean;
  statusReason: string | null;
  lastDiagnosedAt: Date | null;
  lastDiagnosisOk: boolean | null;
};

function Status({ icon, tone, title, children }: { icon: ReactNode; tone: "success" | "warning" | "info"; title: string; children?: ReactNode }) {
  const color = { success: "text-success", warning: "text-warning", info: "text-info" }[tone];
  return (
    <div className="flex gap-2.5">
      <span className={cn("mt-0.5 shrink-0", color)}>{icon}</span>
      <div className="min-w-0">
        <p className={cn("text-sm font-semibold", color)}>{title}</p>
        {children ? <p className="mt-0.5 text-sm text-ink-2">{children}</p> : null}
      </div>
    </div>
  );
}

function Step({ n, children }: { n: number; children: ReactNode }) {
  return (
    <li className="flex gap-3">
      <span aria-hidden className="flex size-6 shrink-0 items-center justify-center rounded-full bg-surface text-xs font-semibold text-warning ring-1 ring-inset ring-warning-line">
        {n}
      </span>
      <div className="min-w-0 flex-1 pt-0.5">{children}</div>
    </li>
  );
}

const kbd = "rounded border border-line bg-surface px-1 font-mono text-xs text-ink";

/**
 * 'Session LinkedIn' block of a browser account, in three states:
 * (a) session to open: the terminal steps or a li_at cookie, and nothing else to click;
 * (b) open but never checked: the check is the primary action;
 * (c) checked: when, and whether everything was recognised.
 */
export function SessionPanel({ account, now = new Date() }: { account: SessionAccount; now?: Date }) {
  const headingId = `session-${account.id}`;
  return (
    <section
      aria-labelledby={headingId}
      className={cn("rounded-card border p-4", account.needsSession ? "border-warning-line bg-warning-soft" : "border-line bg-surface-2")}
    >
      <h3 id={headingId} className="mb-3 flex items-center gap-2 text-sm font-semibold text-ink">
        <KeyRound className="size-4 text-muted" aria-hidden /> Session LinkedIn
      </h3>
      {account.needsSession ? <OpenSession account={account} /> : <CheckedSession account={account} now={now} />}
    </section>
  );
}

function OpenSession({ account }: { account: SessionAccount }) {
  // An expired session or a security check says why; a new account needs no explanation beyond the steps.
  const reason = account.statusReason && account.statusReason !== SESSION_TO_OPEN_REASON ? account.statusReason : null;
  return (
    <div className="space-y-4">
      <Status icon={<TriangleAlert className="size-4" aria-hidden />} tone="warning" title="Session à ouvrir">
        {reason ?? "Vela ne peut rien faire sur LinkedIn tant que la session de ce compte n'est pas ouverte."}
      </Status>
      <div>
        <p className="text-sm font-medium text-ink">Depuis le terminal de Vela</p>
        <ol className="mt-2 space-y-3 text-sm text-ink-2">
          <Step n={1}>
            Arrêtez Vela : <kbd className={kbd}>Ctrl</kbd> + <kbd className={kbd}>C</kbd> dans son terminal.
          </Step>
          <Step n={2}>
            Lancez cette commande, puis connectez-vous à LinkedIn dans la fenêtre qui s&apos;ouvre (mot de passe, code de sécurité) :
            <CopyCommand command={`npm run linkedin:login -- --account ${account.id}`} />
          </Step>
          <Step n={3}>
            Relancez Vela avec <code className="rounded bg-surface px-1 font-mono text-xs text-ink">npm run local</code>. Le compte redevient actif tout seul.
          </Step>
        </ol>
      </div>
      <div className="flex items-center gap-3 text-xs font-medium uppercase tracking-wide text-muted" aria-hidden>
        <span className="h-px flex-1 bg-warning-line" />
        ou
        <span className="h-px flex-1 bg-warning-line" />
      </div>
      <div>
        <p className="mb-2 text-sm font-medium text-ink">Collez le cookie li_at de votre session</p>
        <SessionForm accountId={account.id} submitLabel="Ouvrir la session" />
      </div>
    </div>
  );
}

function CheckedSession({ account, now }: { account: SessionAccount; now: Date }) {
  const checked = account.lastDiagnosedAt !== null && account.lastDiagnosisOk !== null;
  const status = !checked ? (
    <Status icon={<CircleDashed className="size-4" aria-hidden />} tone="info" title="Session ouverte, non vérifiée">
      Vérifiez que Vela lit bien vos pages LinkedIn avant de lancer une campagne (environ 1 minute).
    </Status>
  ) : account.lastDiagnosisOk ? (
    <Status icon={<CircleCheck className="size-4" aria-hidden />} tone="success" title={`Vérifiée ${onDay(account.lastDiagnosedAt!, now)}`}>
      Vela lit correctement vos pages LinkedIn.
    </Status>
  ) : (
    <Status icon={<TriangleAlert className="size-4" aria-hidden />} tone="warning" title={`Points non reconnus ${onDay(account.lastDiagnosedAt!, now)}`}>
      LinkedIn a peut-être changé son interface, ou la session a été refusée. N&apos;activez pas de campagne avant une vérification réussie.
    </Status>
  );
  return (
    // Same component in every state, so the details of a check survive the refresh that stores its result.
    <SessionCheck accountId={account.id} primary={account.lastDiagnosisOk !== true}>
      {status}
    </SessionCheck>
  );
}
