import type { Campaign, LinkedInAccount, Prisma, ProspectSource, Workspace } from "@prisma/client";
import { WEEK } from "@/server/domain/time";
import type { ProviderProfile } from "@/server/linkedin/types";
import { logActivity } from "./activity";
import type { EngineDeps } from "./deps";

/** Prospects pulled per campaign per tick. */
export const SOURCING_BATCH = 25;
/** Stop sourcing while this many qualified prospects already wait for an invitation. */
export const QUALIFIED_BACKLOG = 80;

type SourcingState = Partial<Record<ProspectSource, string | null | "done">>;

const AUTOMATIC_SOURCES: ProspectSource[] = ["SEARCH", "SIGNALS", "POST_ENGAGERS", "PROFILE_VISITORS"];

type CampaignWithContext = Campaign & { account: LinkedInAccount; workspace: Workspace };

export async function sourceProspects(deps: EngineDeps, campaign: CampaignWithContext): Promise<number> {
  const { db, now } = deps;
  const weeklyCap = campaign.weeklyProspectTarget;
  const foundThisWeek = await db.activity.count({
    where: { campaignId: campaign.id, type: "PROSPECT_FOUND", createdAt: { gt: new Date(now.getTime() - WEEK) } },
  });
  const backlog = await db.prospect.count({ where: { campaignId: campaign.id, stage: { in: ["NEW", "QUALIFIED"] } } });
  const budget = Math.min(SOURCING_BATCH, weeklyCap - foundThisWeek);
  if (budget <= 0 || backlog >= QUALIFIED_BACKLOG) return 0;

  const state = (campaign.sourcingState ?? {}) as SourcingState;
  const sources = campaign.sources.filter(
    (s) => AUTOMATIC_SOURCES.includes(s) && state[s] !== "done" && (s !== "POST_ENGAGERS" || campaign.postUrls.length > 0),
  );
  if (sources.length === 0) return 0;

  // Round-robin: draw from the source that has contributed the fewest prospects so far.
  const counts = await db.prospect.groupBy({ by: ["source"], where: { campaignId: campaign.id }, _count: true });
  const countOf = (s: ProspectSource) => counts.find((c) => c.source === s)?._count ?? 0;
  const source = [...sources].sort((a, b) => countOf(a) - countOf(b))[0]!;

  const provider = deps.providerFor(campaign.account.provider);
  const cursor = state[source] ?? null;
  const page = await provider.search(
    { externalId: campaign.account.externalId },
    {
      source,
      searchUrl: campaign.searchUrl || undefined,
      titles: campaign.titles,
      keywords: campaign.keywords,
      industries: campaign.industries,
      locations: campaign.locations,
      companySizes: campaign.companySizes,
      signals: campaign.signals,
      postUrls: campaign.postUrls,
    },
    cursor === "done" ? null : cursor,
    budget,
  );

  const created = await insertProspects(deps, campaign, page.profiles, source);
  await db.campaign.update({
    where: { id: campaign.id },
    data: { sourcingState: { ...state, [source]: page.nextCursor ?? "done" } as Prisma.InputJsonValue },
  });
  return created;
}

/** Inserts new people, skipping anyone the workspace already knows (in any campaign). */
export async function insertProspects(
  deps: EngineDeps,
  campaign: Pick<Campaign, "id" | "workspaceId" | "accountId">,
  profiles: ProviderProfile[],
  source: ProspectSource,
): Promise<number> {
  if (profiles.length === 0) return 0;
  const rows = await deps.db.prospect.createManyAndReturn({
    data: profiles.map((p) => ({
      workspaceId: campaign.workspaceId,
      campaignId: campaign.id,
      accountId: campaign.accountId,
      externalId: p.externalId,
      profileUrl: p.profileUrl,
      firstName: p.firstName,
      lastName: p.lastName,
      headline: p.headline,
      title: p.title,
      company: p.company,
      companySize: p.companySize,
      industry: p.industry,
      location: p.location,
      source,
      signal: p.signal,
      signalDetail: p.signalDetail,
      stage: "NEW" as const,
      stageChangedAt: deps.now,
      createdAt: deps.now,
    })),
    skipDuplicates: true,
    select: { id: true, signal: true },
  });
  for (const row of rows) {
    await logActivity(deps.db, {
      workspaceId: campaign.workspaceId, campaignId: campaign.id, prospectId: row.id,
      accountId: campaign.accountId, type: "PROSPECT_FOUND", data: { source, signal: row.signal }, at: deps.now,
    });
  }
  return rows.length;
}

/** Scores NEW prospects. Imported prospects skip the minimum score (someone chose them) but not exclusions. */
export async function scoreNewProspects(deps: EngineDeps, campaign: Campaign & { workspace?: Workspace }, limit = 100): Promise<number> {
  const prospects = await deps.db.prospect.findMany({
    where: { campaignId: campaign.id, stage: "NEW" },
    orderBy: { createdAt: "asc" },
    take: limit,
  });
  const workspace = campaign.workspace ?? (await deps.db.workspace.findUniqueOrThrow({ where: { id: campaign.workspaceId } }));
  const context = { offer: campaign.offer || workspace.offer, persona: campaign.persona || workspace.persona };
  const results = await deps.agents.scorer.scoreBatch(prospects.map((prospect) => ({ id: prospect.id, prospect, targeting: campaign, context })));
  for (const [i, prospect] of prospects.entries()) {
    const result = results[i]!;
    const qualified = result.excludedBy === null && (prospect.source === "IMPORT" || result.score >= campaign.minScore);
    await deps.db.prospect.update({
      where: { id: prospect.id },
      data: {
        score: result.score,
        scoreReasons: result.reasons,
        scoreSummary: result.summary ?? null,
        scoredBy: result.scoredBy,
        stage: qualified ? "QUALIFIED" : "DISQUALIFIED",
        stageChangedAt: deps.now,
        disqualifiedReason: qualified
          ? null
          : result.excludedBy
            ? `Exclusion : ${result.excludedBy}`
            : `Score ${result.score} sous le minimum de ${campaign.minScore}`,
      },
    });
    await logActivity(deps.db, {
      workspaceId: prospect.workspaceId, campaignId: campaign.id, prospectId: prospect.id, accountId: prospect.accountId,
      type: qualified ? "PROSPECT_QUALIFIED" : "PROSPECT_DISQUALIFIED", data: { score: result.score, by: result.scoredBy }, at: deps.now,
    });
  }
  return prospects.length;
}
