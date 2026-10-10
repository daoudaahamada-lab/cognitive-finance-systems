import { Check, Minus } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { ButtonLink } from "@/components/ui/button";
import { cn } from "@/lib/cn";
import { formatNumber } from "@/lib/format";
import { PRICING, annualMonthlyPrice } from "@/lib/pricing";
import { PLANS } from "@/server/domain/plans";

export const metadata: Metadata = {
  title: "Tarifs",
  description: `Trois plans à prix fixe, setter IA inclus dès le plan Pro. ${PRICING.trialDays} jours d'essai gratuit, sans carte bancaire.`,
};

type Key = keyof typeof PLANS;

const PITCH: Record<Key, string> = {
  STARTER: "Pour lancer votre prospection et répondre vous-même.",
  PRO: "Pour déléguer les réponses au setter et réserver plus de rendez-vous.",
  AGENCY: "Pour les équipes et les agences qui gèrent plusieurs comptes.",
};

const ROWS: { label: string; value: (k: Key) => string | boolean }[] = [
  { label: "Comptes LinkedIn", value: (k) => (PLANS[k].maxAccounts === 1 ? "1" : `${PLANS[k].includedAccounts} inclus, jusqu'à ${PLANS[k].maxAccounts}`) },
  { label: "Nouveaux prospects", value: (k) => (PLANS[k].weeklyProspects ? `${PLANS[k].weeklyProspects} / semaine / campagne` : "Illimités, dans les quotas LinkedIn") },
  { label: "Relances automatiques", value: (k) => `Jusqu'à ${PLANS[k].maxFollowUps}` },
  { label: "Signaux d'achat et engagement", value: () => true },
  { label: "Scoring et messages personnalisés par Claude", value: () => true },
  { label: "Setter IA (réponses et prise de rendez-vous)", value: (k) => PLANS[k].setter },
  { label: "Import de listes de prospects", value: (k) => PLANS[k].listImport },
  { label: "Plafonds de sécurité et horaires d'envoi", value: () => true },
];

export default async function PricingPage({ searchParams }: { searchParams: Promise<{ facturation?: string }> }) {
  const annual = (await searchParams).facturation === "annuelle";
  const price = (k: Key) => (annual ? annualMonthlyPrice(PRICING.monthly[k]) : PRICING.monthly[k]);

  return (
    <section className="py-16 sm:py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="text-center">
          <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Un prix fixe, sans surprise</h1>
          <p className="mx-auto mt-4 max-w-xl text-muted">
            {PRICING.trialDays} jours d&apos;essai avec toutes les fonctionnalités Pro, sans carte bancaire. Prix hors taxes, par mois.
          </p>
          <div className="mt-8 inline-flex rounded-xl border border-line bg-canvas p-1 text-sm" role="group" aria-label="Facturation">
            <Link href="/tarifs" aria-current={!annual ? "true" : undefined} className={cn("rounded-lg px-4 py-1.5", !annual ? "bg-surface font-medium shadow-sm" : "text-muted")}>
              Mensuelle
            </Link>
            <Link href="/tarifs?facturation=annuelle" aria-current={annual ? "true" : undefined} className={cn("rounded-lg px-4 py-1.5", annual ? "bg-surface font-medium shadow-sm" : "text-muted")}>
              Annuelle <span className="text-emerald-700">−{Math.round(PRICING.annualDiscount * 100)} %</span>
            </Link>
          </div>
        </div>

        <div className="mt-12 grid gap-6 lg:grid-cols-3">
          {(Object.keys(PLANS) as Key[]).map((k) => {
            const featured = k === "PRO";
            return (
              <div key={k} className={cn("flex flex-col rounded-3xl border p-7", featured ? "border-brand-500 bg-brand-50/40 shadow-[0_20px_50px_-24px_rgba(79,70,229,0.45)]" : "border-line")}>
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold">{PLANS[k].label}</h2>
                  {featured ? <span className="rounded-full bg-brand-600 px-2.5 py-0.5 text-xs font-medium text-white">Le plus choisi</span> : null}
                </div>
                <p className="mt-2 min-h-10 text-sm text-muted">{PITCH[k]}</p>
                <p className="mt-6">
                  <span className="text-4xl font-semibold tracking-tight">{price(k)} €</span>
                  <span className="text-sm text-muted"> HT / mois</span>
                </p>
                <p className="mt-1 h-5 text-xs text-muted">
                  {annual ? `Facturé ${formatNumber(price(k) * 12)} € HT par an` : ""}
                  {k === "AGENCY" ? `${annual ? " · " : ""}+${PRICING.extraAccount} € par compte supplémentaire` : ""}
                </p>
                <ButtonLink href="/signup" variant={featured ? "primary" : "secondary"} className="mt-6 h-11">
                  Commencer l&apos;essai gratuit
                </ButtonLink>
                <ul className="mt-8 space-y-3 text-sm">
                  {ROWS.map((row) => {
                    const v = row.value(k);
                    return (
                      <li key={row.label} className={cn("flex gap-2.5", v === false && "text-muted")}>
                        {v === false ? <Minus className="mt-0.5 size-4 shrink-0" aria-label="Non inclus" /> : <Check className="mt-0.5 size-4 shrink-0 text-emerald-600" aria-hidden />}
                        <span>
                          {row.label}
                          {typeof v === "string" ? <span className="text-muted"> : {v}</span> : null}
                        </span>
                      </li>
                    );
                  })}
                </ul>
              </div>
            );
          })}
        </div>

        <p className="mx-auto mt-10 max-w-2xl text-center text-sm text-muted">
          Sans engagement en facturation mensuelle. Les appels à Claude sont inclus dans le prix des plans.
        </p>
      </div>
    </section>
  );
}
