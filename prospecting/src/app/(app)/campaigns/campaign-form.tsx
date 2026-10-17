"use client";

import { ArrowRight, Plus, Sparkles, Trash2 } from "lucide-react";
import { startTransition, useActionState, useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import { Dot } from "@/components/ui/badge";
import { Button, ButtonLink, buttonClass } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Field, FormMessage, Input, Select, Textarea, checkbox } from "@/components/ui/form";
import { StickyActionBar } from "@/components/ui/sticky-action-bar";
import { TagInput } from "@/components/ui/tag-input";
import { cn } from "@/lib/cn";
import { plural } from "@/lib/format";
import { COMPANY_SIZES, SETTER_MODES, SIGNALS, SOURCES } from "@/lib/labels";
import { FIRST_MESSAGE_DELAY_HOURS, MAX_FOLLOW_UPS, sequenceEndDay, sequenceTimeline, type FollowUpStep } from "@/server/domain/followups";
import {
  INVITE_NOTE_MAX,
  TEMPLATE_VARIABLES,
  VARIABLE_LABELS_FR,
  countVariants,
  renderTemplate,
  suggestVariable,
  unknownVariables,
  type TemplateVars,
} from "@/server/domain/templates";
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
  searchUrl: string;
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

export type CampaignFormAccount = { id: string; fullName: string; provider: string; accountType: string; status: string };

type Props = {
  /** Whether Claude agents are configured on this deployment. */
  aiEnabled: boolean;
  campaignId: string | null;
  values: CampaignFormValues;
  accounts: CampaignFormAccount[];
  /** Settings used when the campaign leaves offer, persona or booking link empty. */
  workspace: { offer: string; persona: string; bookingUrl: string };
};

const SAMPLE: Omit<TemplateVars, "senderFirstName" | "bookingUrl"> = {
  firstName: "Camille", lastName: "Durand", company: "Nova Conseil", title: "DAF", industry: "Conseil", location: "Lyon",
};

const TITLE_SUGGESTIONS = ["CEO", "Fondateur", "CFO", "Directeur Administratif et Financier", "Head of Sales", "Directeur Commercial", "VP Marketing", "Head of Growth", "CTO", "DRH", "Expert-comptable"];
const INDUSTRY_SUGGESTIONS = ["Logiciels (SaaS)", "Conseil", "Expertise comptable", "E-commerce", "Industrie", "Immobilier", "Santé", "Services financiers", "Agence marketing", "Formation", "Logistique", "Recrutement"];
const LOCATION_SUGGESTIONS = ["Paris", "Lyon", "Bordeaux", "Lille", "Nantes", "Marseille", "Toulouse", "Rennes", "Bruxelles", "Genève", "Montréal", "Casablanca"];

const SECTIONS = [
  { id: "general", label: "Général" },
  { id: "ciblage", label: "Ciblage" },
  { id: "offre", label: "Offre" },
  { id: "sequence", label: "Séquence" },
  { id: "setter", label: "Setter" },
] as const;
type SectionId = (typeof SECTIONS)[number]["id"];

/** Form order, labels for the "Corrigez : …" summary, and the section each field lives in. */
const FIELDS: Record<string, { label: string; section: SectionId }> = {
  name: { label: "Nom de la campagne", section: "general" },
  accountId: { label: "Compte LinkedIn", section: "general" },
  sources: { label: "Sources", section: "ciblage" },
  searchUrl: { label: "URL de recherche LinkedIn", section: "ciblage" },
  signals: { label: "Signaux d'achat", section: "ciblage" },
  postUrls: { label: "Posts à surveiller", section: "ciblage" },
  titles: { label: "Postes ciblés", section: "ciblage" },
  industries: { label: "Secteurs", section: "ciblage" },
  locations: { label: "Zones", section: "ciblage" },
  keywords: { label: "Mots-clés", section: "ciblage" },
  companySizes: { label: "Taille d'entreprise", section: "ciblage" },
  exclusions: { label: "Exclusions", section: "ciblage" },
  minScore: { label: "Score minimum", section: "ciblage" },
  weeklyProspectTarget: { label: "Nouveaux prospects par semaine", section: "ciblage" },
  offer: { label: "Ce que vous proposez", section: "offre" },
  persona: { label: "Client idéal", section: "offre" },
  aiPersonalization: { label: "Personnalisation par Claude", section: "sequence" },
  inviteNote: { label: "Note d'invitation", section: "sequence" },
  firstMessage: { label: "Premier message", section: "sequence" },
  followUps: { label: "Relances", section: "sequence" },
  setterMode: { label: "Mode du setter", section: "setter" },
  bookingUrl: { label: "Lien de réservation", section: "setter" },
};
const FIELD_ORDER = Object.keys(FIELDS);

/** Field info for an error key; follow-up errors are keyed by step ("followUps.1" is Relance 2). */
function fieldInfo(key: string): { label: string; section: SectionId; order: number } | null {
  const step = /^followUps\.(\d+)$/.exec(key);
  if (step) return { label: `Relance ${Number(step[1]) + 1}`, section: "sequence", order: FIELD_ORDER.indexOf("followUps") + (Number(step[1]) + 1) / 100 };
  const field = FIELDS[key];
  return field ? { ...field, order: FIELD_ORDER.indexOf(key) } : null;
}

/** Buying signals only exist in the simulator: a real LinkedIn account finds no one with them. */
function isRealAccount(account: CampaignFormAccount | undefined): boolean {
  return account !== undefined && account.provider !== "simulator";
}

function unknownVariableHint(name: string): string {
  const suggestion = suggestVariable(name);
  return suggestion
    ? `Variable inconnue {{${name}}} : vouliez-vous {{${suggestion}}} ?`
    : `Variable inconnue {{${name}}} : insérez plutôt une des variables proposées.`;
}

export function CampaignForm({ aiEnabled, campaignId, values, accounts, workspace }: Props) {
  const [state, formAction, pending] = useActionState(saveCampaignAction.bind(null, campaignId), null);
  const formRef = useRef<HTMLFormElement>(null);
  const [accountId, setAccountId] = useState(values.accountId);
  const [sources, setSources] = useState<string[]>(() =>
    isRealAccount(accounts.find((a) => a.id === values.accountId)) ? values.sources.filter((s) => s !== "SIGNALS") : values.sources,
  );
  const [searchUrl, setSearchUrl] = useState(values.searchUrl);
  const [minScore, setMinScore] = useState(values.minScore);
  const [withNote, setWithNote] = useState(values.inviteNote.trim() !== "");
  const [inviteNote, setInviteNote] = useState(values.inviteNote);
  const [firstMessage, setFirstMessage] = useState(values.firstMessage);
  const [followUps, setFollowUps] = useState<FollowUpStep[]>(values.followUps);
  const [bookingUrl, setBookingUrl] = useState(values.bookingUrl);
  const [preview, setPreview] = useState(0);
  const err = state?.fieldErrors ?? {};

  const account = accounts.find((a) => a.id === accountId);
  const realAccount = isRealAccount(account);
  const usesSearchUrl = sources.includes("SEARCH") && searchUrl.trim() !== "";
  const timeline = sequenceTimeline(followUps);

  // Bring the first invalid field into view after a rejected save (the message itself is in the sticky bar).
  useEffect(() => {
    if (!state?.fieldErrors) return;
    const first = formRef.current?.querySelector<HTMLElement>('[aria-invalid="true"]');
    if (!first) return;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    first.scrollIntoView({ block: "center", behavior: reduceMotion ? "auto" : "smooth" });
    first.focus({ preventScroll: true });
  }, [state]);

  // Submitting through onSubmit instead of <form action> keeps every typed value: React 19 resets
  // uncontrolled fields after a form action, which wiped the form whenever the server refused it.
  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (pending) return;
    const data = new FormData(event.currentTarget);
    startTransition(() => formAction(data));
  };

  const errorFields = Object.keys(err)
    .map(fieldInfo)
    .filter((f) => f !== null)
    .sort((a, b) => a.order - b.order);
  const sectionsWithErrors = new Set(errorFields.map((f) => f.section));
  const barState = state?.error && errorFields.length > 0 ? { error: `Corrigez : ${[...new Set(errorFields.map((f) => f.label))].join(", ")}.` } : state;

  const changeAccount = (id: string) => {
    setAccountId(id);
    if (!isRealAccount(accounts.find((a) => a.id === id))) return;
    setSources((current) => {
      const kept = current.filter((s) => s !== "SIGNALS");
      return current.includes("SIGNALS") && kept.length === 0 ? ["SEARCH"] : kept;
    });
  };
  const toggleSource = (s: string) => setSources(sources.includes(s) ? sources.filter((x) => x !== s) : [...sources, s]);
  const updateFollowUp = (i: number, change: Partial<FollowUpStep>) => setFollowUps(followUps.map((x, j) => (j === i ? { ...x, ...change } : x)));

  const vars: TemplateVars = { ...SAMPLE, senderFirstName: account?.fullName.split(" ")[0] ?? "", bookingUrl: bookingUrl.trim() || workspace.bookingUrl };
  const steps = [
    ...(withNote && inviteNote.trim() ? [{ key: "note", label: "Note d'invitation", text: renderTemplate(inviteNote, vars, `preview-${preview}-note`) }] : []),
    { key: "first", label: "Premier message · J0", text: renderTemplate(firstMessage, vars, `preview-${preview}-first`) },
    ...followUps.map((f, i) => ({
      key: `f${i}`,
      label: `Relance ${i + 1} · J+${timeline[i]!.dayFromFirst}`,
      text: renderTemplate(f.template, vars, `preview-${preview}-f${i}`),
    })),
  ];

  return (
    <form ref={formRef} onSubmit={onSubmit} className="space-y-6">
      <nav
        aria-label="Sections de la campagne"
        className="-mx-4 border-b border-line bg-canvas/95 px-4 py-2 backdrop-blur sm:-mx-8 sm:px-8 lg:sticky lg:top-(--app-header-h) lg:z-10"
      >
        <ul className="flex gap-1 overflow-x-auto">
          {SECTIONS.map((s) => (
            <li key={s.id} className="shrink-0">
              <a href={`#${s.id}`} className={buttonClass({ variant: "ghost", size: "sm" }, "text-sm")}>
                {s.label}
                {sectionsWithErrors.has(s.id) ? <Dot tone="danger" label="contient une erreur" /> : null}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      <Card id="general" className="lg:scroll-mt-12">
        <CardHeader title="Général" />
        <CardBody className="grid gap-4 sm:grid-cols-2">
          <Field label="Nom de la campagne" htmlFor="name" error={err.name}>
            <Input id="name" name="name" defaultValue={values.name} placeholder="DAF de PME SaaS · Île-de-France" required />
          </Field>
          <Field
            label="Compte LinkedIn"
            htmlFor="accountId"
            error={err.accountId}
            hint={account?.status === "PAUSED" ? "Ce compte est en pause : la campagne pourra être lancée une fois le compte réparé dans Comptes LinkedIn." : undefined}
          >
            <Select id="accountId" name="accountId" value={accountId} onChange={(e) => changeAccount(e.target.value)} required>
              {account ? null : (
                <option value="" disabled>
                  Choisissez un compte
                </option>
              )}
              {accounts.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.fullName}
                  {a.provider === "simulator" ? " · simulateur" : ""}
                  {a.status === "PAUSED" ? " (en pause)" : ""}
                </option>
              ))}
            </Select>
          </Field>
        </CardBody>
      </Card>

      <Card id="ciblage" className="lg:scroll-mt-12">
        <CardHeader title="Ciblage" description="Où trouver les prospects et à qui s'adresser. Chaque profil est noté sur 100 selon ces critères." />
        <CardBody className="space-y-6">
          <fieldset>
            <legend className="mb-2 text-sm font-medium text-ink">Sources</legend>
            <div className="grid gap-2 sm:grid-cols-2">
              {(["SEARCH", "SIGNALS", "POST_ENGAGERS", "PROFILE_VISITORS"] as const).map((s) => {
                const unavailable = s === "SIGNALS" && realAccount;
                const checked = sources.includes(s) && !unavailable;
                return (
                  <label
                    key={s}
                    className={cn(
                      "flex gap-3 rounded-control border p-3",
                      unavailable ? "cursor-not-allowed border-line bg-surface-2" : "cursor-pointer",
                      checked ? "border-brand-500 bg-brand-50/60" : !unavailable && "border-line hover:border-line-strong",
                    )}
                  >
                    <input
                      type="checkbox"
                      name="sources"
                      value={s}
                      checked={checked}
                      disabled={unavailable}
                      onChange={() => toggleSource(s)}
                      className={cn(checkbox, "mt-0.5")}
                    />
                    <span>
                      <span className={cn("block text-sm font-medium", unavailable ? "text-muted" : "text-ink")}>{SOURCES[s]!.label}</span>
                      <span className={cn("block text-xs", checked ? "text-ink-2" : "text-muted")}>
                        {unavailable ? "Pas encore disponible avec un vrai compte LinkedIn" : SOURCES[s]!.description}
                      </span>
                    </span>
                  </label>
                );
              })}
            </div>
            {err.sources ? (
              <p className="mt-2 text-xs text-danger">{err.sources}</p>
            ) : sources.length === 0 ? (
              <p className="mt-2 text-xs text-muted">Sans source, la campagne ne contacte que les prospects que vous importez.</p>
            ) : null}
          </fieldset>

          {sources.includes("SEARCH") ? (
            <Field
              label="URL de recherche LinkedIn (facultative)"
              htmlFor="searchUrl"
              error={err.searchUrl}
              hint="Faites votre recherche de personnes sur LinkedIn avec ses filtres (lieu, secteur, entreprise…), puis collez l'URL. Sinon, la recherche est construite à partir des postes et mots-clés ci-dessous."
            >
              <Input
                id="searchUrl"
                name="searchUrl"
                type="url"
                value={searchUrl}
                onChange={(e) => setSearchUrl(e.target.value)}
                placeholder="https://www.linkedin.com/search/results/people/?keywords=…"
              />
            </Field>
          ) : null}

          {sources.includes("SIGNALS") && !realAccount ? (
            <fieldset>
              <legend className="mb-2 text-sm font-medium text-ink">Signaux d&apos;achat</legend>
              <div className="flex flex-wrap gap-2">
                {(["NEW_ROLE", "HIRING", "FUNDRAISING"] as const).map((s) => (
                  <Chip key={s} name="signals" value={s} label={SIGNALS[s]!} defaultChecked={values.signals.includes(s)} />
                ))}
              </div>
              {err.signals ? <p className="mt-2 text-xs text-danger">{err.signals}</p> : null}
            </fieldset>
          ) : null}

          {sources.includes("POST_ENGAGERS") ? (
            <Field label="Posts à surveiller" htmlFor="postUrls" error={err.postUrls} hint="URL de posts LinkedIn (les vôtres ou ceux d'influenceurs de votre marché)">
              <TagInput id="postUrls" name="postUrls" defaultValue={values.postUrls} placeholder="https://www.linkedin.com/posts/…" />
            </Field>
          ) : null}

          <fieldset className="space-y-4 rounded-control border border-line p-4">
            <legend className="px-1 text-sm font-semibold text-ink">{usesSearchUrl ? "Critères de note (la recherche utilise votre URL)" : "Critères de recherche et de note"}</legend>
            <div className="grid gap-4 md:grid-cols-2">
              <Field label="Postes ciblés" htmlFor="titles" error={err.titles} hint="Les équivalents FR/EN sont reconnus (CFO = DAF)">
                <TagInput id="titles" name="titles" defaultValue={values.titles} suggestions={TITLE_SUGGESTIONS} placeholder="CFO, Head of Sales…" />
              </Field>
              <Field label="Secteurs" htmlFor="industries" error={err.industries} hint={realAccount ? "Utilisés pour la note, pas pour la recherche LinkedIn" : undefined}>
                <TagInput id="industries" name="industries" defaultValue={values.industries} suggestions={INDUSTRY_SUGGESTIONS} placeholder="Logiciels (SaaS)…" />
              </Field>
              <Field label="Zones" htmlFor="locations" error={err.locations}>
                <TagInput id="locations" name="locations" defaultValue={values.locations} suggestions={LOCATION_SUGGESTIONS} placeholder="Paris, Lyon…" />
              </Field>
              <Field label="Mots-clés" htmlFor="keywords" error={err.keywords} hint="Cherchés dans le titre, le poste et l'entreprise">
                <TagInput id="keywords" name="keywords" defaultValue={values.keywords} placeholder="reporting, levée de fonds…" />
              </Field>
            </div>

            <fieldset aria-describedby={realAccount ? "companySizes-desc" : undefined}>
              <legend className="mb-2 text-sm font-medium text-ink">Taille d&apos;entreprise (salariés)</legend>
              <div className="flex flex-wrap gap-2">
                {COMPANY_SIZES.map((s) => (
                  <Chip key={s} name="companySizes" value={s} label={s} defaultChecked={values.companySizes.includes(s)} />
                ))}
              </div>
              {realAccount ? (
                <p id="companySizes-desc" className="mt-1.5 text-xs text-muted">
                  Utilisés pour la note, pas pour la recherche LinkedIn
                </p>
              ) : null}
            </fieldset>

            <Field label="Exclusions" htmlFor="exclusions" error={err.exclusions} hint="Un profil contenant un de ces termes n'est jamais contacté (concurrents, clients, stagiaires…)">
              <TagInput id="exclusions" name="exclusions" defaultValue={values.exclusions} placeholder="Stagiaire, Concurrent SA…" />
            </Field>
          </fieldset>

          <div className="grid gap-4 md:grid-cols-2">
            <Field label={`Score minimum : ${minScore}/100`} htmlFor="minScore" error={err.minScore} hint="En dessous, le prospect est écarté (sauf s'il vient d'un import)">
              <input id="minScore" name="minScore" type="range" min={0} max={100} step={5} value={minScore} onChange={(e) => setMinScore(Number(e.target.value))} className="h-11 w-full accent-brand-600 sm:h-9" />
            </Field>
            <Field label="Nouveaux prospects par semaine" htmlFor="weeklyProspectTarget" error={err.weeklyProspectTarget}>
              <Input id="weeklyProspectTarget" name="weeklyProspectTarget" type="number" inputMode="numeric" min={10} max={1000} defaultValue={values.weeklyProspectTarget} />
            </Field>
          </div>
        </CardBody>
      </Card>

      <Card id="offre" className="lg:scroll-mt-12">
        <CardHeader title="Offre" description="Sert à noter les profils, à personnaliser les messages et à répondre aux questions des prospects." />
        <CardBody className="grid gap-4 md:grid-cols-2">
          <Field
            label="Ce que vous proposez"
            htmlFor="offer"
            error={err.offer}
            hint={
              workspace.offer.trim()
                ? "Laissez vide pour utiliser celle des Réglages. La première phrase sert de réponse courte."
                : "Aucune offre dans les Réglages : décrivez-la ici. La première phrase sert de réponse courte."
            }
          >
            <Textarea id="offer" name="offer" rows={4} defaultValue={values.offer} placeholder={workspace.offer.trim() || "Ex. : nous automatisons le reporting financier des PME…"} />
          </Field>
          <Field
            label="Client idéal"
            htmlFor="persona"
            error={err.persona}
            hint={workspace.persona.trim() ? "Laissez vide pour utiliser celui des Réglages." : "Aucun client idéal dans les Réglages : décrivez-le ici."}
          >
            <Textarea id="persona" name="persona" rows={4} defaultValue={values.persona} placeholder={workspace.persona.trim() || "Ex. : DAF de PME de 20 à 500 salariés…"} />
          </Field>
        </CardBody>
      </Card>

      <Card id="sequence" className="lg:scroll-mt-12">
        <CardHeader
          title="Séquence"
          description="Ce que reçoit chaque prospect, de l'invitation à la dernière relance. Les boutons au-dessus de chaque message insèrent une variable à l'endroit du curseur."
        />
        <CardBody className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
          <div className="min-w-0 space-y-5">
            <label className="group flex cursor-pointer items-start gap-3 rounded-control border border-line p-3 has-[:checked]:border-ai-line has-[:checked]:bg-ai-soft">
              <input type="checkbox" name="aiPersonalization" defaultChecked={values.aiPersonalization} className={cn(checkbox, "mt-0.5 accent-ai")} />
              <span>
                <span className="flex items-center gap-1.5 text-sm font-medium text-ink">
                  <Sparkles className="size-3.5 text-ai" aria-hidden /> Personnalisation par Claude
                </span>
                <span className="block text-xs text-muted group-has-[:checked]:text-ink-2">
                  Claude adapte chaque message au profil (poste, entreprise, signal récent) en gardant votre intention, votre ton et vos liens. Il n&apos;invente aucun fait ; en cas de doute, votre texte part tel quel.
                  {aiEnabled ? "" : " Claude n'est pas configuré sur cette installation : vos messages partent tels quels."}
                </span>
              </span>
            </label>

            <CadenceLine followUps={followUps} />

            <div className="space-y-2">
              <label className="flex cursor-pointer items-center gap-2.5 text-sm font-medium text-ink">
                <input type="checkbox" checked={withNote} onChange={(e) => setWithNote(e.target.checked)} className={checkbox} aria-describedby="inviteNote-toggle-desc" />
                Ajouter une note à l&apos;invitation
              </label>
              <p id="inviteNote-toggle-desc" className="text-xs text-muted">
                Sans note, les invitations sont souvent mieux acceptées.
              </p>
              {withNote ? (
                <TemplateEditor
                  id="inviteNote"
                  name="inviteNote"
                  label="Note d'invitation"
                  value={inviteNote}
                  onChange={setInviteNote}
                  rows={3}
                  maxLength={INVITE_NOTE_MAX}
                  serverError={err.inviteNote}
                  hint={account?.accountType === "FREE" ? "Compte gratuit : LinkedIn limite les notes personnalisées ; au-delà, l'invitation part sans note." : undefined}
                />
              ) : (
                <input type="hidden" name="inviteNote" value="" />
              )}
            </div>

            <TemplateEditor
              id="firstMessage"
              name="firstMessage"
              label={`Premier message (${FIRST_MESSAGE_DELAY_HOURS} h après l'acceptation)`}
              value={firstMessage}
              onChange={setFirstMessage}
              rows={5}
              serverError={err.firstMessage}
              required
            />

            <div className="space-y-3">
              <input type="hidden" name="followUps" value={JSON.stringify(followUps)} />
              <p className="text-sm font-medium text-ink">
                Relances{" "}
                <span className="font-normal text-muted">
                  ({followUps.length} sur {MAX_FOLLOW_UPS} possibles · elles s&apos;arrêtent dès que le prospect répond)
                </span>
              </p>
              {err.followUps ? <p className="text-xs text-danger">{err.followUps}</p> : null}
              {followUps.map((f, i) => {
                const after = i === 0 ? "le premier message" : `la relance ${i}`;
                return (
                  <div key={i} className="space-y-2 rounded-control border border-line p-3">
                    <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm">
                      <span className="whitespace-nowrap font-medium text-ink">Relance {i + 1}</span>
                      <span className="text-muted" aria-hidden>
                        ·
                      </span>
                      <Input
                        aria-label={`Délai de la relance ${i + 1}, en jours après ${after}`}
                        type="number"
                        inputMode="numeric"
                        min={1}
                        max={30}
                        value={f.delayDays || ""}
                        onChange={(e) => updateFollowUp(i, { delayDays: Math.min(30, Math.max(0, Math.round(Number(e.target.value) || 0))) })}
                        onBlur={() => {
                          if (f.delayDays < 1) updateFollowUp(i, { delayDays: 1 });
                        }}
                        className="w-20"
                      />
                      <span className="text-muted">
                        {f.delayDays > 1 ? "jours" : "jour"} après {after}
                      </span>
                      <span className="font-medium tabular-nums text-ink-2">(J+{timeline[i]!.dayFromFirst})</span>
                      <Button variant="ghost" size="icon" className="ml-auto" onClick={() => setFollowUps(followUps.filter((_, j) => j !== i))} aria-label={`Supprimer la relance ${i + 1}`}>
                        <Trash2 className="size-4" aria-hidden />
                      </Button>
                    </div>
                    <TemplateEditor
                      id={`followUp-${i}`}
                      aria-label={`Texte de la relance ${i + 1}`}
                      value={f.template}
                      onChange={(template) => updateFollowUp(i, { template })}
                      rows={3}
                      serverError={err[`followUps.${i}`]}
                    />
                  </div>
                );
              })}
              {followUps.length < MAX_FOLLOW_UPS ? (
                <Button variant="secondary" size="sm" onClick={() => setFollowUps([...followUps, { delayDays: 4, template: "{{firstName}}, " }])}>
                  <Plus className="size-3.5" aria-hidden /> Ajouter une relance
                </Button>
              ) : null}
            </div>
          </div>

          <aside aria-label="Aperçu des messages" className="min-w-0 space-y-3 xl:sticky xl:top-[calc(var(--app-header-h)+4.5rem)] xl:self-start">
            <div className="flex items-center justify-between gap-2">
              <p className="text-sm font-medium text-ink">Aperçu</p>
              <Button variant="ghost" size="sm" onClick={() => setPreview(preview + 1)}>
                Autre variante
              </Button>
            </div>
            <div className="space-y-3 rounded-card bg-canvas p-4">
              {steps.map((s) => (
                <div key={s.key}>
                  <p className="mb-1 text-2xs font-medium uppercase tracking-wide text-muted">{s.label}</p>
                  <p className="whitespace-pre-line rounded-control rounded-tl-sm bg-surface px-3 py-2 text-sm text-ink shadow-card">{s.text || "—"}</p>
                </div>
              ))}
            </div>
            <p className="text-xs text-muted">
              Exemple avec {SAMPLE.firstName} {SAMPLE.lastName}, {SAMPLE.title} chez {SAMPLE.company}.
              {aiEnabled ? " Avec la personnalisation, Claude part de ce texte pour chaque prospect." : ""}
            </p>
          </aside>
        </CardBody>
      </Card>

      <Card id="setter" className="lg:scroll-mt-12">
        <CardHeader title="Setter IA" description="Ce qui se passe quand un prospect répond." />
        <CardBody className="space-y-4">
          <fieldset>
            <legend className="sr-only">Mode du setter</legend>
            <div className="grid gap-2 md:grid-cols-3">
              {(["AUTO", "APPROVAL", "OFF"] as const).map((mode) => (
                <label key={mode} className="group flex cursor-pointer gap-3 rounded-control border border-line p-3 hover:border-line-strong has-[:checked]:border-ai-line has-[:checked]:bg-ai-soft">
                  <input type="radio" name="setterMode" value={mode} defaultChecked={values.setterMode === mode} className={cn(checkbox, "mt-0.5 accent-ai")} />
                  <span>
                    <span className="block text-sm font-medium text-ink">{SETTER_MODES[mode]!.label}</span>
                    <span className="block text-xs text-muted group-has-[:checked]:text-ink-2">{SETTER_MODES[mode]!.description}</span>
                  </span>
                </label>
              ))}
            </div>
            {err.setterMode ? <p className="mt-2 text-xs text-danger">{err.setterMode}</p> : null}
          </fieldset>
          <Field
            label="Lien de réservation"
            htmlFor="bookingUrl"
            error={err.bookingUrl}
            hint={
              workspace.bookingUrl
                ? "Envoyé aux prospects intéressés. Laissez vide pour utiliser celui des Réglages."
                : "Envoyé aux prospects intéressés. Aucun lien dans les Réglages pour l'instant : sans lien, le setter vous passe la main pour fixer le rendez-vous."
            }
          >
            <Input
              id="bookingUrl"
              name="bookingUrl"
              type="url"
              value={bookingUrl}
              onChange={(e) => setBookingUrl(e.target.value)}
              placeholder={workspace.bookingUrl || "https://calendly.com/vous/20min"}
            />
          </Field>
        </CardBody>
      </Card>

      <StickyActionBar>
        {barState?.error || barState?.message ? (
          <div className="min-w-0 flex-1 basis-64">
            <FormMessage state={barState} />
          </div>
        ) : null}
        <ButtonLink href={campaignId ? `/campaigns/${campaignId}` : "/campaigns"} variant="ghost">
          Annuler
        </ButtonLink>
        <Button type="submit" disabled={pending} aria-busy={pending}>
          {pending ? "Enregistrement…" : campaignId ? "Enregistrer" : "Créer la campagne"}
        </Button>
      </StickyActionBar>
    </form>
  );
}

/** Acceptation → +4 h premier message (J0) → J+3 relance 1 → … → J+15 sans réponse. */
function CadenceLine({ followUps }: { followUps: FollowUpStep[] }) {
  const items: ReactNode[] = [
    "Acceptation",
    `+${FIRST_MESSAGE_DELAY_HOURS} h premier message (J0)`,
    ...sequenceTimeline(followUps).map((t) => `J+${t.dayFromFirst} relance ${t.index}`),
    <span key="end" className="text-warning">J+{sequenceEndDay(followUps)} sans réponse</span>,
  ];
  return (
    <div className="rounded-control border border-line bg-surface-2 px-3 py-2.5 text-xs text-ink-2">
      <p className="mb-1 font-medium text-ink">Déroulé pour chaque prospect</p>
      <ol className="flex flex-wrap items-center gap-x-1.5 gap-y-1">
        {items.map((item, i) => (
          <li key={i} className="flex items-center gap-1.5 tabular-nums">
            {i > 0 ? <ArrowRight className="size-3 text-muted" aria-hidden /> : null}
            {item}
          </li>
        ))}
        <li className="text-muted">· arrêt dès la première réponse</li>
      </ol>
    </div>
  );
}

/**
 * Message textarea with insert chips for the variables (at the caret), a "{A|B}" button that turns the
 * selection into variants, live checks of unknown variables, and a characters · variants footer.
 */
function TemplateEditor({
  id,
  name,
  label,
  value,
  onChange,
  rows = 4,
  maxLength,
  serverError,
  hint,
  required,
  "aria-label": ariaLabel,
}: {
  id: string;
  name?: string;
  label?: ReactNode;
  value: string;
  onChange: (value: string) => void;
  rows?: number;
  maxLength?: number;
  serverError?: string;
  hint?: ReactNode;
  required?: boolean;
  "aria-label"?: string;
}) {
  const ref = useRef<HTMLTextAreaElement>(null);
  // Until the textarea has been focused, its caret position means nothing: insert at the end.
  const touched = useRef(false);
  const unknown = unknownVariables(value);
  const error = unknown.length > 0 ? unknown.map(unknownVariableHint).join(" ") : serverError;
  const tooLong = maxLength !== undefined && value.length > maxLength;
  const variants = countVariants(value);
  const describedBy = [error ? `${id}-error` : null, `${id}-meta`].filter(Boolean).join(" ");
  const subject = ariaLabel ?? (typeof label === "string" ? label : "le message");

  const replaceSelection = (make: (selected: string) => { text: string; caret: number }) => {
    const el = ref.current;
    const start = el && touched.current ? el.selectionStart : value.length;
    const end = el && touched.current ? el.selectionEnd : value.length;
    const { text, caret } = make(value.slice(start, end));
    onChange(value.slice(0, start) + text + value.slice(end));
    const position = start + caret;
    requestAnimationFrame(() => {
      el?.focus();
      el?.setSelectionRange(position, position);
    });
  };

  return (
    <div className="space-y-1.5">
      {label ? (
        <label htmlFor={id} className="block text-sm font-medium text-ink">
          {label}
        </label>
      ) : null}
      <div role="group" aria-label={`Insérer dans : ${subject}`} className="flex gap-1.5 overflow-x-auto pb-1 sm:flex-wrap sm:overflow-visible sm:pb-0">
        {TEMPLATE_VARIABLES.map((v) => (
          <button
            key={v}
            type="button"
            onClick={() => replaceSelection(() => ({ text: `{{${v}}}`, caret: v.length + 4 }))}
            title={`Insère {{${v}}}`}
            className={buttonClass({ variant: "secondary", size: "sm" }, "shrink-0 font-normal text-ink-2")}
          >
            {VARIABLE_LABELS_FR[v]}
          </button>
        ))}
        <button
          type="button"
          onClick={() =>
            replaceSelection((selected) => (selected ? { text: `{${selected}|}`, caret: selected.length + 2 } : { text: "{|}", caret: 1 }))
          }
          title="Transforme la sélection en variantes {texte|autre texte} : chaque prospect reçoit l'une d'elles."
          className={buttonClass({ variant: "secondary", size: "sm" }, "shrink-0 font-normal text-ink-2")}
        >
          <span aria-hidden className="font-mono text-brand-700">
            {"{A|B}"}
          </span>
          Variante
        </button>
      </div>
      <Textarea
        ref={ref}
        id={id}
        name={name}
        rows={rows}
        value={value}
        maxLength={maxLength}
        required={required}
        aria-label={label ? undefined : ariaLabel}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        onFocus={() => {
          touched.current = true;
        }}
        onChange={(e) => onChange(e.target.value)}
        className="min-h-20 [field-sizing:content]"
      />
      {error ? (
        <p id={`${id}-error`} className="text-xs text-danger">
          {error}
        </p>
      ) : null}
      <p id={`${id}-meta`} className="text-xs text-muted">
        <span className={cn("tabular-nums", tooLong && "font-medium text-danger")}>
          {maxLength !== undefined ? `${value.length}/${maxLength} caractères` : plural(value.length, "caractère")}
        </span>
        {" · "}
        <span className="tabular-nums">{plural(variants, "variante")}</span>
        {hint ? <> · {hint}</> : null}
      </p>
    </div>
  );
}

function Chip({ name, value, label, defaultChecked }: { name: string; value: string; label: string; defaultChecked: boolean }) {
  return (
    <label className="flex min-h-9 cursor-pointer items-center gap-1.5 rounded-control border border-line px-2.5 py-1.5 text-sm text-ink hover:border-line-strong has-[:checked]:border-brand-500 has-[:checked]:bg-brand-50 max-sm:min-h-11 pointer-coarse:min-h-11">
      <input type="checkbox" name={name} value={value} defaultChecked={defaultChecked} className={checkbox} />
      {label}
    </label>
  );
}
