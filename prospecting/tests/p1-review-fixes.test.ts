import type { ProspectSource, ProspectStage } from "@prisma/client";
import { beforeEach, describe, expect, it } from "vitest";
import { DAY, MINUTE } from "@/server/domain/time";
import { SESSION_TO_OPEN_REASON } from "@/server/services/accounts";
import { attentionItems, reasonOutsideAccounts } from "@/server/services/attention";
import { onboardingStatus } from "@/server/services/workspace";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

beforeEach(resetDb);

const NOW = new Date("2026-10-16T10:00:00Z");
const ago = (days: number) => new Date(NOW.getTime() - days * DAY);
let seq = 0;

async function prospect(
  workspaceId: string,
  campaignId: string,
  accountId: string,
  data: { stage?: ProspectStage; source?: ProspectSource; createdAt?: Date; invitedAt?: Date } = {},
) {
  seq += 1;
  return db.prospect.create({
    data: {
      workspaceId, campaignId, accountId, externalId: `r-${seq}`, profileUrl: `https://www.linkedin.com/in/r-${seq}`,
      firstName: "Léa", lastName: `Durand ${seq}`, source: "SEARCH", ...data,
    },
  });
}

/** A workspace whose engine synced a minute ago, so the engine row stays out of the way. */
async function freshWorkspace() {
  const { workspace, account } = await createWorkspace();
  await db.linkedInAccount.update({ where: { id: account.id }, data: { lastSyncedAt: new Date(NOW.getTime() - MINUTE) } });
  return { workspace, account };
}

describe("first run is decided on lifetime facts", () => {
  it("is a first run only while nothing was ever launched and no prospect exists", async () => {
    const { workspace, account } = await createWorkspace();
    expect(await onboardingStatus(workspace.id)).toMatchObject({ everLaunched: false, hasProspects: false });

    await createCampaign(workspace.id, account.id, { status: "DRAFT" });
    expect(await onboardingStatus(workspace.id)).toMatchObject({ everLaunched: false, hasProspects: false });
  });

  it("is not a first run once every campaign is paused and the prospects are older than the period", async () => {
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id, { status: "PAUSED", launchedAt: ago(45) });
    await prospect(workspace.id, campaign.id, account.id, { stage: "INVITED", createdAt: ago(40), invitedAt: ago(39) });

    const status = await onboardingStatus(workspace.id);
    // The launch step goes back to "to do", but the dashboard keeps its full view.
    expect(status).toMatchObject({ campaignLaunched: false, everLaunched: true, hasProspects: true, draftCampaignId: campaign.id });
  });

  it("remembers a launch whose campaign was archived since", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id, { status: "ARCHIVED", launchedAt: ago(60) });
    expect(await onboardingStatus(workspace.id)).toMatchObject({ campaignCreated: false, everLaunched: true, hasProspects: false });
  });

  it("counts an imported list on a draft as history", async () => {
    const { workspace, account } = await createWorkspace();
    const draft = await createCampaign(workspace.id, account.id, { status: "DRAFT", sources: [] });
    await prospect(workspace.id, draft.id, account.id, { source: "IMPORT", stage: "NEW" });
    expect(await onboardingStatus(workspace.id)).toMatchObject({ everLaunched: false, hasProspects: true });
  });
});

describe("attentionItems review fixes", () => {
  it("asks for a new list, not wider targeting, when a campaign without automatic source has contacted its imports", async () => {
    const { workspace, account } = await freshWorkspace();
    const imported = await createCampaign(workspace.id, account.id, { name: "Import salon", sources: [] });
    await prospect(workspace.id, imported.id, account.id, { source: "IMPORT", stage: "INVITED", invitedAt: ago(1) });
    // Engagers without any post: nothing to page through, and nothing imported yet.
    const noPosts = await createCampaign(workspace.id, account.id, { name: "Posts", sources: ["POST_ENGAGERS"], postUrls: [] });
    // Still has an imported prospect to invite: nothing to say.
    const waiting = await createCampaign(workspace.id, account.id, { sources: [] });
    await prospect(workspace.id, waiting.id, account.id, { source: "IMPORT", stage: "QUALIFIED" });

    const items = await attentionItems(workspace.id, NOW);
    expect(items).toEqual([
      {
        kind: "campaign_exhausted", severity: "medium", count: 1, href: `/campaigns/${imported.id}#import`,
        label: "Campagne Import salon : tous les prospects importés ont été contactés, importez une nouvelle liste",
      },
      {
        kind: "campaign_exhausted", severity: "medium", count: 1, href: `/campaigns/${noPosts.id}#import`,
        label: "Campagne Posts : aucun prospect à contacter, importez une liste",
      },
    ]);
  });

  it("links a disconnected account to the campaign that depends on it, where another account can be chosen", async () => {
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id, { status: "PAUSED" });
    await createCampaign(workspace.id, account.id, { status: "ARCHIVED" });
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "DISCONNECTED", statusReason: "Compte retiré." } });

    let items = await attentionItems(workspace.id, NOW);
    expect(items).toEqual([
      {
        kind: "account_disconnected", severity: "medium", count: 1, href: `/campaigns/${campaign.id}`, label: "Alex Martin est déconnecté",
        detail: "Compte retiré. 1 campagne en dépend : choisissez un autre compte ou archivez-la.",
      },
    ]);

    // Several campaigns: the list, since /accounts no longer shows a disconnected account.
    await createCampaign(workspace.id, account.id, { status: "DRAFT" });
    items = await attentionItems(workspace.id, NOW);
    expect(items[0]).toMatchObject({
      href: "/campaigns", detail: "Compte retiré. 2 campagnes en dépendent : choisissez un autre compte ou archivez-les.",
    });
  });

  it("drops a never-opened session from a disconnected account's row", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id, { status: "PAUSED" });
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "DISCONNECTED", statusReason: SESSION_TO_OPEN_REASON } });
    const [item] = await attentionItems(workspace.id, NOW);
    expect(item?.detail).toBe("1 campagne en dépend : choisissez un autre compte ou archivez-la.");
  });

  it("agrees the meetings detail with their number", async () => {
    const { workspace, account } = await freshWorkspace();
    const campaign = await createCampaign(workspace.id, account.id, { sourcingState: { SEARCH: "abc", SIGNALS: "abc" } });
    const p = await prospect(workspace.id, campaign.id, account.id, { stage: "MEETING_BOOKED" });
    await db.meeting.create({ data: { workspaceId: workspace.id, prospectId: p.id, campaignId: campaign.id, startsAt: ago(1) } });
    expect((await attentionItems(workspace.id, NOW))[0]).toMatchObject({ label: "1 rendez-vous à confirmer", detail: "Indiquez s'il a eu lieu." });

    await db.meeting.create({ data: { workspaceId: workspace.id, prospectId: p.id, campaignId: campaign.id, startsAt: ago(2) } });
    expect((await attentionItems(workspace.id, NOW))[0]).toMatchObject({ label: "2 rendez-vous à confirmer", detail: "Indiquez s'ils ont eu lieu." });
  });

  it("words a session to open for the dashboard, in the attention row and the onboarding step", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: account.id }, data: { provider: "browser", status: "PAUSED", statusReason: SESSION_TO_OPEN_REASON } });
    const expected = "Session LinkedIn à ouvrir : connectez-la depuis la fiche du compte.";

    const [item] = await attentionItems(workspace.id, NOW);
    expect(item).toMatchObject({ kind: "account_paused", href: `/accounts#${account.id}`, detail: expected });
    expect((await onboardingStatus(workspace.id)).accountIssue).toEqual({ accountId: account.id, reason: expected });
  });

  it("keeps any other reason as it is", () => {
    const expired = "Session LinkedIn expirée ou vérification de sécurité demandée : mettez à jour le cookie du compte.";
    expect(reasonOutsideAccounts(expired)).toBe(expired);
    expect(reasonOutsideAccounts(SESSION_TO_OPEN_REASON)).not.toContain("ci-dessous");
    expect(reasonOutsideAccounts(SESSION_TO_OPEN_REASON)).not.toContain("npm");
  });
});
