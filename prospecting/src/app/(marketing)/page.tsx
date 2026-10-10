import { Bot, CalendarCheck, Check, Gauge, Inbox, MessageSquareText, Radar, ShieldCheck, Sparkles, Target, Users } from "lucide-react";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { ButtonLink } from "@/components/ui/button";
import { BRAND } from "@/lib/brand";

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
  { icon: Inbox, title: "Boîte de réception unique", text: "Les conversations qui demandent une décision remontent en haut, avec la raison. Les brouillons se valident en un clic." },
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
        <ol className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {STEPS.map((step, i) => (
            <li key={step.title} className="rounded-2xl border border-line bg-surface p-5">
              <div className="flex items-center gap-3">
                <span className="flex size-9 items-center justify-center rounded-xl bg-brand-50 text-brand-700">
                  <step.icon className="size-4" aria-hidden />
                </span>
                <span className="text-xs font-semibold text-muted">0{i + 1}</span>
              </div>
              <h3 className="mt-4 font-semibold">{step.title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-muted">{step.text}</p>
            </li>
          ))}
        </ol>
      </Section>

      <section id="setter" className="scroll-mt-20 bg-brand-900 py-20 text-white">
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

      <Section id="securite" eyebrow="Sécurité" title="Des limites prudentes, appliquées automatiquement" intro="LinkedIn ne publie pas de limites officielles. Le moteur applique les seuils couramment observés, sur des fenêtres glissantes, et s'arrête avant de les atteindre.">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[3fr_2fr]">
          <div className="overflow-x-auto rounded-2xl border border-line">
            <table className="w-full min-w-[480px] text-left text-sm">
              <thead className="bg-canvas text-xs uppercase tracking-wide text-muted">
                <tr>
                  <th className="px-5 py-3 font-medium">Type de compte</th>
                  <th className="px-5 py-3 font-medium">Invitations / semaine</th>
                  <th className="px-5 py-3 font-medium">Invitations / jour</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                <tr>
                  <td className="px-5 py-3">Gratuit</td>
                  <td className="px-5 py-3 font-semibold tabular-nums">100</td>
                  <td className="px-5 py-3 font-semibold tabular-nums">40</td>
                </tr>
                <tr>
                  <td className="px-5 py-3">Premium, Sales Navigator, Recruiter</td>
                  <td className="px-5 py-3 font-semibold tabular-nums">200</td>
                  <td className="px-5 py-3 font-semibold tabular-nums">40</td>
                </tr>
              </tbody>
            </table>
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
        <div className="mx-auto max-w-3xl divide-y divide-line rounded-2xl border border-line">
          {FAQ.map((item) => (
            <details key={item.q} className="group px-6 py-5">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 font-medium">
                {item.q}
                <span className="text-muted transition-transform group-open:rotate-45" aria-hidden>+</span>
              </summary>
              <p className="mt-3 text-sm leading-relaxed text-muted">{item.a}</p>
            </details>
          ))}
        </div>
      </Section>

      <section className="mx-auto max-w-6xl px-4 pb-20 sm:px-6">
        <div className="rounded-3xl bg-brand-600 px-6 py-14 text-center text-white sm:px-12">
          <h2 className="text-3xl font-semibold">Votre prochain rendez-vous commence par un bon premier message.</h2>
          <p className="mx-auto mt-3 max-w-xl text-brand-100">Configurez votre première campagne en quelques minutes. Le moteur se charge de la suite.</p>
          <ButtonLink href="/login" variant="secondary" className="mt-8 h-11 px-6 text-base">
            Ouvrir l&apos;application
          </ButtonLink>
        </div>
      </section>
    </>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div aria-hidden className="pointer-events-none absolute inset-x-0 top-0 h-[520px] bg-gradient-to-b from-brand-50 to-transparent" />
      <div className="relative mx-auto grid max-w-6xl grid-cols-1 items-center gap-12 px-4 pb-24 pt-16 sm:px-6 lg:grid-cols-[1.1fr_1fr] lg:pt-24">
        <div>
          <p className="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-surface px-3 py-1 text-xs font-medium text-brand-700">
            <Sparkles className="size-3.5" aria-hidden /> Propulsé par Claude
          </p>
          <h1 className="mt-6 text-4xl font-semibold leading-[1.1] tracking-tight sm:text-5xl lg:text-[3.4rem]">
            Des rendez-vous qualifiés depuis LinkedIn, sans y passer vos journées.
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted">
            {BRAND.name} trouve les bons prospects, engage la conversation avec un message qui leur parle, relance au bon moment et réserve le rendez-vous dans votre agenda. Vous gardez
            la main sur ce qui compte.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-3">
            <ButtonLink href="/login" className="h-11 px-6 text-base">
              Ouvrir l&apos;application
            </ButtonLink>
            <ButtonLink href="/#fonctionnement" variant="ghost" className="h-11 px-4 text-base">
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
    <section id={id} className="scroll-mt-20 py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-sm font-semibold uppercase tracking-widest text-brand-600">{eyebrow}</p>
        <h2 className="mt-3 max-w-3xl text-3xl font-semibold leading-tight tracking-tight sm:text-4xl">{title}</h2>
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
      <ShieldCheck className="mt-0.5 size-4 shrink-0 text-emerald-600" aria-hidden />
      <span>{children}</span>
    </li>
  );
}

/** Illustration: a scored prospect card. Example data, clearly fictional. */
function ProspectMock() {
  return (
    <div aria-hidden className="relative min-w-0 sm:pb-10">
      <div className="rounded-3xl border border-line bg-surface p-5 shadow-[0_24px_60px_-24px_rgba(49,46,129,0.35)]">
        <div className="flex items-center gap-3">
          <span className="flex size-11 items-center justify-center rounded-full bg-[#0e7490] text-sm font-semibold text-white">CD</span>
          <div className="min-w-0 flex-1">
            <p className="font-semibold">Camille Durand</p>
            <p className="truncate text-sm text-muted">Directrice financière · Nova Conseil · 51-200 sal.</p>
          </div>
          <span className="rounded-lg bg-emerald-50 px-2.5 py-1 text-sm font-semibold text-emerald-700">92</span>
        </div>
        <p className="mt-4 rounded-xl bg-canvas px-3 py-2.5 text-sm">Décide du reporting dans une PME de conseil en croissance : cible prioritaire.</p>
        <ul className="mt-3 space-y-1.5 text-sm">
          <li className="flex justify-between"><span>Poste de décision financière</span><span className="text-emerald-700">Favorable</span></li>
          <li className="flex justify-between"><span>Son entreprise recrute</span><span className="text-emerald-700">Favorable</span></li>
          <li className="flex justify-between text-muted"><span>Hors des zones prioritaires</span><span>Défavorable</span></li>
        </ul>
        <div className="mt-5 flex items-center justify-between border-t border-line pt-4 text-xs text-muted">
          <span className="inline-flex items-center gap-1.5"><Sparkles className="size-3.5 text-brand-600" /> Évalué par Claude</span>
          <span className="rounded-md bg-brand-50 px-2 py-0.5 font-medium text-brand-700">Invitation programmée</span>
        </div>
        <div className="hidden h-16 sm:block" />
      </div>
      <div className="absolute -bottom-2 left-8 hidden w-56 rounded-2xl border border-line bg-surface p-4 shadow-lg sm:block">
        <p className="text-xs text-muted">Invitations (7 jours)</p>
        <p className="mt-1 text-sm font-semibold">142 / 200</p>
        <div className="mt-2 h-1.5 rounded-full bg-zinc-100">
          <div className="h-full w-[71%] rounded-full bg-brand-600" />
        </div>
      </div>
    </div>
  );
}

/** Illustration: a setter conversation. Example data, clearly fictional. */
function SetterMock() {
  return (
    <div aria-hidden className="rounded-3xl bg-surface p-5 text-ink shadow-2xl">
      <div className="flex items-center justify-between border-b border-line pb-3">
        <p className="text-sm font-semibold">Thomas Girard · CFO, Atlas Labs</p>
        <span className="rounded-md bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-800">A répondu</span>
      </div>
      <div className="space-y-3 py-4 text-sm">
        <Bubble side="right" label="Séquence">Merci pour la connexion Thomas. Comment se passe la clôture mensuelle chez Atlas Labs depuis votre levée de fonds ?</Bubble>
        <Bubble side="left">Honnêtement, c&apos;est là que ça coince. Vous faites quoi exactement ?</Bubble>
        <Bubble side="right" label="Setter IA">
          Nous connectons votre comptabilité et votre banque à un reporting prêt pour le comité de direction, sans changer d&apos;outil. Le plus simple est d&apos;en parler 20 minutes : cal.example.com/alex
        </Bubble>
      </div>
      <div className="rounded-xl bg-emerald-50 px-3 py-2.5 text-sm text-emerald-900">
        <span className="font-semibold">Rendez-vous réservé</span> · jeudi 14:00
      </div>
    </div>
  );
}

function Bubble({ side, label, children }: { side: "left" | "right"; label?: string; children: ReactNode }) {
  return (
    <div className={side === "right" ? "flex flex-col items-end" : "flex flex-col items-start"}>
      <p className={side === "right" ? "max-w-[85%] rounded-2xl rounded-br-sm bg-brand-600 px-3.5 py-2.5 text-white" : "max-w-[85%] rounded-2xl rounded-bl-sm border border-line bg-canvas px-3.5 py-2.5"}>
        {children}
      </p>
      {label ? <span className="mt-1 text-[11px] text-muted">{label}</span> : null}
    </div>
  );
}
