import { Columns3, List, Search, Users } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import type { ProspectStage } from "@prisma/client";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { Button, ButtonLink } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/form";
import { Avatar, EmptyState, PageHeader, ScorePill } from "@/components/ui/misc";
import { cn } from "@/lib/cn";
import { formatNumber, formatRelative } from "@/lib/format";
import { SIGNALS, SOURCES, STAGE_LABELS } from "@/lib/labels";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { listProspects, prospectBoard, type ProspectFilters } from "@/server/services/prospects";

export const metadata: Metadata = { title: "Prospects" };

type Search = { stage?: string; campaignId?: string; q?: string; sort?: string; page?: string; view?: string; minScore?: string };

export default async function ProspectsPage({ searchParams }: { searchParams: Promise<Search> }) {
  const { workspace } = await requireContext();
  const sp = await searchParams;
  const filters: ProspectFilters = {
    stage: sp.stage && sp.stage in STAGE_LABELS ? (sp.stage as ProspectStage) : undefined,
    campaignId: sp.campaignId || undefined,
    q: sp.q,
    minScore: sp.minScore ? Number(sp.minScore) : undefined,
    sort: sp.sort === "score" ? "score" : "recent",
    page: Number(sp.page) || 1,
  };
  const view = sp.view === "board" ? "board" : "table";
  const campaigns = await db.campaign.findMany({ where: { workspaceId: workspace.id }, select: { id: true, name: true }, orderBy: { createdAt: "desc" } });

  const href = (patch: Partial<Search>) => {
    const params = new URLSearchParams(Object.entries({ ...sp, ...patch }).filter(([, v]) => v) as [string, string][]);
    return `/prospects?${params.toString()}`;
  };

  return (
    <>
      <PageHeader title="Prospects" description="Tous les profils trouvés, notés et suivis par le moteur." />

      <form className="mb-4 flex flex-wrap items-center gap-2" action="/prospects">
        <input type="hidden" name="view" value={view} />
        <div className="relative w-full sm:w-64">
          <Search className="pointer-events-none absolute left-2.5 top-2.5 size-4 text-muted" aria-hidden />
          <Input name="q" defaultValue={sp.q} placeholder="Nom, entreprise, poste…" className="pl-8" aria-label="Rechercher" />
        </div>
        <Select name="campaignId" defaultValue={sp.campaignId ?? ""} className="w-auto" aria-label="Campagne">
          <option value="">Toutes les campagnes</option>
          {campaigns.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </Select>
        {view === "table" ? (
          <>
            <Select name="stage" defaultValue={sp.stage ?? ""} className="w-auto" aria-label="Étape">
              <option value="">Toutes les étapes</option>
              {Object.entries(STAGE_LABELS).map(([value, { label }]) => <option key={value} value={value}>{label}</option>)}
            </Select>
            <Select name="sort" defaultValue={filters.sort} className="w-auto" aria-label="Tri">
              <option value="recent">Activité récente</option>
              <option value="score">Meilleur score</option>
            </Select>
          </>
        ) : null}
        <Button type="submit" variant="secondary">Filtrer</Button>
        <div className="ml-auto flex rounded-lg border border-line bg-surface p-0.5">
          <Link href={href({ view: "table", page: "" })} aria-current={view === "table" ? "true" : undefined} className={cn("flex items-center gap-1.5 rounded-md px-2.5 py-1 text-sm", view === "table" ? "bg-canvas font-medium" : "text-muted")}>
            <List className="size-4" aria-hidden /> Liste
          </Link>
          <Link href={href({ view: "board", page: "" })} aria-current={view === "board" ? "true" : undefined} className={cn("flex items-center gap-1.5 rounded-md px-2.5 py-1 text-sm", view === "board" ? "bg-canvas font-medium" : "text-muted")}>
            <Columns3 className="size-4" aria-hidden /> Pipeline
          </Link>
        </div>
      </form>

      {view === "board" ? <Board workspaceId={workspace.id} filters={filters} /> : <ProspectTable workspaceId={workspace.id} filters={filters} href={href} />}
    </>
  );
}

async function ProspectTable({ workspaceId, filters, href }: { workspaceId: string; filters: ProspectFilters; href: (p: Partial<Search>) => string }) {
  const { rows, total, page, pages } = await listProspects(workspaceId, filters);
  if (total === 0) {
    return (
      <Card>
        <EmptyState icon={<Users className="size-5" />} title="Aucun prospect" description="Lancez une campagne : le moteur trouve et note les prospects automatiquement." action={<ButtonLink href="/campaigns">Voir les campagnes</ButtonLink>} />
      </Card>
    );
  }
  return (
    <Card>
      <div className="overflow-x-auto">
        <table className="data-table">
          <thead>
            <tr>
              <th>Prospect</th>
              <th>Entreprise</th>
              <th>Score</th>
              <th>Étape</th>
              <th>Origine</th>
              <th>Campagne</th>
              <th className="text-right">Mis à jour</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((p) => (
              <tr key={p.id}>
                <td>
                  <Link href={`/prospects/${p.id}`} className="flex items-center gap-3">
                    <Avatar first={p.firstName} last={p.lastName} size="sm" />
                    <span className="min-w-0">
                      <span className="block truncate font-medium hover:underline">{p.firstName} {p.lastName}</span>
                      <span className="block max-w-56 truncate text-xs text-muted">{p.title}</span>
                    </span>
                  </Link>
                </td>
                <td>
                  <span className="block">{p.company}</span>
                  <span className="block text-xs text-muted">{p.industry} · {p.location}</span>
                </td>
                <td><ScorePill score={p.score} /></td>
                <td><LabeledBadge map={STAGE_LABELS} value={p.stage} /></td>
                <td className="text-xs">
                  {p.signal ? <Badge tone="amber">{SIGNALS[p.signal] ?? p.signal}</Badge> : <span className="text-muted">{SOURCES[p.source]?.label}</span>}
                </td>
                <td className="max-w-40 truncate text-xs text-muted">{p.campaign.name}</td>
                <td className="text-right text-xs text-muted">{formatRelative(p.stageChangedAt)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between border-t border-line px-4 py-3 text-sm text-muted">
        <span>{formatNumber(total)} prospect{total > 1 ? "s" : ""}</span>
        <div className="flex items-center gap-2">
          {page > 1 ? <ButtonLink href={href({ page: String(page - 1) })} variant="secondary" size="sm">Précédent</ButtonLink> : null}
          <span>Page {page} / {pages}</span>
          {page < pages ? <ButtonLink href={href({ page: String(page + 1) })} variant="secondary" size="sm">Suivant</ButtonLink> : null}
        </div>
      </div>
    </Card>
  );
}

async function Board({ workspaceId, filters }: { workspaceId: string; filters: ProspectFilters }) {
  const columns = await prospectBoard(workspaceId, filters);
  return (
    <div className="flex gap-3 overflow-x-auto pb-4">
      {columns.map((col) => (
        <section key={col.stage} className="w-64 shrink-0 rounded-xl bg-zinc-100/70 p-2" aria-label={STAGE_LABELS[col.stage]?.label}>
          <header className="mb-2 flex items-center justify-between px-1.5 py-1">
            <LabeledBadge map={STAGE_LABELS} value={col.stage} />
            <span className="text-xs font-medium tabular-nums text-muted">{col.count}</span>
          </header>
          <ul className="max-h-[calc(100vh-17rem)] space-y-2 overflow-y-auto">
            {col.items.map((p) => (
              <li key={p.id}>
                <Link href={`/prospects/${p.id}`} className="block rounded-lg border border-line bg-surface p-3 shadow-sm hover:border-brand-200">
                  <div className="flex items-start justify-between gap-2">
                    <p className="truncate text-sm font-medium">{p.firstName} {p.lastName}</p>
                    <ScorePill score={p.score} />
                  </div>
                  <p className="mt-0.5 truncate text-xs text-muted">{p.title}</p>
                  <p className="truncate text-xs text-muted">{p.company}</p>
                  <p className="mt-2 text-[11px] text-muted">{formatRelative(p.stageChangedAt)}</p>
                </Link>
              </li>
            ))}
            {col.count > col.items.length ? <li className="px-2 text-xs text-muted">+ {col.count - col.items.length} autres</li> : null}
            {col.count === 0 ? <li className="px-2 py-4 text-center text-xs text-muted">Vide</li> : null}
          </ul>
        </section>
      ))}
    </div>
  );
}
