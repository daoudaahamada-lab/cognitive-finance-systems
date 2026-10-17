import { Columns3, List, Search, SearchX, Upload, Users } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import type { ProspectStage } from "@prisma/client";
import { LabeledBadge } from "@/components/ui/badge";
import { Button, ButtonLink } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input, Select } from "@/components/ui/form";
import { Avatar, EmptyState, PageHeader, ScorePill } from "@/components/ui/misc";
import { SegmentedControl } from "@/components/ui/segmented-control";
import { cn } from "@/lib/cn";
import { formatNumber, formatRelative, plural } from "@/lib/format";
import { SOURCES, STAGE_LABELS } from "@/lib/labels";
import { toneClasses } from "@/lib/tones";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { listProspects, prospectBoard, type ProspectFilters } from "@/server/services/prospects";
import { FilterAutosubmit } from "./filter-autosubmit";
import { SignalBadge, SignalGlyph, SignalIcon, signalLabel } from "./signal-badge";

export const metadata: Metadata = { title: "Prospects" };

type Search = { stage?: string; campaignId?: string; q?: string; sort?: string; page?: string; view?: string; minScore?: string };
type Href = (patch: Partial<Search>) => string;
type Row = Awaited<ReturnType<typeof listProspects>>["rows"][number];
type BoardItem = Awaited<ReturnType<typeof prospectBoard>>[number]["items"][number];

/** Table cells, without .data-table: its unlayered rules would override the denser padding and the sticky header. */
const TH = "sticky top-(--app-header-h) z-10 bg-surface-2 px-4 py-2.5 text-left text-xs font-medium tracking-wide whitespace-nowrap text-muted uppercase shadow-[inset_0_-1px_0_var(--color-line)] first:rounded-tl-card last:rounded-tr-card";
const TD = "border-b border-line px-4 py-2.5 align-middle";

function fullName(p: { firstName: string; lastName: string }) {
  return `${p.firstName} ${p.lastName}`;
}

/** "Poste · Entreprise", whichever is known. */
function roleAtCompany(p: { title: string; company: string }) {
  return [p.title, p.company].filter(Boolean).join(" · ");
}

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
  const campaigns = await db.campaign.findMany({
    where: { workspaceId: workspace.id },
    select: { id: true, name: true, status: true, _count: { select: { prospects: true } } },
    orderBy: { createdAt: "desc" },
  });
  // 'Importer une liste' opens the import panel of the most recent campaign still in use.
  const importTarget = campaigns.find((c) => c.status !== "ARCHIVED");
  // The Campagne column only helps when prospects come from several campaigns and none is filtered.
  const showCampaign = !filters.campaignId && campaigns.filter((c) => c._count.prospects > 0).length >= 2;
  const filtered = Boolean(filters.q?.trim() || filters.campaignId || filters.minScore || (view === "table" && filters.stage));

  const href: Href = (patch) => {
    const params = new URLSearchParams(Object.entries({ ...sp, ...patch }).filter(([, v]) => v) as [string, string][]);
    return `/prospects?${params.toString()}`;
  };

  return (
    <>
      <PageHeader
        title="Prospects"
        description="Tous les profils trouvés, notés et suivis par le moteur."
        actions={
          importTarget ? (
            <ButtonLink href={`/campaigns/${importTarget.id}#import`} variant="secondary">
              <Upload className="size-4" aria-hidden /> Importer une liste
            </ButtonLink>
          ) : null
        }
      />

      <FilterAutosubmit
        action="/prospects"
        label="Filtrer les prospects"
        values={{ q: sp.q ?? "", campaignId: filters.campaignId ?? "", stage: filters.stage ?? "", sort: filters.sort ?? "recent" }}
        className="mb-4 flex flex-wrap items-center gap-2"
      >
        <input type="hidden" name="view" value={view} />
        <div className="relative w-full sm:w-64">
          <Search className="pointer-events-none absolute left-2.5 top-1/2 size-4 -translate-y-1/2 text-muted" aria-hidden />
          <Input name="q" defaultValue={sp.q} placeholder="Nom, entreprise, poste…" className="pl-8" aria-label="Rechercher un prospect" enterKeyHint="search" />
        </div>
        <Select name="campaignId" defaultValue={sp.campaignId ?? ""} className="min-w-36 flex-1 sm:w-auto sm:max-w-64 sm:flex-none" aria-label="Campagne">
          <option value="">Toutes les campagnes</option>
          {campaigns.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </Select>
        {view === "table" ? (
          <>
            <Select name="stage" defaultValue={filters.stage ?? ""} className="min-w-36 flex-1 sm:w-auto sm:flex-none" aria-label="Étape">
              <option value="">Toutes les étapes</option>
              {Object.entries(STAGE_LABELS).map(([value, { label }]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
            <Select name="sort" defaultValue={filters.sort} className="min-w-36 flex-1 sm:w-auto sm:flex-none" aria-label="Tri">
              <option value="recent">Activité récente</option>
              <option value="score">Meilleur score</option>
            </Select>
          </>
        ) : null}
        <noscript>
          <Button type="submit" variant="secondary">
            Filtrer
          </Button>
        </noscript>
        <SegmentedControl
          label="Affichage"
          value={view}
          className="ml-auto"
          items={[
            { href: href({ view: "table", page: "" }), value: "table", label: "Liste", icon: <List className="size-4" aria-hidden /> },
            { href: href({ view: "board", page: "" }), value: "board", label: "Pipeline", icon: <Columns3 className="size-4" aria-hidden /> },
          ]}
        />
      </FilterAutosubmit>

      {view === "board" ? (
        <Board workspaceId={workspace.id} filters={filters} href={href} filtered={filtered} />
      ) : (
        <ProspectTable workspaceId={workspace.id} filters={filters} href={href} showCampaign={showCampaign} filtered={filtered} />
      )}
    </>
  );
}

function NoResults({ clearHref }: { clearHref: string }) {
  return (
    <Card>
      <EmptyState
        icon={<SearchX className="size-5" aria-hidden />}
        title="Aucun résultat pour ces filtres"
        description="Essayez un autre nom, une autre campagne ou une autre étape."
        action={
          <ButtonLink href={clearHref} variant="secondary">
            Effacer les filtres
          </ButtonLink>
        }
      />
    </Card>
  );
}

function NoProspects() {
  return (
    <Card>
      <EmptyState
        icon={<Users className="size-5" aria-hidden />}
        title="Aucun prospect"
        description="Lancez une campagne : le moteur trouve et note les prospects automatiquement."
        action={<ButtonLink href="/campaigns">Voir les campagnes</ButtonLink>}
      />
    </Card>
  );
}

/** Signal (with its icon) or, failing that, where the prospect came from. */
function Origin({ p }: { p: Row }) {
  if (!p.signal) return <span className="text-xs text-muted">{SOURCES[p.source]?.label ?? p.source}</span>;
  return <SignalBadge signal={p.signal} />;
}

async function ProspectTable({
  workspaceId,
  filters,
  href,
  showCampaign,
  filtered,
}: {
  workspaceId: string;
  filters: ProspectFilters;
  href: Href;
  showCampaign: boolean;
  filtered: boolean;
}) {
  const { rows, total, page, pages } = await listProspects(workspaceId, filters);
  if (total === 0) return filtered ? <NoResults clearHref="/prospects" /> : <NoProspects />;
  const now = new Date();
  return (
    <Card>
      {/* Phones and small tablets: one card per prospect, score and stage always visible. */}
      <ul className="divide-y divide-line md:hidden">
        {rows.map((p) => (
          <ProspectListItem key={p.id} p={p} now={now} />
        ))}
      </ul>

      <table className="hidden w-full text-sm md:table">
        <thead>
          <tr>
            <th scope="col" className={TH}>Prospect</th>
            <th scope="col" className={TH}>Score</th>
            <th scope="col" className={TH}>Étape</th>
            <th scope="col" className={TH}>Origine</th>
            {showCampaign ? <th scope="col" className={cn(TH, "hidden xl:table-cell")}>Campagne</th> : null}
            <th scope="col" className={cn(TH, "text-right")}>Mis à jour</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((p) => (
            <tr key={p.id} className="hover:bg-surface-2 [&:last-child>td]:border-b-0">
              {/* w-full + max-w-0: this column takes the space left and truncates instead of widening the table. */}
              <td className={cn(TD, "w-full max-w-0")}>
                <Link
                  href={`/prospects/${p.id}`}
                  className="group flex items-center gap-3 rounded-control focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600"
                >
                  <Avatar first={p.firstName} last={p.lastName} size="sm" />
                  <span className="min-w-0">
                    <span className="block truncate leading-tight font-medium text-ink group-hover:underline">{fullName(p)}</span>
                    <span className="block truncate text-xs leading-tight text-muted">{roleAtCompany(p) || "—"}</span>
                  </span>
                </Link>
              </td>
              <td className={TD}>
                <ScorePill score={p.score} />
              </td>
              <td className={cn(TD, "whitespace-nowrap")}>
                <LabeledBadge map={STAGE_LABELS} value={p.stage} />
              </td>
              <td className={cn(TD, "whitespace-nowrap")}>
                <Origin p={p} />
              </td>
              {showCampaign ? (
                <td className={cn(TD, "hidden max-w-60 truncate text-xs text-muted xl:table-cell")} title={p.campaign.name}>
                  {p.campaign.name}
                </td>
              ) : null}
              <td className={cn(TD, "text-right text-xs whitespace-nowrap text-muted")}>{formatRelative(p.stageChangedAt, now)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-line px-4 py-3 text-sm text-muted">
        <span>{plural(total, "prospect")}</span>
        <div className="flex items-center gap-2">
          {page > 1 ? (
            <ButtonLink href={href({ page: String(page - 1) })} variant="secondary" size="sm">
              Précédent
            </ButtonLink>
          ) : null}
          <span className="tabular-nums">
            Page {page} / {pages}
          </span>
          {page < pages ? (
            <ButtonLink href={href({ page: String(page + 1) })} variant="secondary" size="sm">
              Suivant
            </ButtonLink>
          ) : null}
        </div>
      </div>
    </Card>
  );
}

function ProspectListItem({ p, now }: { p: Row; now: Date }) {
  return (
    <li>
      <Link
        href={`/prospects/${p.id}`}
        className="flex gap-3 px-4 py-3 hover:bg-surface-2 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand-600"
      >
        <Avatar first={p.firstName} last={p.lastName} />
        <span className="min-w-0 flex-1">
          <span className="flex items-center gap-2">
            <span className="min-w-0 flex-1 truncate text-sm font-medium text-ink">{fullName(p)}</span>
            <ScorePill score={p.score} />
          </span>
          <span className="mt-0.5 flex items-center gap-2">
            <span className="min-w-0 flex-1 truncate text-xs text-muted">{roleAtCompany(p) || "—"}</span>
            <LabeledBadge map={STAGE_LABELS} value={p.stage} />
          </span>
          <span className="mt-1.5 flex items-center gap-2 text-xs text-muted">
            <span className="flex min-w-0 flex-1 items-center gap-1">
              {p.signal ? <SignalGlyph signal={p.signal} className="size-3.5" /> : null}
              <span className="truncate">{p.signal ? signalLabel(p.signal) : (SOURCES[p.source]?.label ?? p.source)}</span>
            </span>
            <span className="shrink-0">{formatRelative(p.stageChangedAt, now)}</span>
          </span>
        </span>
      </Link>
    </li>
  );
}

async function Board({ workspaceId, filters, href, filtered }: { workspaceId: string; filters: ProspectFilters; href: Href; filtered: boolean }) {
  const columns = await prospectBoard(workspaceId, filters);
  if (filtered && columns.every((col) => col.count === 0)) return <NoResults clearHref="/prospects?view=board" />;
  const now = new Date();
  return (
    // Snaps column by column; phones bleed to the screen edges and scroll the page, not the columns.
    // `relative` keeps the sr-only texts inside the scroller, otherwise they widen the page.
    <div className="relative -mx-4 flex snap-x snap-mandatory scroll-px-4 items-start gap-3 overflow-x-auto px-4 pb-4 [mask-image:linear-gradient(to_right,#000_calc(100%-2.5rem),transparent)] sm:mx-0 sm:scroll-px-0 sm:px-0">
      {columns.map((col) => {
        const stage = STAGE_LABELS[col.stage] ?? { label: col.stage, tone: "neutral" as const };
        const accent = toneClasses(stage.tone).border;
        const titleId = `colonne-${col.stage}`;
        if (col.count === 0) {
          return (
            <section key={col.stage} aria-labelledby={titleId} className={cn("flex w-11 shrink-0 snap-start flex-col items-center gap-2 rounded-card border-t-2 bg-line/40 py-3", accent)}>
              <h2 id={titleId} className="text-sm font-semibold text-ink-2 [writing-mode:vertical-rl]">
                {stage.label}
              </h2>
              <span className="text-xs font-medium tabular-nums text-muted">
                0<span className="sr-only"> prospect</span>
              </span>
            </section>
          );
        }
        const more = col.count - col.items.length;
        return (
          <section key={col.stage} aria-labelledby={titleId} className={cn("w-[82vw] shrink-0 snap-start rounded-card border-t-2 bg-line/40 p-2 sm:w-[272px]", accent)}>
            <header className="mb-2 flex items-center justify-between gap-2 px-1.5 py-1">
              <h2 id={titleId} className="truncate text-sm font-semibold text-ink">
                {stage.label}
              </h2>
              <span className="rounded-full bg-surface px-2 py-0.5 text-xs font-medium tabular-nums text-ink-2 ring-1 ring-line ring-inset">
                {formatNumber(col.count)}
                <span className="sr-only"> {col.count > 1 ? "prospects" : "prospect"}</span>
              </span>
            </header>
            {/* From md the column scrolls on its own, above the mobile tab bar until lg; phones use the page scroll. */}
            <ul className="space-y-2 md:max-h-[calc(100dvh-17rem-var(--mobile-nav-h))] md:overflow-y-auto lg:max-h-[calc(100dvh-17rem)]">
              {col.items.map((p) => (
                <li key={p.id}>
                  <BoardCard p={p} now={now} />
                </li>
              ))}
              {more > 0 ? (
                <li>
                  <Link
                    href={href({ view: "table", stage: col.stage, page: "" })}
                    aria-label={`Voir les ${formatNumber(col.count)} prospects « ${stage.label} » dans la liste`}
                    className="block rounded-control px-2 py-1.5 text-xs font-medium text-brand-700 hover:bg-surface hover:underline focus-visible:outline-2 focus-visible:outline-brand-600"
                  >
                    + {plural(more, "autre")}
                  </Link>
                </li>
              ) : null}
            </ul>
          </section>
        );
      })}
      {/* Room for the fade mask, so the last column can scroll fully into view. */}
      <div aria-hidden className="w-6 shrink-0" />
    </div>
  );
}

function BoardCard({ p, now }: { p: BoardItem; now: Date }) {
  return (
    <Link
      href={`/prospects/${p.id}`}
      className="flex gap-2.5 rounded-control border border-line bg-surface p-2.5 shadow-card transition-colors hover:border-brand-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600"
    >
      <Avatar first={p.firstName} last={p.lastName} size="sm" />
      <span className="min-w-0 flex-1">
        <span className="flex items-center gap-1.5">
          <span className="min-w-0 flex-1 truncate text-sm font-medium text-ink">{fullName(p)}</span>
          {p.signal ? <SignalIcon signal={p.signal} /> : null}
          <ScorePill score={p.score} />
        </span>
        <span className="mt-0.5 block truncate text-xs text-muted">{roleAtCompany(p) || "—"}</span>
        <span className="mt-1 block text-2xs text-muted">{formatRelative(p.stageChangedAt, now)}</span>
      </span>
    </Link>
  );
}
