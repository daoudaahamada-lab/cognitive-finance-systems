import type { Campaign, LinkedInAccount } from "@prisma/client";
import { CircleCheck, CircleX, Clock, Info, Pencil, TriangleAlert, type LucideIcon } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import type { ReactNode } from "react";
import { FunnelChart } from "@/components/charts/funnel-chart";
import { Badge, LabeledBadge } from "@/components/ui/badge";
import { ButtonLink } from "@/components/ui/button";
import { Card, CardBody, CardHeader } from "@/components/ui/card";
import { Avatar, PageHeader, ScorePill } from "@/components/ui/misc";
import { cn } from "@/lib/cn";
import { formatAgo, formatDate, formatDateTime, formatNumber, formatPercent, formatRelative } from "@/lib/format";
import { CAMPAIGN_STATUS, SETTER_MODES, SIGNALS, SOURCES, STAGE_LABELS, type SemanticTone } from "@/lib/labels";
import { toneClasses } from "@/lib/tones";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { FIRST_MESSAGE_DELAY_HOURS, parseFollowUps, sequenceEndDay } from "@/server/domain/followups";
import { rates } from "@/server/domain/rates";
import { isRealAccount } from "@/server/engine/pace";
import {
  editHref,
  effectiveSettings,
  followUpSummary,
  launchReadiness,
  nextActions,
  personalizationLabel,
  type CheckLevel,
  type EditSection,
  type EffectiveSetting,
  type LaunchReadiness,
  type NextActions,
  withPeriod,
} from "@/server/services/campaign-insights";
import { funnelFromStages, getCampaign, stageCounts, type StageCounts } from "@/server/services/campaigns";
import { CampaignControls } from "./campaign-controls";
import { ImportForm } from "./import-form";
import { ImportPanel, ImportToggle } from "./import-panel";

export const metadata: Metadata = { title: "Campagne" };

type CampaignWithAccount = Campaign & { account: LinkedInAccount };

export default async function CampaignPage({ params }: { params: Promise<{ id: string }> }) {
  const { workspace } = await requireContext();
  const { id } = await params;
  const campaign = await getCampaign(workspace.id, id);
  if (!campaign) notFound();

  const now = new Date();
  const draft = campaign.status === "DRAFT";
  const [readiness, counts, recent, upcoming] = await Promise.all([
    // Launching and resuming share the checklist; a draft shows it in full.
    campaign.status === "ACTIVE" ? null : launchReadiness(campaign, workspace, now),
    draft ? null : stageCounts({ campaignId: campaign.id }),
    draft ? [] : db.prospect.findMany({ where: { campaignId: campaign.id }, orderBy: { stageChangedAt: "desc" }, take: 10 }),
    campaign.status === "ACTIVE" ? nextActions(campaign, now) : null,
  ]);
  // What stops 'Reprendre' (a disconnected account has its own banner).
  const blockers = (readiness?.checks ?? []).filter((c) => c.level === "blocker" && !(c.key === "account" && campaign.account.status === "DISCONNECTED"));

  return (
    <>
      <PageHeader
        title={
          <span className="flex min-w-0 flex-wrap items-center gap-x-3 gap-y-1">
            <span className="min-w-0 break-words">{campaign.name}</span> <LabeledBadge map={CAMPAIGN_STATUS} value={campaign.status} />
          </span>
        }
        description={`${campaign.account.fullName} · ${campaign.launchedAt ? `lancée le ${formatDate(campaign.launchedAt)}` : "jamais lancée"}`}
        actions={
          <>
            <ImportToggle />
            <ButtonLink href={`/campaigns/${campaign.id}/edit`} variant="secondary">
              <Pencil className="size-4" aria-hidden /> Modifier
            </ButtonLink>
            <CampaignControls campaignId={campaign.id} status={campaign.status} launchBlocked={readiness?.blocked ?? false} />
          </>
        }
      />

      <div className="space-y-6">
        <ImportPanel>
          <ImportForm campaignId={campaign.id} />
        </ImportPanel>

        {campaign.account.status === "DISCONNECTED" ? (
          <Banner tone="warning" action={{ href: editHref(campaign.id, "general"), label: "Choisir un autre compte" }}>
            Le compte LinkedIn de cette campagne ({campaign.account.fullName}) est déconnecté : elle ne peut plus rien envoyer.
          </Banner>
        ) : null}

        {!draft && campaign.status !== "ACTIVE" && blockers.length > 0 ? (
          <Banner tone="danger">
            Pour reprendre cette campagne : {blockers.map((b) => b.detail).join(" ")}{" "}
            {blockers[0]?.fix ? (
              <Link href={blockers[0].fix.href} className="font-semibold underline underline-offset-2 hover:no-underline">
                {blockers[0].fix.label}
              </Link>
            ) : null}
          </Banner>
        ) : null}

        {upcoming ? <NextActionsCard campaignId={campaign.id} actions={upcoming} now={now} /> : null}

        <div className="grid grid-cols-1 items-start gap-6 xl:grid-cols-3">
          <div className="min-w-0 space-y-6 xl:col-span-2">
            {draft && readiness ? (
              <ReadinessCard readiness={readiness} />
            ) : (
              <>
                <FunnelCard campaignId={campaign.id} counts={counts ?? {}} />
                <RecentCard recent={recent} />
              </>
            )}
          </div>
          <SettingsCard campaign={campaign} workspace={workspace} />
        </div>
      </div>
    </>
  );
}

// ---------------------------------------------------------------------------
// Banners and status lines
// ---------------------------------------------------------------------------

function Banner({ tone, action, children }: { tone: "warning" | "danger"; action?: { href: string; label: string }; children: ReactNode }) {
  return (
    <div className={cn("flex flex-wrap items-start gap-x-2 gap-y-1 rounded-card border px-4 py-3 text-sm", toneClasses(tone).soft, tone === "warning" ? "border-warning-line" : "border-danger-line")}>
      <TriangleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
      <p className="min-w-0 flex-1 basis-56 break-words">{children}</p>
      {action ? (
        <Link href={action.href} className="ml-6 shrink-0 font-semibold underline underline-offset-2 hover:no-underline sm:ml-0">
          {action.label}
        </Link>
      ) : null}
    </div>
  );
}

const LEVELS: Record<CheckLevel, { icon: LucideIcon; tone: SemanticTone; label: string }> = {
  ok: { icon: CircleCheck, tone: "success", label: "OK" },
  info: { icon: Info, tone: "info", label: "Conseil" },
  warn: { icon: TriangleAlert, tone: "warning", label: "Attention" },
  blocker: { icon: CircleX, tone: "danger", label: "Bloquant" },
};

// ---------------------------------------------------------------------------
// Draft: launch checklist
// ---------------------------------------------------------------------------

function ReadinessCard({ readiness }: { readiness: LaunchReadiness }) {
  const blockers = readiness.checks.filter((c) => c.level === "blocker").length;
  return (
    <Card aria-labelledby="readiness-title">
      <CardHeader
        title={<span id="readiness-title">Prêt à lancer ?</span>}
        description={
          blockers > 0
            ? `${blockers} point${blockers > 1 ? "s" : ""} à corriger avant de lancer la campagne.`
            : "Tout est prêt : lancez la campagne quand vous voulez."
        }
      />
      <ul className="divide-y divide-line">
        {readiness.checks.map((check) => {
          const level = LEVELS[check.level];
          const Icon = level.icon;
          return (
            <li key={check.key} className="flex flex-wrap items-start gap-x-3 gap-y-2 px-5 py-3">
              <Icon className={cn("mt-0.5 size-5 shrink-0", toneClasses(level.tone).text)} aria-hidden />
              <div className="min-w-0 flex-1 basis-48">
                <p className="text-sm font-medium text-ink">
                  <span className="sr-only">{level.label} : </span>
                  {check.label}
                </p>
                <p className="mt-0.5 text-sm break-words text-muted">{check.detail}</p>
              </div>
              {check.fix ? (
                <ButtonLink href={check.fix.href} variant={check.level === "blocker" ? "secondary" : "ghost"} size="sm" className="ml-8 sm:ml-0">
                  {check.fix.label}
                </ButtonLink>
              ) : null}
            </li>
          );
        })}
      </ul>
      <div className="rounded-b-card border-t border-line bg-surface-2 px-5 py-4">
        <h3 className="text-sm font-semibold text-ink">Ce qui va se passer</h3>
        <p className="mt-1 text-sm text-ink-2">{readiness.plan.join(" ")}</p>
      </div>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Active: what the engine does next
// ---------------------------------------------------------------------------

function NextActionsCard({ campaignId, actions, now }: { campaignId: string; actions: NextActions; now: Date }) {
  const prospects = (stage: string) => `/prospects?campaignId=${campaignId}&stage=${stage}`;
  const items = [
    { value: actions.toInvite, one: "qualifié à inviter", many: "qualifiés à inviter", href: prospects("QUALIFIED") },
    { value: actions.pendingInvites, one: "invitation en attente", many: "invitations en attente", href: prospects("INVITED") },
    { value: actions.firstMessages, one: "premier message prévu", many: "premiers messages prévus", href: prospects("CONNECTED") },
    { value: actions.followUpsSoon, one: "relance dans les 24 h", many: "relances dans les 24 h", href: prospects("MESSAGED") },
  ];
  const { account } = actions;
  return (
    <Card aria-labelledby="next-title">
      <div className="px-5 pt-4">
        <h2 id="next-title" className="text-title font-semibold text-ink">
          Prochaines actions
        </h2>
      </div>
      <ul className="grid grid-cols-2 gap-3 px-5 py-3 md:grid-cols-4">
        {items.map((item) => (
          <li key={item.one} className="min-w-0">
            <Link href={item.href} className="block rounded-control px-2 py-1.5 -mx-2 hover:bg-surface-2 focus-visible:outline-2 focus-visible:outline-brand-600">
              <span className="block text-title font-semibold text-ink tabular-nums">{formatNumber(item.value)}</span>
              <span className="block text-xs text-muted">{item.value >= 2 ? item.many : item.one}</span>
            </Link>
          </li>
        ))}
      </ul>
      <div className="space-y-1.5 border-t border-line px-5 py-3 text-sm">
        <p className="flex items-start gap-2 text-ink-2">
          <Clock className="mt-0.5 size-4 shrink-0 text-muted" aria-hidden />
          <span className="min-w-0">
            Envois {actions.window.label}
            {actions.window.open ? null : <span className="text-warning"> · actuellement hors horaires</span>}
          </span>
        </p>
        {/* A disconnected account has its own banner above. */}
        {account.status === "PAUSED" ? (
          <StatusLine tone="danger" href={`/accounts#${account.id}`} link="Réparer">
            {withPeriod(`${account.fullName} est en pause${account.statusReason ? ` : ${account.statusReason}` : ""}`)} Rien
            n&apos;est envoyé.
          </StatusLine>
        ) : null}
        {actions.invitesPausedUntil ? (
          <StatusLine tone="warning">
            LinkedIn a signalé la limite d&apos;invitations : reprise le {formatDateTime(actions.invitesPausedUntil)}.
          </StatusLine>
        ) : null}
        {account.status === "ACTIVE" && account.lastError ? (
          <StatusLine tone="danger" href={`/accounts#${account.id}`} link="Voir le compte">
            Dernière synchronisation en échec{account.lastErrorAt ? ` (${formatAgo(account.lastErrorAt, now)})` : ""} : {account.lastError}
          </StatusLine>
        ) : null}
      </div>
    </Card>
  );
}

function StatusLine({ tone, href, link, children }: { tone: "warning" | "danger"; href?: string; link?: string; children: ReactNode }) {
  return (
    <p className={cn("flex flex-wrap items-start gap-x-2 gap-y-1", toneClasses(tone).text)}>
      <TriangleAlert className="mt-0.5 size-4 shrink-0" aria-hidden />
      <span className="min-w-0 flex-1 basis-56 break-words">{children}</span>
      {href && link ? (
        <Link href={href} className="ml-6 shrink-0 font-semibold underline underline-offset-2 hover:no-underline sm:ml-0">
          {link}
        </Link>
      ) : null}
    </p>
  );
}

// ---------------------------------------------------------------------------
// Funnel and recent activity
// ---------------------------------------------------------------------------

function FunnelCard({ campaignId, counts }: { campaignId: string; counts: StageCounts }) {
  const funnel = funnelFromStages(counts);
  const r = rates(funnel);
  const tiles = [
    { label: "Acceptation", value: r.acceptance, hint: `${formatNumber(funnel.connected)} sur ${formatNumber(funnel.invited)} invités` },
    { label: "Réponse", value: r.reply, hint: `${formatNumber(funnel.replied)} sur ${formatNumber(funnel.messaged)} contactés` },
    { label: "Rendez-vous", value: r.meeting, hint: `${formatNumber(funnel.meetings)} sur ${formatNumber(funnel.replied)} réponses` },
  ];
  return (
    <Card aria-labelledby="funnel-title">
      <CardHeader
        title={<span id="funnel-title">Entonnoir de la campagne</span>}
        actions={
          <ButtonLink href={`/prospects?campaignId=${campaignId}`} variant="ghost" size="sm">
            Tous les prospects
          </ButtonLink>
        }
      />
      <dl className="grid grid-cols-3 divide-x divide-line border-b border-line">
        {tiles.map((t) => (
          <div key={t.label} className="min-w-0 px-3 py-3 sm:px-5">
            <dt className="truncate text-xs text-muted">{t.label}</dt>
            <dd className="mt-0.5 text-title font-semibold text-ink tabular-nums">{formatPercent(t.value)}</dd>
            <dd className="text-2xs text-muted">{t.hint}</dd>
          </div>
        ))}
      </dl>
      <CardBody>
        <FunnelChart
          steps={[
            { label: "Trouvés", value: funnel.found },
            { label: "Qualifiés", value: funnel.qualified },
            { label: "Invités", value: funnel.invited },
            { label: "En relation", value: funnel.connected },
            { label: "Ont répondu", value: funnel.replied },
            { label: "RDV réservés", value: funnel.meetings },
          ]}
        />
      </CardBody>
    </Card>
  );
}

type RecentProspect = { id: string; firstName: string; lastName: string; title: string; company: string; score: number | null; stage: string; stageChangedAt: Date };

function RecentCard({ recent }: { recent: RecentProspect[] }) {
  return (
    <Card aria-labelledby="recent-title">
      <CardHeader title={<span id="recent-title">Dernière activité</span>} />
      {recent.length === 0 ? (
        <CardBody>
          <p className="text-sm text-muted">Pas encore de prospect. Le moteur en ajoute à son prochain passage, ou importez une liste.</p>
        </CardBody>
      ) : (
        <ul className="divide-y divide-line">
          {recent.map((p) => (
            <li key={p.id}>
              <Link
                href={`/prospects/${p.id}`}
                className="flex items-center gap-3 px-5 py-3 hover:bg-surface-2 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-brand-600"
              >
                <Avatar first={p.firstName} last={p.lastName} size="sm" />
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-medium text-ink">
                    {p.firstName} {p.lastName}
                  </span>
                  <span className="block truncate text-xs text-muted">{[p.title, p.company].filter(Boolean).join(" · ") || "Profil à compléter"}</span>
                </span>
                <ScorePill score={p.score} />
                {/* Fixed width from sm, so stages line up from row to row. */}
                <span className="flex shrink-0 sm:w-32">
                  <LabeledBadge map={STAGE_LABELS} value={p.stage} />
                </span>
                <span className="hidden w-24 shrink-0 text-right text-xs text-muted sm:block">{formatRelative(p.stageChangedAt)}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Settings summary
// ---------------------------------------------------------------------------

function SettingsCard({ campaign, workspace }: { campaign: CampaignWithAccount; workspace: { bookingUrl: string; offer: string } }) {
  const followUps = parseFollowUps(campaign.followUps);
  const effective = effectiveSettings(campaign, workspace);
  const realAccount = isRealAccount(campaign.account);
  const id = campaign.id;

  return (
    <Card aria-labelledby="settings-title">
      <CardHeader title={<span id="settings-title">Réglages</span>} />
      <div className="divide-y divide-line">
        <SettingGroup title="Ciblage" campaignId={id} section="ciblage">
          <Setting label="Sources">
            {campaign.sources.length === 0 ? (
              <span className="text-muted">Aucune (import uniquement)</span>
            ) : (
              <span className="flex flex-wrap gap-x-2 gap-y-1">
                {campaign.sources.map((s, i) => {
                  const label = SOURCES[s]?.label ?? s;
                  const last = i === campaign.sources.length - 1;
                  return s === "SIGNALS" && realAccount ? (
                    <span key={s}>
                      <s className="text-muted">{label}</s> <span className="text-xs text-muted">(sans effet sur un vrai compte)</span>
                      {last ? "" : ","}
                    </span>
                  ) : (
                    <span key={s}>
                      {label}
                      {last ? "" : ","}
                    </span>
                  );
                })}
              </span>
            )}
          </Setting>
          {campaign.sources.includes("SIGNALS") ? <Setting label="Signaux">{campaign.signals.map((s) => SIGNALS[s] ?? s).join(", ") || "Tous"}</Setting> : null}
          {campaign.searchUrl ? (
            <Setting label="URL de recherche">
              <a href={campaign.searchUrl} target="_blank" rel="noreferrer" className="block truncate text-brand-700 underline underline-offset-2 hover:no-underline">
                {campaign.searchUrl.replace(/^https:\/\/(www\.)?/, "")}
              </a>
            </Setting>
          ) : null}
          <Setting label="Postes"><Tags values={campaign.titles} empty="Tous" /></Setting>
          {campaign.keywords.length ? <Setting label="Mots-clés"><Tags values={campaign.keywords} empty="Aucun" /></Setting> : null}
          <Setting label="Secteurs"><Tags values={campaign.industries} empty="Tous" /></Setting>
          <Setting label="Zones"><Tags values={campaign.locations} empty="Toutes" /></Setting>
          <Setting label="Exclusions"><Tags values={campaign.exclusions} empty="Aucune" /></Setting>
          <Setting label="Note minimum">{campaign.minScore}/100</Setting>
          <Setting label="Rythme">{formatNumber(campaign.weeklyProspectTarget)} nouveaux prospects par semaine</Setting>
        </SettingGroup>

        <SettingGroup title="Offre" campaignId={id} section="offre">
          <Setting label="Offre (1re phrase)">
            <Effective setting={effective.offer} empty="Non renseignée" />
          </Setting>
        </SettingGroup>

        <SettingGroup title="Séquence" campaignId={id} section="sequence">
          <Setting label="Invitation">{campaign.inviteNote ? "Avec une note" : "Sans note"}</Setting>
          <Setting label="Premier message">{FIRST_MESSAGE_DELAY_HOURS} h après l&apos;acceptation</Setting>
          <Setting label="Relances">
            {followUpSummary(followUps)}
            {followUps.length ? <span className="block text-xs text-muted">Arrêt dès la première réponse ; sans réponse, fin à J+{sequenceEndDay(followUps)}.</span> : null}
          </Setting>
          <Setting label="Personnalisation">{personalizationLabel(campaign.aiPersonalization)}</Setting>
        </SettingGroup>

        <SettingGroup title="Setter" campaignId={id} section="setter">
          <Setting label="Mode">{SETTER_MODES[campaign.setterMode]?.label ?? campaign.setterMode}</Setting>
          <Setting label="Lien de réservation">
            <Effective setting={effective.bookingUrl} empty={campaign.setterMode === "OFF" ? "Aucun" : "Aucun : à renseigner"} link />
          </Setting>
        </SettingGroup>
      </div>
    </Card>
  );
}

const SECTION_NAMES: Record<EditSection, string> = {
  general: "les informations générales",
  ciblage: "le ciblage",
  offre: "l'offre",
  sequence: "la séquence",
  setter: "le setter",
};

function SettingGroup({ title, campaignId, section, children }: { title: string; campaignId: string; section: EditSection; children: ReactNode }) {
  return (
    <section className="px-5 py-4" aria-label={title}>
      <div className="mb-2 flex items-center justify-between gap-2">
        <h3 className="text-xs font-semibold uppercase tracking-wide text-ink-2">{title}</h3>
        <Link
          href={editHref(campaignId, section)}
          className="-my-1 rounded-control px-2 py-1 text-xs font-medium text-brand-700 hover:bg-brand-50 focus-visible:outline-2 focus-visible:outline-brand-600 pointer-coarse:py-2.5"
        >
          Modifier<span className="sr-only"> {SECTION_NAMES[section]}</span>
        </Link>
      </div>
      <dl className="space-y-2.5 text-sm">{children}</dl>
    </section>
  );
}

function Setting({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div className="grid grid-cols-[minmax(0,7.5rem)_minmax(0,1fr)] gap-x-3">
      <dt className="text-muted">{label}</dt>
      <dd className="min-w-0 break-words text-ink">{children}</dd>
    </div>
  );
}

function Effective({ setting, empty, link = false }: { setting: EffectiveSetting; empty: string; link?: boolean }) {
  if (setting.origin === "none") {
    return (
      <span className="text-muted">
        {empty}{" "}
        <Link href="/settings" className="text-brand-700 underline underline-offset-2 hover:no-underline">
          (Réglages)
        </Link>
      </span>
    );
  }
  return (
    <span>
      {link ? (
        <a href={setting.value} target="_blank" rel="noreferrer" className="wrap-anywhere text-brand-700 underline underline-offset-2 hover:no-underline">
          {setting.value.replace(/^https?:\/\/(www\.)?/, "")}
        </a>
      ) : (
        setting.value
      )}{" "}
      <span className="text-xs whitespace-nowrap text-muted">{setting.origin === "workspace" ? "(Réglages)" : "(propre à la campagne)"}</span>
    </span>
  );
}

function Tags({ values, empty }: { values: string[]; empty: string }) {
  if (values.length === 0) return <span className="text-muted">{empty}</span>;
  return (
    <span className="flex flex-wrap gap-1">
      {values.map((v) => (
        <Badge key={v} className="max-w-full">
          <span className="truncate">{v}</span>
        </Badge>
      ))}
    </span>
  );
}
