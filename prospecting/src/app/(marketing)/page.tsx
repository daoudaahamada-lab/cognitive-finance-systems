import { Bot, CalendarCheck, Check, Gauge, Inbox, MessageSquareText, Radar, ShieldCheck, Sparkles, Target, Users } from "lucide-react";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { LogoMark } from "@/components/layout/logo";
import { LabeledBadge } from "@/components/ui/badge";
import { ButtonLink } from "@/components/ui/button";
import { Avatar } from "@/components/ui/misc";
import { BRAND } from "@/lib/brand";
import { cn } from "@/lib/cn";
import { STAGE_LABELS } from "@/lib/labels";

export const metadata: Metadata = {
  title: { absolute: `${BRAND.name} · ${BRAND.tagline}` },
  description:
    "Ciblage, messages personnalisés, relances et setter IA qui répond à vos prospects et réserve vos rendez-vous. Dans des limites prudentes pour votre compte LinkedIn.",
};

const STEPS = [
  { icon: Target, title: "Ciblez", text: "Décrivez votre offre et votre client idéal. Ajoutez des critères, des signaux d'achat, des posts à surveiller ou votre propre liste." },
  { icon: Gauge, title: "Notez", text: "Chaque profil reçoit une note sur 100, avec les raisons. Seuls ceux qui passent votre seuil sont contactés." },
  { icon: Users, title: "Connectez", text: "Les invitations partent dans vos horaires, à un rythme humain, sans jamais dépasser les plafonds de sécurité." },
  { icon: MessageSquareText, title: "Conversez", text: "Un premier message adapté au profil, puis des relances espacées qui s'arrêtent dès la première réponse." },
  { icon: CalendarCheck, title: "Convertissez", text: "Le setter répond, lève les objections et envoie votre lien de réservation. Le rendez-vous arrive dans votre agenda." },
];

const FEATURES = [
  { icon: Radar, title: "Sources de prospects", text: "Recherche par critères, signaux (nouveau poste, recrutement, levée de fonds), personnes qui interagissent avec des posts, visiteurs de votre profil, import de listes." },
  { icon: Sparkles, title: "Scoring expliqué", text: "Claude évalue chaque profil au regard de votre offre et de votre client idéal. Vous voyez la note, la synthèse et chaque raison." },
  { icon: MessageSquareText, title: "Messages personnalisés", text: "Vous écrivez le message, Claude l'adapte à chaque personne à partir de son profil, sans rien inventer. Variables et variantes incluses." },
  { icon: Bot, title: "Setter IA", text: "Automatique, avec validation ou désactivé : vous choisissez par campagne jusqu'où il va." },
  { icon: Inbox, title: "Boîte de réception unique", text: "Les conversations qui demandent une décision remontent en haut, avec la raison. Les réponses proposées par le setter se valident en un clic." },
  { icon: Gauge, title: "Pilotage", text: "Entonnoir, taux d'acceptation et de réponse, rendez-vous, quotas par compte : tout sur un seul écran." },
];

const FAQ: { q: string; a: ReactNode }[] = [
  {
    q: "Le setter peut-il répondre n'importe quoi à mes prospects ?",
    a: "Non. Il s'appuie uniquement sur la description de votre offre, n'invente ni prix ni promesse, et le seul lien qu'il peut envoyer est votre lien de réservation. Les questions de prix, les sujets sensibles et tout ce dont il n'est pas sûr vous sont transmis. En mode validation, rien ne part sans votre accord.",
  },
  {
    q: "Mon compte LinkedIn risque-t-il quelque chose ?",
    a: `Les conditions d'utilisation de LinkedIn interdisent les outils d'automatisation tiers : aucun outil ne peut garantir qu'un compte ne sera jamais restreint. ${BRAND.name} réduit ce risque avec des plafonds prudents (100 invitations par semaine sur un compte gratuit, 200 sur un compte payant, 40 par jour au maximum), des envois uniquement dans vos horaires et un rythme espacé.`,
  },
  {
    q: "Puis-je garder mes propres messages ?",
    a: "Oui. Vous écrivez chaque étape de la séquence. La personnalisation par Claude se désactive par campagne ; dans ce cas, vos textes partent tels quels, avec leurs variables et leurs variantes.",
  },
  {
    q: "Avec quels agendas cela fonctionne-t-il ?",
    a: "Avec tout outil qui fournit un lien de réservation : Calendly, Cal.com, Google Agenda ou un autre. Le setter envoie ce lien aux prospects intéressés.",
  },
  {
    q: "Puis-je gérer plusieurs comptes LinkedIn ?",
    a: "Oui. Chaque compte a sa propre session, ses horaires d'envoi et ses plafonds, et une même personne n'est jamais contactée depuis deux comptes.",
  },
  {
    q: "Où sont mes données ?",
    a: `Sur votre instance : ${BRAND.name} s'héberge sur votre machine ou votre serveur, avec sa propre base PostgreSQL. Seules les informations nécessaires à chaque requête sont envoyées à Claude.`,
  },
];

export default function LandingPage() {
  return (
    <>
      <Hero />

      <Section id="fonctionnement" eyebrow="Fonctionnement" title="De la recherche au rendez-vous, en cinq étapes" intro="Vous fixez la cible, le ton et les limites. Le moteur s'occupe du reste, jour après jour.">
        {/* A numbered stepper on a 1px line: vertical on phones, horizontal from lg. */}
        <ol className="grid grid-cols-1 gap-8 lg:grid-cols-5 lg:gap-6">
          {STEPS.map((step, i) => (
            <li key={step.title} className="relative flex gap-4 lg:block">
              {i < STEPS.length - 1 ? (
                <span aria-hidden className="absolute -bottom-6 left-4 top-10 w-px bg-line lg:-right-2 lg:bottom-auto lg:left-12 lg:top-4 lg:h-px lg:w-auto" />
              ) : null}
              <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-brand-600 text-sm font-semibold tabular-nums text-white shadow-card">{i + 1}</span>
              <div className="min-w-0 lg:mt-5">
                <h3 className="flex items-center gap-2 font-semibold text-ink">
                  <step.icon className="size-4 text-brand-600" aria-hidden />
                  {step.title}
                </h3>
                <p className="mt-1.5 text-sm leading-relaxed text-muted">{step.text}</p>
              </div>
            </li>
          ))}
        </ol>
      </Section>

      <section id="setter" className="bg-brand-900 py-20 text-white">
        <div className="mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 px-4 sm:px-6 lg:grid-cols-2">
          <div>
            <p className="text-sm font-semibold uppercase tracking-widest text-brand-200">Setter IA</p>
            <h2 className="mt-3 text-3xl font-semibold leading-tight sm:text-4xl">Il répond comme vous le feriez, et vous passe la main quand il le faut.</h2>
            <p className="mt-4 text-brand-100">
              Quand un prospect répond, le setter lit toute la conversation, comprend l&apos;intention et agit : il propose un créneau, répond à une question à partir de votre offre, reconnaît une
              objection sans insister, ou remercie poliment après un refus.
            </p>
            <ul className="mt-8 space-y-4">
              <Mode title="Automatique" text="Il répond seul et vous signale ce qu'il ne doit pas traiter." />
              <Mode title="Validation" text="Il rédige, vous relisez, vous envoyez. Idéal pour démarrer." />
              <Mode title="Désactivé" text="Toutes les réponses arrivent dans votre boîte." />
            </ul>
          </div>
          <SetterMock />
        </div>
      </section>

      <Section eyebrow="Fonctionnalités" title="Tout ce qu'il faut pour prospecter sur LinkedIn, rien de plus">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div key={f.title} className="rounded-2xl border border-line bg-surface p-6">
              <f.icon className="size-5 text-brand-600" aria-hidden />
              <h3 className="mt-4 font-semibold">{f.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-muted">{f.text}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section
        id="securite"
        eyebrow="Sécurité"
        title="Des limites prudentes, appliquées automatiquement"
        intro={`LinkedIn ne publie pas de limites officielles. ${BRAND.name} applique les seuils couramment observés, compte vos envois des 7 derniers jours et s'arrête toujours avant la limite.`}
      >
        <div className="grid grid-cols-1 items-start gap-6 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
          <div>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <LimitTile value={100} label="Compte gratuit" />
              <LimitTile value={200} label="Premium" detail="Même plafond pour Sales Navigator et Recruiter." />
            </div>
            <p className="mt-4 text-sm text-muted">Quel que soit le compte, jamais plus de 40 invitations par jour.</p>
          </div>
          <ul className="space-y-3 text-sm">
            <Safety>Envois uniquement dans vos jours et horaires, au rythme de quelques actions à la fois.</Safety>
            <Safety>Une personne n&apos;est jamais recontactée depuis une autre campagne.</Safety>
            <Safety>Les demandes de suppression de données ou d&apos;arrêt des messages vous sont toujours transmises.</Safety>
            <Safety>Vous pouvez baisser chaque plafond, jamais le relever au-delà du seuil de sécurité.</Safety>
          </ul>
        </div>
      </Section>

      <Section id="faq" eyebrow="FAQ" title="Questions fréquentes">
        <div className="max-w-3xl divide-y divide-line rounded-2xl border border-line">
          {FAQ.map((item) => (
            <details key={item.q} className="group px-6 py-5">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 font-medium text-ink">
                {item.q}
                <span className="text-muted transition-transform group-open:rotate-45" aria-hidden>+</span>
              </summary>
              <p className="mt-3 text-sm leading-relaxed text-muted">{item.a}</p>
            </details>
          ))}
        </div>
      </Section>

      <section className="mx-auto max-w-6xl px-4 pb-20 sm:px-6">
        <div className="relative overflow-hidden rounded-3xl bg-brand-600 px-6 py-14 text-center text-white sm:px-12">
          {/* The sail glyph as a background motif. */}
          <LogoMark className="pointer-events-none absolute -bottom-16 -right-12 size-80 text-white opacity-[0.06] sm:-right-6" />
          <div className="relative">
            <h2 className="text-3xl font-semibold">Votre prochain rendez-vous commence par un bon premier message.</h2>
            <p className="mx-auto mt-3 max-w-xl text-brand-100">Configurez votre première campagne en quelques minutes. {BRAND.name} se charge de la suite.</p>
            <ButtonLink href="/login" variant="secondary" size="lg" className="mt-8">
              Ouvrir l&apos;application
            </ButtonLink>
          </div>
        </div>
      </section>
    </>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div aria-hidden className="pointer-events-none absolute inset-x-0 top-0 h-[520px] bg-gradient-to-b from-brand-50 to-transparent" />
      <div className="relative mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 px-4 pb-24 pt-16 sm:px-6 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] lg:pt-24">
        <div>
          <p className="inline-flex items-center gap-2 rounded-full border border-ai-line bg-surface px-3 py-1 text-xs font-medium text-ai">
            <Sparkles className="size-3.5" aria-hidden /> Propulsé par Claude
          </p>
          <h1 className="mt-6 text-4xl font-semibold leading-[1.1] tracking-tight text-ink sm:text-5xl lg:text-[3.4rem]">
            Des rendez-vous qualifiés depuis LinkedIn, sans y passer vos journées.
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted">
            {BRAND.name} trouve les bons prospects, engage la conversation avec un message qui leur parle, relance au bon moment et réserve le rendez-vous dans votre agenda. Vous gardez
            la main sur ce qui compte.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <ButtonLink href="/login" size="lg">
              Ouvrir l&apos;application
            </ButtonLink>
            <ButtonLink href="/#fonctionnement" variant="ghost" size="lg">
              Voir comment ça marche
            </ButtonLink>
          </div>
          <p className="mt-4 text-sm text-muted">Votre instance, vos comptes, vos données.</p>
        </div>
        <ProspectMock />
      </div>
    </section>
  );
}

function Section({ id, eyebrow, title, intro, children }: { id?: string; eyebrow: string; title: string; intro?: string; children: ReactNode }) {
  return (
    <section id={id} className="py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-sm font-semibold uppercase tracking-widest text-brand-600">{eyebrow}</p>
        <h2 className="mt-3 max-w-3xl text-3xl font-semibold leading-tight tracking-tight text-ink sm:text-4xl">{title}</h2>
        {intro ? <p className="mt-4 max-w-2xl text-muted">{intro}</p> : null}
        <div className="mt-10">{children}</div>
      </div>
    </section>
  );
}

function Mode({ title, text }: { title: string; text: string }) {
  return (
    <li className="flex gap-3">
      <span className="mt-1 flex size-5 shrink-0 items-center justify-center rounded-full bg-brand-600">
        <Check className="size-3" aria-hidden />
      </span>
      <span>
        <span className="font-semibold">{title}.</span> <span className="text-brand-100">{text}</span>
      </span>
    </li>
  );
}

function Safety({ children }: { children: ReactNode }) {
  return (
    <li className="flex gap-3 rounded-xl border border-line p-4">
      <ShieldCheck className="mt-0.5 size-4 shrink-0 text-success" aria-hidden />
      <span>{children}</span>
    </li>
  );
}

function LimitTile({ value, label, detail }: { value: number; label: string; detail?: string }) {
  return (
    <div className="rounded-2xl bg-brand-50 p-6">
      <p className="text-sm font-medium text-brand-700">{label}</p>
      <p className="mt-2 flex items-baseline gap-2">
        <span className="text-5xl font-semibold tracking-tight tabular-nums text-ink">{value}</span>
        <span className="text-base font-medium text-ink-2">/ semaine</span>
      </p>
      <p className="mt-1 text-sm text-ink-2">invitations au maximum</p>
      {detail ? <p className="mt-3 text-xs text-ink-2">{detail}</p> : null}
    </div>
  );
}

/** Illustration: a scored prospect card. Example data, clearly fictional. */
function ProspectMock() {
  return (
    <div aria-hidden className="relative min-w-0 sm:pb-8">
      <div className="rounded-3xl border border-line bg-surface p-5 shadow-pop">
        <div className="flex items-center gap-3">
          <Avatar first="Camille" last="Durand" size="lg" />
          <div className="min-w-0 flex-1">
            <p className="font-semibold text-ink">Camille Durand</p>
            <p className="truncate text-sm text-muted">Directrice financière · Nova Conseil · 51-200 sal.</p>
          </div>
          <span className="rounded-lg bg-success-soft px-2.5 py-1 text-sm font-semibold tabular-nums text-success">92</span>
        </div>
        <p className="mt-4 rounded-xl bg-canvas px-3 py-2.5 text-sm text-ink-2">Décide du reporting dans une PME de conseil en croissance : cible prioritaire.</p>
        <ul className="mt-3 space-y-1.5 text-sm">
          <li className="flex justify-between gap-3"><span>Poste de décision financière</span><span className="text-success">Favorable</span></li>
          <li className="flex justify-between gap-3"><span>Son entreprise recrute</span><span className="text-success">Favorable</span></li>
          <li className="flex justify-between gap-3 text-muted"><span>Hors des zones prioritaires</span><span>Défavorable</span></li>
        </ul>
        {/* Right-aligned on sm+: the quota chip overlaps the card's bottom-left corner. */}
        <div className="mt-5 flex flex-wrap items-center justify-between gap-2 border-t border-line pt-4 text-xs sm:justify-end">
          <span className="inline-flex items-center gap-1.5 text-ai"><Sparkles className="size-3.5" /> Évalué par Claude</span>
          <span className="rounded-md bg-brand-50 px-2 py-0.5 font-medium text-brand-700">Invitation programmée</span>
        </div>
      </div>
      <div className="absolute -left-4 bottom-0 hidden w-52 rounded-2xl border border-line bg-surface p-4 shadow-pop sm:block">
        <p className="text-xs text-muted">Invitations (7 jours)</p>
        <p className="mt-1 text-sm font-semibold tabular-nums text-ink">142 / 200</p>
        <div className="mt-2 h-1.5 rounded-full bg-line">
          <div className="h-full w-[71%] rounded-full bg-brand-600" />
        </div>
      </div>
    </div>
  );
}

/** Illustration: a setter conversation. Example data, clearly fictional. */
function SetterMock() {
  return (
    <div aria-hidden className="rounded-3xl bg-surface p-5 text-ink shadow-pop">
      <div className="flex items-center justify-between gap-3 border-b border-line pb-3">
        <p className="text-sm font-semibold">Thomas Girard · CFO, Atlas Labs</p>
        <LabeledBadge map={STAGE_LABELS} value="REPLIED" />
      </div>
      <div className="space-y-3 py-4 text-sm">
        <Bubble author="sequence">Merci d&apos;avoir accepté mon invitation, Thomas. Comment se passe la clôture mensuelle chez Atlas Labs depuis votre levée de fonds ?</Bubble>
        <Bubble author="prospect">Honnêtement, c&apos;est là que ça coince. Vous faites quoi exactement ?</Bubble>
        <Bubble author="setter">
          Nous connectons votre comptabilité et votre banque à un reporting prêt pour le comité de direction, sans changer d&apos;outil. Le plus simple est d&apos;en parler 20 minutes : cal.example.com/alex
        </Bubble>
      </div>
      <div className="rounded-xl bg-success-soft px-3 py-2.5 text-sm text-success">
        <span className="font-semibold">Rendez-vous réservé</span> · jeudi 14:00
      </div>
    </div>
  );
}

/** Same reading as the inbox: the sequence in grey, the setter in the AI tint, the prospect on the left. */
function Bubble({ author, children }: { author: "prospect" | "sequence" | "setter"; children: ReactNode }) {
  const outbound = author !== "prospect";
  return (
    <div className={outbound ? "flex flex-col items-end" : "flex flex-col items-start"}>
      <p
        className={cn(
          "max-w-[85%] rounded-2xl px-3.5 py-2.5",
          author === "prospect" && "rounded-bl-sm border border-line bg-surface text-ink shadow-card",
          author === "sequence" && "rounded-br-sm border border-line bg-surface-2 text-ink-2",
          author === "setter" && "rounded-br-sm border border-ai-line bg-ai-soft text-ai",
        )}
      >
        {children}
      </p>
      {outbound ? (
        <span className={cn("mt-1 inline-flex items-center gap-1 text-2xs", author === "setter" ? "text-ai" : "text-muted")}>
          {author === "setter" ? <Sparkles className="size-3" /> : null}
          {author === "setter" ? "Setter IA" : "Séquence"}
        </span>
      ) : null}
    </div>
  );
}
