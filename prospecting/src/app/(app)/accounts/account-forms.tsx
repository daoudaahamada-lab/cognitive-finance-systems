"use client";

import type { LinkedInAccount } from "@prisma/client";
import { Check, CircleCheck, CircleX, Copy, Pause, Play } from "lucide-react";
import { createContext, useActionState, useContext, useEffect, useState, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Field, FormMessage, Input, Select, checkbox } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { ACCOUNT_TYPES, WEEKDAYS } from "@/lib/labels";
import { WEEKLY_INVITE_CAP } from "@/server/domain/quotas";
import type { ActionState } from "@/server/services/errors";
import { connectAccountAction, diagnoseAccountAction, setAccountStatusAction, updateAccountAction, updateSessionAction } from "./actions";

function CookieHelp() {
  return (
    <details className="rounded-control bg-canvas px-3 py-2 text-xs text-muted">
      <summary className="cursor-pointer select-none font-medium text-ink pointer-coarse:py-2">Où trouver le cookie li_at ?</summary>
      <ol className="mt-2 list-decimal space-y-1 pl-4">
        <li>Connectez-vous à LinkedIn dans Chrome, sur votre ordinateur.</li>
        <li>Ouvrez les outils de développement (F12), onglet Application, puis Cookies → https://www.linkedin.com.</li>
        <li>Copiez la valeur du cookie <code>li_at</code> et collez-la ici.</li>
      </ol>
      <p className="mt-2">
        Ce cookie donne accès à votre compte : il reste sur votre ordinateur, dans le navigateur dédié de Vela. Si vous vous déconnectez de LinkedIn dans le navigateur où vous
        l&apos;avez copié, il ne fonctionnera plus.
      </p>
    </details>
  );
}

export function ConnectAccountForm() {
  const [state, action] = useActionState(connectAccountAction, null);
  const [provider, setProvider] = useState<"browser" | "simulator">("browser");
  const err = state?.fieldErrors ?? {};
  // The new account's card holds the next step (open or verify the session): bring it into view.
  const newAccountId = state?.accountId;
  useEffect(() => {
    if (newAccountId) document.getElementById(newAccountId)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }, [newAccountId]);
  return (
    <form action={action} className="space-y-4">
      <FormMessage state={state} />
      <fieldset className="grid gap-2 sm:grid-cols-2">
        <legend className="sr-only">Mode de connexion</legend>
        {(
          [
            ["browser", "Mon compte LinkedIn", "Vela utilise votre compte dans un navigateur dédié sur votre ordinateur, à un rythme humain."],
            ["simulator", "Simulateur", "Aucun vrai compte : profils et réponses simulés, pour tester le parcours."],
          ] as const
        ).map(([value, label, description]) => (
          <label key={value} className="flex cursor-pointer gap-3 rounded-control border border-line p-3 has-[:checked]:border-brand-600 has-[:checked]:bg-brand-50">
            <input type="radio" name="provider" value={value} checked={provider === value} onChange={() => setProvider(value)} className={`${checkbox} mt-0.5`} />
            <span>
              <span className="block text-sm font-medium text-ink">{label}</span>
              <span className="block text-xs text-ink-2">{description}</span>
            </span>
          </label>
        ))}
      </fieldset>
      {provider === "browser" ? (
        <>
          <Field
            label="Cookie de session li_at"
            htmlFor="sessionCookie"
            error={err.sessionCookie}
            hint="Facultatif. Sans cookie, vous ouvrirez la session vous-même depuis le terminal de Vela : la carte du compte vous guidera."
          >
            <Input id="sessionCookie" name="sessionCookie" type="password" autoComplete="off" spellCheck={false} placeholder="AQEDAR…" />
          </Field>
          <CookieHelp />
        </>
      ) : null}
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Nom affiché" htmlFor="fullName" error={err.fullName} hint={provider === "browser" ? "Lu sur LinkedIn quand vous collez un cookie." : undefined}>
          <Input id="fullName" name="fullName" autoComplete="name" placeholder="Alex Martin" />
        </Field>
        <Field label="Type de compte" htmlFor="accountType" hint="Il fixe le plafond d'invitations par semaine.">
          <Select id="accountType" name="accountType" defaultValue="FREE">
            {Object.entries(ACCOUNT_TYPES).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </Select>
        </Field>
      </div>
      {provider === "simulator" ? (
        <Field label="Titre du profil" htmlFor="headline">
          <Input id="headline" name="headline" placeholder="Fondateur · J'aide les PME à …" />
        </Field>
      ) : null}
      <SubmitButton pendingLabel={provider === "browser" ? "Vérification de la session…" : "Connexion…"}>Connecter le compte</SubmitButton>
    </form>
  );
}

/** A shell command with a copy button; the confirmation is announced to screen readers. */
export function CopyCommand({ command }: { command: string }) {
  const [copied, setCopied] = useState<"yes" | "no" | null>(null);
  useEffect(() => {
    if (!copied) return;
    const timer = setTimeout(() => setCopied(null), 2000);
    return () => clearTimeout(timer);
  }, [copied]);
  return (
    <span className="mt-1.5 flex items-center gap-2 rounded-control border border-line bg-surface py-1 pl-3 pr-1">
      <code className="min-w-0 flex-1 break-all font-mono text-xs leading-5 text-ink">{command}</code>
      <Button
        variant="ghost"
        size="sm"
        aria-label={`Copier la commande ${command}`}
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(command);
            setCopied("yes");
          } catch {
            setCopied("no");
          }
        }}
      >
        {copied === "yes" ? <Check className="size-3.5 text-success" aria-hidden /> : <Copy className="size-3.5" aria-hidden />}
        <span aria-hidden>{copied === "yes" ? "Copié" : "Copier"}</span>
      </Button>
      <span aria-live="polite" className="sr-only">
        {copied === "yes" ? "Copié dans le presse-papiers" : copied === "no" ? "Copie impossible : sélectionnez la commande à la main." : ""}
      </span>
    </span>
  );
}

type SessionAction = { state: ActionState; action: (form: FormData) => void };

/** The 'Ouvrir la session' action of a 'Session LinkedIn' block, held above the block's state switch. */
const OpenSessionContext = createContext<SessionAction | null>(null);

/**
 * Read-only check run on LinkedIn by Vela's browser: tells whether Vela still understands the pages.
 * `children` is the stored result (server-rendered); this component keeps the details of the last run,
 * so it stays mounted while the page refreshes with the new result.
 */
export function SessionCheck({ accountId, primary, children }: { accountId: string; primary: boolean; children: ReactNode }) {
  const [state, action] = useActionState(diagnoseAccountAction.bind(null, accountId), null);
  // Mounted right after 'Ouvrir la session' replaced its form: focus lands on this next step, not on the page.
  const sessionJustOpened = useContext(OpenSessionContext)?.state?.ok === true;
  const failed = state?.lines?.filter((line) => !line.ok).length ?? 0;
  return (
    <form action={action} className="space-y-3">
      {children}
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <SubmitButton
          variant={primary ? "primary" : "secondary"}
          size="sm"
          autoFocus={sessionJustOpened}
          pendingLabel="Vérification sur LinkedIn… (environ 1 minute)"
        >
          Vérifier la connexion LinkedIn
        </SubmitButton>
        <p className="text-xs text-muted">Ouvre votre session, une recherche, un profil, vos relations et vos messages. N&apos;envoie rien.</p>
      </div>
      {state?.error ? <FormMessage state={state} /> : null}
      {state?.lines ? (
        <div role="status" className={`space-y-2 rounded-control border px-3 py-2 text-sm ${failed ? "border-warning-line bg-warning-soft" : "border-success-line bg-success-soft"}`}>
          <p className={`font-semibold ${failed ? "text-warning" : "text-success"}`}>
            {failed
              ? `${failed} point${failed > 1 ? "s" : ""} non reconnu${failed > 1 ? "s" : ""} : LinkedIn a peut-être changé son interface. N'activez pas de campagne pour l'instant.`
              : "Tout est reconnu : vous pouvez lancer une campagne."}
          </p>
          <ul className="space-y-1 text-ink-2">
            {state.lines.map((line) => (
              <li key={line.check} className="flex gap-2">
                {line.ok ? (
                  <CircleCheck className="mt-0.5 size-4 shrink-0 text-success" role="img" aria-label="Reconnu" />
                ) : (
                  <CircleX className="mt-0.5 size-4 shrink-0 text-danger" role="img" aria-label="Non reconnu" />
                )}
                <span className="min-w-0 break-words">
                  <strong className="font-semibold text-ink">{line.check}</strong> : {line.detail}
                </span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </form>
  );
}

/**
 * Wraps every state of a 'Session LinkedIn' block and owns its 'Ouvrir la session' action. A new session
 * makes the account active, so the refresh swaps the cookie form for the check in the same commit: the
 * confirmation lives here to survive it, and SessionCheck takes the focus the vanished button held.
 */
export function SessionScope({ accountId, children }: { accountId: string; children: ReactNode }) {
  const [state, action] = useActionState(updateSessionAction.bind(null, accountId), null);
  return (
    <OpenSessionContext value={{ state, action }}>
      {/* Always mounted, so the confirmation is announced when it appears. */}
      <div role="status">
        {state?.ok && state.message ? (
          <p className="mb-3 rounded-control border border-success-line bg-success-soft px-3 py-2 text-sm text-success">{state.message}</p>
        ) : null}
      </div>
      {children}
    </OpenSessionContext>
  );
}

/** 'Ouvrir la session' (session to open), inside a SessionScope: the scope shows its success. */
export function OpenSessionForm({ accountId }: { accountId: string }) {
  const scope = useContext(OpenSessionContext);
  if (!scope) throw new Error("OpenSessionForm must be rendered inside SessionScope.");
  return <SessionCookieForm accountId={accountId} submitLabel="Ouvrir la session" state={scope.state?.ok ? null : scope.state} action={scope.action} />;
}

/** Replaces the LinkedIn session of an account that has one ('Mettre à jour la session'). */
export function SessionForm({ accountId }: { accountId: string }) {
  const [state, action] = useActionState(updateSessionAction.bind(null, accountId), null);
  return <SessionCookieForm accountId={accountId} submitLabel="Mettre à jour la session" state={state} action={action} />;
}

/** Opens or replaces the LinkedIn session with a li_at cookie. The cookie is never shown again. */
function SessionCookieForm({ accountId, submitLabel, state, action }: SessionAction & { accountId: string; submitLabel: string }) {
  return (
    <form action={action} className="space-y-3">
      <FormMessage state={state} />
      <Field label="Cookie li_at" htmlFor={`cookie-${accountId}`} error={state?.fieldErrors?.sessionCookie}>
        <Input id={`cookie-${accountId}`} name="sessionCookie" type="password" autoComplete="off" spellCheck={false} placeholder="AQEDAR…" required />
      </Field>
      <CookieHelp />
      <SubmitButton variant="secondary" size="sm" pendingLabel="Ouverture de la session…">
        {submitLabel}
      </SubmitButton>
    </form>
  );
}

type ActionTarget = "pause" | "resume" | "disconnect";

function disconnectQuestion(name: string, activeCampaigns: number, sessionHint: string | null): string {
  const impact =
    activeCampaigns === 0
      ? "Le compte disparaîtra de Vela."
      : activeCampaigns === 1
        ? "Sa campagne active sera mise en pause et le compte disparaîtra."
        : `Ses ${activeCampaigns} campagnes actives seront mises en pause et le compte disparaîtra.`;
  // A cookie-connected account can have no name (the card then reads "Compte LinkedIn").
  return [`Déconnecter ${name.trim() || "ce compte"} ?`, impact, sessionHint].filter(Boolean).join(" ");
}

/**
 * Pause or resume, replace the session, disconnect. 'Réactiver' is hidden while the LinkedIn session
 * is still to open (the server refuses it too), and disconnecting asks for confirmation.
 */
export function AccountActions({
  account,
}: {
  account: { id: string; fullName: string; provider: string; status: string; needsSession: boolean; activeCampaigns: number };
}) {
  const [pauseState, pause] = useActionState(setAccountStatusAction.bind(null, account.id, "PAUSED"), null);
  const [resumeState, resume] = useActionState(setAccountStatusAction.bind(null, account.id, "ACTIVE"), null);
  const [disconnectState, disconnect] = useActionState(setAccountStatusAction.bind(null, account.id, "DISCONNECTED"), null);
  const [last, setLast] = useState<ActionTarget | null>(null);
  const [sessionOpen, setSessionOpen] = useState(false);
  const state = last === "pause" ? pauseState : last === "resume" ? resumeState : last === "disconnect" ? disconnectState : null;
  const browser = account.provider === "browser";
  const canUpdateSession = browser && !account.needsSession;
  const sessionHint = !browser
    ? null
    : account.needsSession
      ? "Pour une session à ouvrir, suivez plutôt les étapes « Session LinkedIn »."
      : "Pour une session expirée, utilisez plutôt « Mettre à jour la session ».";
  const formId = `session-form-${account.id}`;

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {account.status === "ACTIVE" ? (
          <form action={pause} onSubmit={() => setLast("pause")}>
            <SubmitButton variant="secondary" size="sm" pendingLabel="Mise en pause…">
              <Pause className="size-3.5" aria-hidden /> Mettre en pause
            </SubmitButton>
          </form>
        ) : !account.needsSession ? (
          <form action={resume} onSubmit={() => setLast("resume")}>
            <SubmitButton variant="secondary" size="sm" pendingLabel="Réactivation…">
              <Play className="size-3.5" aria-hidden /> Réactiver
            </SubmitButton>
          </form>
        ) : null}
        {canUpdateSession ? (
          <Button variant="secondary" size="sm" aria-expanded={sessionOpen} aria-controls={formId} onClick={() => setSessionOpen((open) => !open)}>
            Mettre à jour la session
          </Button>
        ) : null}
        <form
          action={disconnect}
          onSubmit={(e) => {
            if (!confirm(disconnectQuestion(account.fullName, account.activeCampaigns, sessionHint))) e.preventDefault();
            else setLast("disconnect");
          }}
        >
          <SubmitButton variant="danger" size="sm" pendingLabel="Déconnexion…">
            Déconnecter
          </SubmitButton>
        </form>
      </div>
      <FormMessage state={state} />
      {canUpdateSession && sessionOpen ? (
        <div id={formId} className="rounded-control border border-line p-3">
          <SessionForm accountId={account.id} />
        </div>
      ) : null}
    </div>
  );
}

export function AccountSettingsForm({ account }: { account: LinkedInAccount }) {
  const [state, action] = useActionState(updateAccountAction.bind(null, account.id), null);
  const daysError = state?.fieldErrors?.sendingDays;
  return (
    <form action={action} className="space-y-4">
      <FormMessage state={state} />
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Type de compte" htmlFor={`type-${account.id}`}>
          <Select id={`type-${account.id}`} name="accountType" defaultValue={account.accountType}>
            {Object.entries(ACCOUNT_TYPES).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Fuseau horaire" htmlFor={`tz-${account.id}`} error={state?.fieldErrors?.timezone} hint="Par exemple Europe/Paris.">
          <Input id={`tz-${account.id}`} name="timezone" defaultValue={account.timezone} />
        </Field>
      </div>
      <fieldset aria-describedby={daysError ? `days-${account.id}-desc` : undefined}>
        <legend className="mb-1.5 text-sm font-medium text-ink">Jours d&apos;envoi</legend>
        <div className="flex flex-wrap gap-2">
          {WEEKDAYS.map((d) => (
            <label
              key={d.value}
              className="flex cursor-pointer items-center gap-1.5 rounded-control border border-line px-2.5 py-1.5 text-sm has-[:checked]:border-brand-600 has-[:checked]:bg-brand-50 pointer-coarse:min-h-11"
            >
              <input type="checkbox" name="sendingDays" value={d.value} defaultChecked={account.sendingDays.includes(d.value)} className={checkbox} />
              {d.label}
            </label>
          ))}
        </div>
        {daysError ? (
          <p id={`days-${account.id}-desc`} className="mt-1 text-xs text-danger">
            {daysError}
          </p>
        ) : null}
      </fieldset>
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Début" htmlFor={`start-${account.id}`}>
          <Input id={`start-${account.id}`} type="time" name="sendingStart" defaultValue={account.sendingStart} />
        </Field>
        <Field label="Fin" htmlFor={`end-${account.id}`} error={state?.fieldErrors?.sendingEnd} hint="Même heure de début et de fin : envois possibles toute la journée.">
          <Input id={`end-${account.id}`} type="time" name="sendingEnd" defaultValue={account.sendingEnd} />
        </Field>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <Field label="Invitations / semaine" htmlFor={`w-${account.id}`} hint="Laissez vide pour appliquer le plafond de sécurité." error={state?.fieldErrors?.weeklyInviteLimit}>
          <Input
            id={`w-${account.id}`}
            type="number"
            inputMode="numeric"
            min={0}
            name="weeklyInviteLimit"
            placeholder={String(WEEKLY_INVITE_CAP[account.accountType])}
            defaultValue={account.weeklyInviteLimit ?? ""}
          />
        </Field>
        <Field label="Invitations / jour" htmlFor={`d-${account.id}`} hint="40 au maximum. Laissez vide pour ce plafond." error={state?.fieldErrors?.dailyInviteLimit}>
          <Input id={`d-${account.id}`} type="number" inputMode="numeric" min={0} max={40} name="dailyInviteLimit" placeholder="40" defaultValue={account.dailyInviteLimit ?? ""} />
        </Field>
        <Field label="Messages / jour" htmlFor={`m-${account.id}`} hint="100 au maximum. Laissez vide pour ce plafond." error={state?.fieldErrors?.dailyMessageLimit}>
          <Input id={`m-${account.id}`} type="number" inputMode="numeric" min={0} max={100} name="dailyMessageLimit" placeholder="100" defaultValue={account.dailyMessageLimit ?? ""} />
        </Field>
      </div>
      <SubmitButton variant="secondary" pendingLabel="Enregistrement…">
        Enregistrer
      </SubmitButton>
    </form>
  );
}
