"use client";

import { Plus, Sparkles, Trash2 } from "lucide-react";
import { useActionState, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, FormMessage, Input, Select, Textarea } from "@/components/ui/form";
import { SubmitButton } from "@/components/ui/submit-button";
import { TagInput } from "@/components/ui/tag-input";
import { cn } from "@/lib/cn";
import { COMPANY_SIZES, SETTER_MODES, SIGNALS, SOURCES } from "@/lib/labels";
import { MAX_FOLLOW_UPS, type FollowUpStep } from "@/server/domain/followups";
import { INVITE_NOTE_MAX, TEMPLATE_VARIABLES, renderTemplate, type TemplateVars } from "@/server/domain/templates";
import { saveCampaignAction } from "./actions";

export type CampaignFormValues = {
  name: string;
  accountId: string;
  sources: string[];
  titles: string[];
  keywords: string[];
  industries: string[];
  locations: string[];
  companySizes: string[];
  signals: string[];
  postUrls: string[];
  exclusions: string[];
  aiPersonalization: boolean;
  minScore: number;
  weeklyProspectTarget: number;
  offer: string;
  persona: string;
  inviteNote: string;
  firstMessage: string;
  followUps: FollowUpStep[];
  setterMode: "OFF" | "APPROVAL" | "AUTO";
  bookingUrl: string;
};

type Props = {
  /** Whether Claude agents are configured on this deployment. */
  aiEnabled: boolean;
  campaignId: string | null;
  values: CampaignFormValues;
  accounts: { id: string; fullName: string }[];
  senderFirstName: string;
};

const SAMPLE: Omit<TemplateVars, "senderFirstName" | "bookingUrl"> = {
  firstName: "Camille", lastName: "Durand", company: "Nova Conseil", title: "DAF", industry: "Conseil", location: "Lyon",
};

const TITLE_SUGGESTIONS = ["CEO", "Fondateur", "CFO", "Directeur Administratif et Financier", "Head of Sales", "Directeur Commercial", "VP Marketing", "Head of Growth", "CTO", "DRH", "Expert-comptable"];
const INDUSTRY_SUGGESTIONS = ["Logiciels (SaaS)", "Conseil", "Expertise comptable", "E-commerce", "Industrie", "Immobilier", "Santé", "Services financiers", "Agence marketing", "Formation", "Logistique", "Recrutement"];
const LOCATION_SUGGESTIONS = ["Paris", "Lyon", "Bordeaux", "Lille", "Nantes", "Marseille", "Toulouse", "Rennes", "Bruxelles", "Genève", "Montréal", "Casablanca"];

export function CampaignForm({ aiEnabled, campaignId, values, accounts, senderFirstName }: Props) {
  const [state, action] = useActionState(saveCampaignAction.bind(null, campaignId), null);
  const [sources, setSources] = useState<string[]>(values.sources);
  const [minScore, setMinScore] = useState(values.minScore);
  const [inviteNote, setInviteNote] = useState(values.inviteNote);
  const [firstMessage, setFirstMessage] = useState(values.firstMessage);
  const [followUps, setFollowUps] = useState<FollowUpStep[]>(values.followUps);
  const [bookingUrl, setBookingUrl] = useState(values.bookingUrl);
  const [preview, setPreview] = useState(0);
  const err = state?.fieldErrors ?? {};

  const vars: TemplateVars = { ...SAMPLE, senderFirstName, bookingUrl };
  const steps = useMemo(
    () => [
      ...(inviteNote ? [{ label: "Note d'invitation", text: renderTemplate(inviteNote, vars, `preview-${preview}-note`) }] : []),
      { label: "Premier message", text: renderTemplate(firstMessage, vars, `preview-${preview}-first`) },
      ...followUps.map((f, i) => ({ label: `Relance ${i + 1} · J+${f.delayDays}`, text: renderTemplate(f.template, vars, `preview-${preview}-f${i}`) })),
    ],
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [inviteNote, firstMessage, followUps, preview, bookingUrl],
  );

  const toggleSource = (s: string) => setSources(sources.includes(s) ? sources.filter((x) => x !== s) : [...sources, s]);

  return (
    <form action={action} className="space-y-6">
      <FormMessage state={state} />

      <Card>
        <CardHeader title="Général" />
        <CardBody className="grid gap-4 sm:grid-cols-2">
          <Field label="Nom de la campagne" htmlFor="name" error={err.name}>
            <Input id="name" name="name" defaultValue={values.name} placeholder="DAF de PME SaaS · Île-de-France" required />
          </Field>
          <Field label="Compte LinkedIn" htmlFor="accountId" error={err.accountId}>
            <Select id="accountId" name="accountId" defaultValue={values.accountId} required>
              {accounts.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.fullName}
                </option>
              ))}
            </Select>
          </Field>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Ciblage" description="Où trouver les prospects et à qui s'adresser. Chaque profil est noté sur 100 selon ces critères." />
        <CardBody className="space-y-5">
          <fieldset>
            <legend className="mb-2 text-sm font-medium">Sources</legend>
            <div className="grid gap-2 sm:grid-cols-2">
              {(["SEARCH", "SIGNALS", "POST_ENGAGERS", "PROFILE_VISITORS"] as const).map((s) => (
                <label key={s} className={cn("flex cursor-pointer gap-3 rounded-lg border p-3", sources.includes(s) ? "border-brand-500 bg-brand-50/60" : "border-line")}>
                  <input type="checkbox" name="sources" value={s} checked={sources.includes(s)} onChange={() => toggleSource(s)} className="mt-0.5 accent-brand-600" />
                  <span>
                    <span className="block text-sm font-medium">{SOURCES[s]!.label}</span>
                    <span className="block text-xs text-muted">{SOURCES[s]!.description}</span>
                  </span>
                </label>
              ))}
            </div>
          </fieldset>

          {sources.includes("SIGNALS") ? (
            <fieldset>
              <legend className="mb-2 text-sm font-medium">Signaux d&apos;achat</legend>
              <div className="flex flex-wrap gap-2">
                {(["NEW_ROLE", "HIRING", "FUNDRAISING"] as const).map((s) => (
                  <Chip key={s} name="signals" value={s} label={SIGNALS[s]!} defaultChecked={values.signals.includes(s)} />
                ))}
              </div>
            </fieldset>
          ) : null}

          {sources.includes("POST_ENGAGERS") ? (
            <Field label="Posts à surveiller" htmlFor="postUrls" error={err.postUrls} hint="URL de posts LinkedIn (les vôtres ou ceux d'influenceurs de votre marché)">
              <TagInput id="postUrls" name="postUrls" defaultValue={values.postUrls} placeholder="https://www.linkedin.com/posts/…" />
            </Field>
          ) : null}

          <div className="grid gap-4 md:grid-cols-2">
            <Field label="Postes ciblés" htmlFor="titles" hint="Les équivalents FR/EN sont reconnus (CFO = DAF)">
              <TagInput id="titles" name="titles" defaultValue={values.titles} suggestions={TITLE_SUGGESTIONS} placeholder="CFO, Head of Sales…" />
            </Field>
            <Field label="Secteurs" htmlFor="industries">
              <TagInput id="industries" name="industries" defaultValue={values.industries} suggestions={INDUSTRY_SUGGESTIONS} placeholder="Logiciels (SaaS)…" />
            </Field>
            <Field label="Zones" htmlFor="locations">
              <TagInput id="locations" name="locations" defaultValue={values.locations} suggestions={LOCATION_SUGGESTIONS} placeholder="Paris, Lyon…" />
            </Field>
            <Field label="Mots-clés" htmlFor="keywords" hint="Cherchés dans le titre, le poste et l'entreprise">
              <TagInput id="keywords" name="keywords" defaultValue={values.keywords} placeholder="reporting, levée de fonds…" />
            </Field>
          </div>

          <fieldset>
            <legend className="mb-2 text-sm font-medium">Taille d&apos;entreprise (salariés)</legend>
            <div className="flex flex-wrap gap-2">
              {COMPANY_SIZES.map((s) => (
                <Chip key={s} name="companySizes" value={s} label={s} defaultChecked={values.companySizes.includes(s)} />
              ))}
            </div>
          </fieldset>

          <Field label="Exclusions" htmlFor="exclusions" hint="Un profil contenant un de ces termes n'est jamais contacté (concurrents, clients, stagiaires…)">
            <TagInput id="exclusions" name="exclusions" defaultValue={values.exclusions} placeholder="Stagiaire, Concurrent SA…" />
          </Field>

          <div className="grid gap-4 md:grid-cols-2">
            <Field label={`Score minimum : ${minScore}/100`} htmlFor="minScore" hint="En dessous, le prospect est écarté (sauf s'il vient d'un import)">
              <input id="minScore" name="minScore" type="range" min={0} max={100} step={5} value={minScore} onChange={(e) => setMinScore(Number(e.target.value))} className="w-full accent-brand-600" />
            </Field>
            <Field label="Nouveaux prospects par semaine" htmlFor="weeklyProspectTarget" error={err.weeklyProspectTarget}>
              <Input id="weeklyProspectTarget" name="weeklyProspectTarget" type="number" min={10} max={1000} defaultValue={values.weeklyProspectTarget} />
            </Field>
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Offre" description="Le setter s'en sert pour répondre aux questions des prospects." />
        <CardBody className="grid gap-4 md:grid-cols-2">
          <Field label="Ce que vous proposez" htmlFor="offer" error={err.offer} hint="La première phrase sert de réponse courte">
            <Textarea id="offer" name="offer" rows={4} defaultValue={values.offer} />
          </Field>
          <Field label="Client idéal" htmlFor="persona" error={err.persona}>
            <Textarea id="persona" name="persona" rows={4} defaultValue={values.persona} />
          </Field>
        </CardBody>
      </Card>

      <Card>
        <CardHeader
          title="Séquence"
          description={
            <>
              Variables : {TEMPLATE_VARIABLES.map((v) => <code key={v} className="mr-1 rounded bg-canvas px-1 text-xs">{`{{${v}}}`}</code>)}
              · Variantes : <code className="rounded bg-canvas px-1 text-xs">{"{Bonjour|Hello}"}</code>
            </>
          }
        />
        <CardBody className="grid gap-6 xl:grid-cols-[3fr_2fr]">
          <div className="space-y-4">
            <label className="flex cursor-pointer items-start gap-3 rounded-lg border border-line p-3 has-[:checked]:border-brand-500 has-[:checked]:bg-brand-50/60">
              <input type="checkbox" name="aiPersonalization" defaultChecked={values.aiPersonalization} className="mt-0.5 accent-brand-600" />
              <span>
                <span className="flex items-center gap-1.5 text-sm font-medium"><Sparkles className="size-3.5 text-brand-600" aria-hidden /> Personnalisation par Claude</span>
                <span className="block text-xs text-muted">
                  Claude adapte chaque message au profil (poste, entreprise, signal récent) en gardant votre intention, votre ton et vos liens. Il n&apos;invente aucun fait ; en cas de doute, votre texte part tel quel.
                  {aiEnabled ? "" : " Inactif tant qu'aucune clé API Anthropic n'est configurée : vos modèles sont envoyés tels quels."}
                </span>
              </span>
            </label>
            <Field label="Note d'invitation (facultative)" htmlFor="inviteNote" error={err.inviteNote} hint={`${inviteNote.length}/${INVITE_NOTE_MAX} caractères · sans note, les invitations sont souvent mieux acceptées`}>
              <Textarea id="inviteNote" name="inviteNote" rows={3} maxLength={INVITE_NOTE_MAX} value={inviteNote} onChange={(e) => setInviteNote(e.target.value)} />
            </Field>
            <Field label="Premier message (après acceptation)" htmlFor="firstMessage" error={err.firstMessage}>
              <Textarea id="firstMessage" name="firstMessage" rows={5} value={firstMessage} onChange={(e) => setFirstMessage(e.target.value)} required />
            </Field>
            <div className="space-y-3">
              <input type="hidden" name="followUps" value={JSON.stringify(followUps)} />
              <p className="text-sm font-medium">
                Relances <span className="font-normal text-muted">({followUps.length}/{MAX_FOLLOW_UPS}, arrêtées dès la première réponse)</span>
              </p>
              {err.followUps ? <p className="text-xs text-red-700">{err.followUps}</p> : null}
              {followUps.map((f, i) => (
                <div key={i} className="rounded-lg border border-line p-3">
                  <div className="mb-2 flex items-center gap-2 text-sm">
                    <span className="whitespace-nowrap font-medium">Relance {i + 1}</span>
                    <span className="text-muted">après</span>
                    <Input
                      aria-label={`Délai de la relance ${i + 1} en jours`}
                      type="number"
                      min={1}
                      max={30}
                      value={f.delayDays}
                      onChange={(e) => setFollowUps(followUps.map((x, j) => (j === i ? { ...x, delayDays: Number(e.target.value) || 1 } : x)))}
                      className="h-8 w-16"
                    />
                    <span className="text-muted">jours</span>
                    <Button variant="ghost" size="sm" className="ml-auto" onClick={() => setFollowUps(followUps.filter((_, j) => j !== i))} aria-label={`Supprimer la relance ${i + 1}`}>
                      <Trash2 className="size-3.5" />
                    </Button>
                  </div>
                  <Textarea
                    aria-label={`Texte de la relance ${i + 1}`}
                    rows={3}
                    value={f.template}
                    onChange={(e) => setFollowUps(followUps.map((x, j) => (j === i ? { ...x, template: e.target.value } : x)))}
                  />
                </div>
              ))}
              {followUps.length < MAX_FOLLOW_UPS ? (
                <Button variant="secondary" size="sm" onClick={() => setFollowUps([...followUps, { delayDays: 4, template: "{{firstName}}, " }])}>
                  <Plus className="size-3.5" /> Ajouter une relance
                </Button>
              ) : null}
            </div>
          </div>

          <aside className="space-y-3 xl:sticky xl:top-24 xl:self-start">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium">Aperçu</p>
              <Button variant="ghost" size="sm" onClick={() => setPreview(preview + 1)}>Autre variante</Button>
            </div>
            <div className="space-y-3 rounded-xl bg-canvas p-4">
              {steps.map((s) => (
                <div key={s.label}>
                  <p className="mb-1 text-[11px] font-medium uppercase tracking-wide text-muted">{s.label}</p>
                  <p className="whitespace-pre-line rounded-lg rounded-tl-sm bg-surface px-3 py-2 text-sm shadow-sm">{s.text || "—"}</p>
                </div>
              ))}
            </div>
            <p className="text-xs text-muted">
              Exemple avec {SAMPLE.firstName} {SAMPLE.lastName}, {SAMPLE.title} chez {SAMPLE.company}. Avec la personnalisation, Claude part de ce texte pour chaque prospect.
            </p>
          </aside>
        </CardBody>
      </Card>

      <Card>
        <CardHeader title="Setter IA" description="Ce qui se passe quand un prospect répond." />
        <CardBody className="space-y-4">
          <div className="grid gap-2 md:grid-cols-3">
            {(["AUTO", "APPROVAL", "OFF"] as const).map((mode) => {
              return (
                <label key={mode} className="flex cursor-pointer gap-3 rounded-lg border border-line p-3 has-[:checked]:border-brand-500 has-[:checked]:bg-brand-50/60">
                  <input type="radio" name="setterMode" value={mode} defaultChecked={values.setterMode === mode} className="mt-0.5 accent-brand-600" />
                  <span>
                    <span className="block text-sm font-medium">{SETTER_MODES[mode]!.label}</span>
                    <span className="block text-xs text-muted">{SETTER_MODES[mode]!.description}</span>
                  </span>
                </label>
              );
            })}
          </div>
          <Field label="Lien de réservation" htmlFor="bookingUrl" error={err.bookingUrl} hint="Envoyé aux prospects intéressés. Vide = lien des réglages.">
            <Input id="bookingUrl" name="bookingUrl" type="url" value={bookingUrl} onChange={(e) => setBookingUrl(e.target.value)} placeholder="https://calendly.com/vous/20min" />
          </Field>
        </CardBody>
      </Card>

      <div className="flex justify-end gap-2">
        <SubmitButton pendingLabel="Enregistrement…">{campaignId ? "Enregistrer" : "Créer la campagne"}</SubmitButton>
      </div>
    </form>
  );
}

function Chip({ name, value, label, defaultChecked }: { name: string; value: string; label: string; defaultChecked: boolean }) {
  return (
    <label className="flex cursor-pointer items-center gap-1.5 rounded-lg border border-line px-2.5 py-1.5 text-sm has-[:checked]:border-brand-500 has-[:checked]:bg-brand-50">
      <input type="checkbox" name={name} value={value} defaultChecked={defaultChecked} className="accent-brand-600" />
      {label}
    </label>
  );
}
