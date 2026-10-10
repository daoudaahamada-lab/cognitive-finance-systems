"use client";

import type { LinkedInAccount } from "@prisma/client";
import { useActionState } from "react";
import { Field, FormMessage, Input, Select } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { ACCOUNT_TYPES, WEEKDAYS } from "@/lib/labels";
import { WEEKLY_INVITE_CAP } from "@/server/domain/quotas";
import { connectAccountAction, updateAccountAction } from "./actions";

export function ConnectAccountForm() {
  const [state, action] = useActionState(connectAccountAction, null);
  return (
    <form action={action} className="space-y-4">
      <FormMessage state={state} />
      <p className="rounded-lg bg-canvas px-3 py-2 text-xs text-muted">
        Mode simulateur : aucun vrai compte n&apos;est contacté. Le simulateur génère des profils et des réponses réalistes pour tester tout le parcours.
      </p>
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Nom affiché" htmlFor="fullName" error={state?.fieldErrors?.fullName}>
          <Input id="fullName" name="fullName" placeholder="Alex Martin" required />
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
      <Field label="Titre du profil" htmlFor="headline">
        <Input id="headline" name="headline" placeholder="Fondateur · J'aide les PME à …" />
      </Field>
      <SubmitButton pendingLabel="Connexion…">Connecter le compte</SubmitButton>
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
