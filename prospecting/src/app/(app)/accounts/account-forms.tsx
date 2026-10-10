"use client";

import type { LinkedInAccount } from "@prisma/client";
import { CircleCheck, CircleX } from "lucide-react";
import { useActionState, useState } from "react";
import { Field, FormMessage, Input, Select } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { ACCOUNT_TYPES, WEEKDAYS } from "@/lib/labels";
import { WEEKLY_INVITE_CAP } from "@/server/domain/quotas";
import { connectAccountAction, diagnoseAccountAction, updateAccountAction, updateSessionAction } from "./actions";

function CookieHelp() {
  return (
    <details className="rounded-lg bg-canvas px-3 py-2 text-xs text-muted">
      <summary className="cursor-pointer select-none font-medium text-ink">Où trouver le cookie li_at ?</summary>
      <ol className="mt-2 list-decimal space-y-1 pl-4">
        <li>Connectez-vous à LinkedIn dans Chrome, sur votre ordinateur.</li>
        <li>Ouvrez les outils de développement (F12), onglet Application, puis Cookies → https://www.linkedin.com.</li>
        <li>Copiez la valeur du cookie <code>li_at</code> et collez-la ici.</li>
      </ol>
      <p className="mt-2">Ce cookie donne accès à votre compte : il reste sur votre instance, dans le profil navigateur du worker. Se déconnecter de LinkedIn ailleurs peut l&apos;invalider.</p>
    </details>
  );
}

export function ConnectAccountForm() {
  const [state, action] = useActionState(connectAccountAction, null);
  const [provider, setProvider] = useState<"browser" | "simulator">("browser");
  const err = state?.fieldErrors ?? {};
  return (
    <form action={action} className="space-y-4">
      <FormMessage state={state} />
      <fieldset className="grid gap-2 sm:grid-cols-2">
        <legend className="sr-only">Mode de connexion</legend>
        {(
          [
            ["browser", "Mon compte LinkedIn", "Le worker pilote votre session LinkedIn dans un navigateur, à un rythme humain."],
            ["simulator", "Simulateur", "Aucun vrai compte : profils et réponses simulés, pour tester le parcours."],
          ] as const
        ).map(([value, label, description]) => (
          <label key={value} className="flex cursor-pointer gap-3 rounded-lg border border-line p-3 has-[:checked]:border-brand-500 has-[:checked]:bg-brand-50/60">
            <input type="radio" name="provider" value={value} checked={provider === value} onChange={() => setProvider(value)} className="mt-0.5 accent-brand-600" />
            <span>
              <span className="block text-sm font-medium">{label}</span>
              <span className="block text-xs text-muted">{description}</span>
            </span>
          </label>
        ))}
      </fieldset>
      {provider === "browser" ? (
        <>
          <Field label="Cookie de session li_at" htmlFor="sessionCookie" error={err.sessionCookie} hint="Laissez vide pour vous connecter vous-même avec npm run linkedin:login.">
            <Input id="sessionCookie" name="sessionCookie" type="password" autoComplete="off" placeholder="AQEDAR…" />
          </Field>
          <CookieHelp />
        </>
      ) : null}
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Nom affiché" htmlFor="fullName" error={err.fullName} hint={provider === "browser" ? "Lu sur LinkedIn quand un cookie est fourni" : undefined}>
          <Input id="fullName" name="fullName" placeholder="Alex Martin" />
        </Field>
        <Field label="Type de compte" htmlFor="accountType" hint="Fixe le plafond d'invitations hebdomadaire">
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

/** Read-only check run by the worker on LinkedIn: tells whether Vela still understands the pages. */
export function DiagnoseForm({ accountId }: { accountId: string }) {
  const [state, action] = useActionState(diagnoseAccountAction.bind(null, accountId), null);
  const failed = state?.lines?.filter((line) => !line.ok).length ?? 0;
  return (
    <form action={action} className="space-y-2">
      <SubmitButton variant="secondary" size="sm" pendingLabel="Vérification sur LinkedIn… (environ 1 minute)">Vérifier la connexion LinkedIn</SubmitButton>
      <p className="text-xs text-muted">Ouvre votre session, une recherche, un profil, vos relations et vos messages. N&apos;envoie rien.</p>
      {state?.error ? <FormMessage state={state} /> : null}
      {state?.lines ? (
        <div role="status" className={`space-y-2 rounded-lg border px-3 py-2 text-sm ${failed ? "border-amber-200 bg-amber-50 text-amber-900" : "border-emerald-200 bg-emerald-50 text-emerald-900"}`}>
          <p className="font-semibold">
            {failed
              ? `${failed} point${failed > 1 ? "s" : ""} non reconnu${failed > 1 ? "s" : ""} : LinkedIn a peut-être changé son interface. N'activez pas de campagne pour l'instant.`
              : "Tout est reconnu : vous pouvez lancer une campagne."}
          </p>
          <ul className="space-y-1">
            {state.lines.map((line) => (
              <li key={line.check} className="flex gap-2">
                {line.ok ? <CircleCheck className="mt-0.5 size-4 shrink-0 text-emerald-600" aria-label="OK" /> : <CircleX className="mt-0.5 size-4 shrink-0 text-red-600" aria-label="Échec" />}
                <span className="min-w-0 break-words"><strong className="font-semibold">{line.check}</strong> : {line.detail}</span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </form>
  );
}

export function SessionForm({ accountId }: { accountId: string }) {
  const [state, action] = useActionState(updateSessionAction.bind(null, accountId), null);
  return (
    <form action={action} className="space-y-2">
      <FormMessage state={state} />
      <Field label="Nouveau cookie li_at" htmlFor={`cookie-${accountId}`} error={state?.fieldErrors?.sessionCookie}>
        <Input id={`cookie-${accountId}`} name="sessionCookie" type="password" autoComplete="off" required />
      </Field>
      <CookieHelp />
      <SubmitButton variant="secondary" size="sm" pendingLabel="Vérification…">Mettre à jour la session</SubmitButton>
    </form>
  );
}

export function AccountSettingsForm({ account }: { account: LinkedInAccount }) {
  const [state, action] = useActionState(updateAccountAction.bind(null, account.id), null);
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
        <Field label="Fuseau horaire" htmlFor={`tz-${account.id}`} error={state?.fieldErrors?.timezone}>
          <Input id={`tz-${account.id}`} name="timezone" defaultValue={account.timezone} />
        </Field>
      </div>
      <fieldset>
        <legend className="mb-1.5 text-sm font-medium">Jours d&apos;envoi</legend>
        <div className="flex flex-wrap gap-2">
          {WEEKDAYS.map((d) => (
            <label key={d.value} className="flex cursor-pointer items-center gap-1.5 rounded-lg border border-line px-2.5 py-1.5 text-sm has-[:checked]:border-brand-500 has-[:checked]:bg-brand-50">
              <input type="checkbox" name="sendingDays" value={d.value} defaultChecked={account.sendingDays.includes(d.value)} className="accent-brand-600" />
              {d.label}
            </label>
          ))}
        </div>
        {state?.fieldErrors?.sendingDays ? <p className="mt-1 text-xs text-red-700">{state.fieldErrors.sendingDays}</p> : null}
      </fieldset>
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Début" htmlFor={`start-${account.id}`}>
          <Input id={`start-${account.id}`} type="time" name="sendingStart" defaultValue={account.sendingStart} />
        </Field>
        <Field label="Fin" htmlFor={`end-${account.id}`} error={state?.fieldErrors?.sendingEnd} hint="Même heure qu'au début = toute la journée">
          <Input id={`end-${account.id}`} type="time" name="sendingEnd" defaultValue={account.sendingEnd} />
        </Field>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <Field label="Invitations / semaine" htmlFor={`w-${account.id}`} hint="Vide = plafond de sécurité" error={state?.fieldErrors?.weeklyInviteLimit}>
          <Input id={`w-${account.id}`} type="number" min={0} name="weeklyInviteLimit" placeholder={String(WEEKLY_INVITE_CAP[account.accountType])} defaultValue={account.weeklyInviteLimit ?? ""} />
        </Field>
        <Field label="Invitations / jour" htmlFor={`d-${account.id}`} hint="40 maximum" error={state?.fieldErrors?.dailyInviteLimit}>
          <Input id={`d-${account.id}`} type="number" min={0} max={40} name="dailyInviteLimit" placeholder="40" defaultValue={account.dailyInviteLimit ?? ""} />
        </Field>
        <Field label="Messages / jour" htmlFor={`m-${account.id}`} hint="100 maximum" error={state?.fieldErrors?.dailyMessageLimit}>
          <Input id={`m-${account.id}`} type="number" min={0} max={100} name="dailyMessageLimit" placeholder="100" defaultValue={account.dailyMessageLimit ?? ""} />
        </Field>
      </div>
      <SubmitButton variant="secondary" pendingLabel="Enregistrement…">Enregistrer</SubmitButton>
    </form>
  );
}
