import type { ReactNode } from "react";

/** Layout for legal pages. Bracketed fields are placeholders the operator must fill in before launch. */
export function LegalPage({ title, updated, children }: { title: string; updated: string; children: ReactNode }) {
  return (
    <article className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
      <h1 className="text-3xl font-semibold tracking-tight text-ink">{title}</h1>
      <p className="mt-2 text-sm text-muted">Dernière mise à jour : {updated}</p>
      <p className="mt-6 rounded-xl border border-warning-line bg-warning-soft px-4 py-3 text-sm text-warning">
        Modèle à compléter et à faire relire avant la mise en ligne : les champs entre crochets doivent être remplacés par les informations de l&apos;éditeur.
      </p>
      <div className="mt-10 space-y-8 text-base leading-relaxed [&_h2]:text-lg [&_h2]:font-semibold [&_p]:mt-3 [&_p]:text-muted [&_ul]:mt-3 [&_ul]:list-disc [&_ul]:space-y-1 [&_ul]:pl-5 [&_ul]:text-muted">
        {children}
      </div>
    </article>
  );
}
