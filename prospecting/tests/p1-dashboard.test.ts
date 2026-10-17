import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import type { ProspectStage } from "@prisma/client";
import { beforeEach, describe, expect, it } from "vitest";
import { POST } from "@/app/api/mcp/route";
import { DAY, HOUR, MINUTE } from "@/server/domain/time";
import { byWeek, dashboard } from "@/server/services/analytics";
import { attentionItems } from "@/server/services/attention";
import { createToken } from "@/server/services/tokens";
import { onboardingStatus } from "@/server/services/workspace";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

beforeEach(resetDb);

const NOW = new Date("2026-10-16T10:00:00Z");
let seq = 0;

async function prospect(workspaceId: string, campaignId: string, accountId: string, data: { stage?: ProspectStage; createdAt?: Date; invitedAt?: Date; connectedAt?: Date } = {}) {
  seq += 1;
  return db.prospect.create({
    data: {
      workspaceId, campaignId, accountId, externalId: `p-${seq}`, profileUrl: `https://www.linkedin.com/in/p-${seq}`,
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

describe("attentionItems", () => {
  it("is empty for a quiet workspace", async () => {
    const { workspace } = await freshWorkspace();
    expect(await attentionItems(workspace.id, NOW)).toEqual([]);
  });

  it("lists meetings to confirm and the inbox, with the setter drafts right under the inbox total", async () => {
    const { workspace, account } = await freshWorkspace();
    const campaign = await createCampaign(workspace.id, account.id, { sourcingState: { SEARCH: "abc" } });
    const a = await prospect(workspace.id, campaign.id, account.id, { stage: "REPLIED" });
    const b = await prospect(workspace.id, campaign.id, account.id, { stage: "REPLIED" });
    const c = await prospect(workspace.id, campaign.id, account.id, { stage: "MEETING_BOOKED" });
    await db.conversation.create({
      data: { workspaceId: workspace.id, prospectId: a.id, accountId: account.id, status: "NEEDS_HUMAN", messages: { create: { direction: "INBOUND", author: "PROSPECT", body: "Combien ?" } } },
    });
    await db.conversation.create({
      data: {
        workspaceId: workspace.id, prospectId: b.id, accountId: account.id, status: "AI_ACTIVE",
        messages: { create: { direction: "INBOUND", author: "PROSPECT", body: "Oui, pourquoi pas" } },
        drafts: { create: { body: "Voici mon agenda", intent: "INTERESTED", rationale: "Intéressé" } },
      },
    });
    await db.meeting.create({ data: { workspaceId: workspace.id, prospectId: c.id, campaignId: campaign.id, startsAt: new Date(NOW.getTime() - 2 * DAY) } });
    await db.meeting.create({ data: { workspaceId: workspace.id, prospectId: c.id, campaignId: campaign.id, startsAt: new Date(NOW.getTime() + 2 * DAY) } });

    const items = await attentionItems(workspace.id, NOW);
    expect(items.map((i) => i.kind)).toEqual(["inbox_todo", "drafts", "meetings_to_confirm"]);
    expect(items[0]).toMatchObject({ severity: "medium", count: 2, href: "/inbox?tab=todo", label: "Conversations à traiter au total" });
    expect(items[1]).toMatchObject({ count: 1, href: "/inbox?tab=drafts", label: "dont réponses du setter à valider" });
    expect(items[2]).toMatchObject({ severity: "low", count: 1, href: "/meetings", label: "1 rendez-vous à confirmer" });
  });

  it("puts a paused account at the top, high severity, linked to its card", async () => {
    const { workspace, account } = await freshWorkspace();
    const campaign = await createCampaign(workspace.id, account.id);
    await db.meeting.create({
      data: { workspaceId: workspace.id, prospectId: (await prospect(workspace.id, campaign.id, account.id)).id, campaignId: campaign.id, startsAt: new Date(NOW.getTime() - DAY) },
    });
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "PAUSED", statusReason: "Session LinkedIn expirée" } });

    const items = await attentionItems(workspace.id, NOW);
    expect(items[0]).toMatchObject({ kind: "account_paused", severity: "high", href: `/accounts#${account.id}`, detail: "Session LinkedIn expirée" });
    // No active account: the engine row would only repeat the pause.
    expect(items.some((i) => i.kind === "engine_down")).toBe(false);
  });

  it("reports recent sync errors and a stopped engine, but not stale errors", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({
      where: { id: account.id },
      data: { lastSyncedAt: new Date(NOW.getTime() - 3 * HOUR), lastError: "Délai dépassé", lastErrorAt: new Date(NOW.getTime() - 3 * HOUR) },
    });
    const items = await attentionItems(workspace.id, NOW);
    expect(items.map((i) => [i.kind, i.severity])).toEqual([["account_error", "high"], ["engine_down", "high"]]);
    expect(items[0]!.detail).toContain("Délai dépassé");

    await db.linkedInAccount.update({ where: { id: account.id }, data: { lastSyncedAt: NOW, lastErrorAt: new Date(NOW.getTime() - 25 * HOUR) } });
    expect(await attentionItems(workspace.id, NOW)).toEqual([]);
  });

  it("groups the last 24 h of failed LinkedIn actions by code, machine problems first", async () => {
    const { workspace, account } = await freshWorkspace();
    const campaign = await createCampaign(workspace.id, account.id);
    const [p1, p2] = [await prospect(workspace.id, campaign.id, account.id), await prospect(workspace.id, campaign.id, account.id)];
    const fail = (prospectId: string, code: string, hoursAgo: number) =>
      db.activity.create({
        data: {
          workspaceId: workspace.id, campaignId: campaign.id, prospectId, accountId: account.id, type: "ACTION_FAILED",
          data: { action: "invite", code, message: code }, createdAt: new Date(NOW.getTime() - hoursAgo * HOUR),
        },
      });
    await fail(p1.id, "PROFILE_NOT_FOUND", 1);
    await fail(p2.id, "PROFILE_NOT_FOUND", 2);
    await fail(p1.id, "WORKER_UNAVAILABLE", 3);
    await fail(p2.id, "UNEXPECTED_PAGE", 30);

    const items = await attentionItems(workspace.id, NOW);
    expect(items).toHaveLength(2);
    expect(items[0]).toMatchObject({ kind: "action_failed", severity: "medium", count: 1, href: "/accounts" });
    expect(items[0]!.label).toContain("le navigateur de Vela ne répond pas");
    expect(items[1]).toMatchObject({ kind: "action_failed", severity: "low", count: 2, href: `/prospects?campaignId=${campaign.id}` });
    expect(items[1]!.label).toBe("2 actions LinkedIn impossibles en 24 h : profil introuvable");
  });

  it("flags an active campaign whose sources are exhausted and that has nobody left to invite", async () => {
    const { workspace, account } = await freshWorkspace();
    const exhausted = await createCampaign(workspace.id, account.id, { name: "DAF Lyon", sources: ["SEARCH", "POST_ENGAGERS"], sourcingState: { SEARCH: "done" } });
    const stillQueued = await createCampaign(workspace.id, account.id, { sources: ["SEARCH"], sourcingState: { SEARCH: "done" } });
    await prospect(workspace.id, stillQueued.id, account.id, { stage: "QUALIFIED" });
    await createCampaign(workspace.id, account.id, { sources: ["SEARCH", "SIGNALS"], sourcingState: { SEARCH: "done", SIGNALS: "cursor-2" } });
    await createCampaign(workspace.id, account.id, { status: "PAUSED", sources: ["SEARCH"], sourcingState: { SEARCH: "done" } });

    const items = await attentionItems(workspace.id, NOW);
    expect(items).toEqual([
      {
        kind: "campaign_exhausted", severity: "medium", count: 1, href: `/campaigns/${exhausted.id}`,
        label: "Campagne DAF Lyon : plus aucun prospect à inviter, élargissez le ciblage",
      },
    ]);
  });
});

describe("onboardingStatus", () => {
  it("does not count a paused account as ready and says why", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "PAUSED", statusReason: "Session LinkedIn à ouvrir" } });
    const status = await onboardingStatus(workspace.id);
    expect(status.accountReady).toBe(false);
    expect(status.accountIssue).toEqual({ accountId: account.id, reason: "Session LinkedIn à ouvrir : connectez-la depuis la fiche du compte." });
  });

  it("skips the connection check for the simulator and links the launch step to the draft", async () => {
    const { workspace, account } = await createWorkspace();
    const draft = await createCampaign(workspace.id, account.id, { status: "DRAFT" });
    let status = await onboardingStatus(workspace.id);
    expect(status).toMatchObject({
      accountReady: true, simulatorOnly: true, sessionVerified: true, offerDescribed: true,
      campaignCreated: true, campaignLaunched: false, draftCampaignId: draft.id,
    });
    await db.campaign.update({ where: { id: draft.id }, data: { status: "ACTIVE" } });
    status = await onboardingStatus(workspace.id);
    expect(status).toMatchObject({ campaignLaunched: true, draftCampaignId: null });
  });

  it("requires a passed connection check for a browser account", async () => {
    const { workspace } = await createWorkspace();
    await db.linkedInAccount.updateMany({ where: { workspaceId: workspace.id }, data: { provider: "browser" } });
    let status = await onboardingStatus(workspace.id);
    expect(status).toMatchObject({ simulatorOnly: false, sessionVerified: false, sessionIssue: null });

    await db.linkedInAccount.updateMany({ where: { workspaceId: workspace.id }, data: { lastDiagnosisOk: false, lastDiagnosedAt: NOW } });
    status = await onboardingStatus(workspace.id);
    expect(status.sessionVerified).toBe(false);
    expect(status.sessionIssue?.reason).toContain("vérification");

    await db.linkedInAccount.updateMany({ where: { workspaceId: workspace.id }, data: { lastDiagnosisOk: true } });
    expect((await onboardingStatus(workspace.id)).sessionVerified).toBe(true);
  });
});

describe("dashboard", () => {
  it("charts 90 days as about 13 weekly columns and shorter periods by day", async () => {
    const { workspace } = await createWorkspace();
    const ninety = await dashboard(workspace.id, 90, NOW);
    expect(ninety.granularity).toBe("week");
    expect(ninety.series).toHaveLength(13);
    const thirty = await dashboard(workspace.id, 30, NOW);
    expect(thirty.granularity).toBe("day");
    expect(thirty.series).toHaveLength(30);
  });

  it("sums days into 7-day columns ending today", () => {
    const days = Array.from({ length: 9 }, (_, i) => ({ day: `2026-10-${String(i + 1).padStart(2, "0")}`, invites: 1, messages: 0, replies: 0, meetings: i }));
    const weeks = byWeek(days);
    expect(weeks.map((w) => [w.day, w.invites, w.meetings])).toEqual([["2026-10-01", 2, 1], ["2026-10-03", 7, 35]]);
  });

  it("counts the previous window for the deltas, and held meetings", async () => {
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id);
    const ago = (d: number) => new Date(NOW.getTime() - d * DAY);
    await prospect(workspace.id, campaign.id, account.id, { createdAt: ago(40), invitedAt: ago(39), connectedAt: ago(38) });
    await prospect(workspace.id, campaign.id, account.id, { createdAt: ago(35), invitedAt: ago(34) });
    const recent = await prospect(workspace.id, campaign.id, account.id, { createdAt: ago(5), invitedAt: ago(4), connectedAt: ago(3) });
    await db.meeting.create({ data: { workspaceId: workspace.id, prospectId: recent.id, campaignId: campaign.id, startsAt: ago(1), status: "COMPLETED", createdAt: ago(2) } });
    await db.meeting.create({ data: { workspaceId: workspace.id, prospectId: recent.id, campaignId: campaign.id, startsAt: ago(-2), createdAt: ago(1) } });
    await db.meeting.create({ data: { workspaceId: workspace.id, prospectId: recent.id, campaignId: campaign.id, startsAt: ago(-3), status: "CANCELED", createdAt: ago(1) } });

    const data = await dashboard(workspace.id, 30, NOW);
    expect(data.kpis).toMatchObject({ found: 1, invited: 1, acceptanceRate: 1, meetings: 2, meetingsCompleted: 1 });
    expect(data.previousKpis).toMatchObject({ found: 2, invited: 2, acceptanceRate: 0.5, meetings: 0, meetingsCompleted: 0 });
  });
});

describe("MCP overview", () => {
  it("includes what needs attention and names the engine tool after the app button", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "PAUSED", statusReason: "Session LinkedIn expirée" } });
    const user = await db.user.create({ data: { email: `p1-${Date.now()}@example.com`, name: "Alex", passwordHash: "x", memberships: { create: { workspaceId: workspace.id } } } });
    const { token } = await createToken(workspace.id, user.id, "Claude Code");
    const transport = new StreamableHTTPClientTransport(new URL("http://vela.test/api/mcp"), {
      requestInit: { headers: { Authorization: `Bearer ${token}` } },
      fetch: (url, init) => POST(new Request(url, init)),
    });
    const client = new Client({ name: "test", version: "1.0.0" });
    await client.connect(transport);

    const { tools } = await client.listTools();
    expect(tools.find((t) => t.name === "run_engine")?.title).toBe("Synchroniser maintenant");
    const result = await client.callTool({ name: "get_overview", arguments: { days: 30 } });
    const overview = JSON.parse((result.content as { text: string }[])[0]!.text);
    expect(overview.attention[0]).toMatchObject({ kind: "account_paused", severity: "high", href: `/accounts#${account.id}` });
    expect(overview.previousKpis).toBeDefined();
    await client.close();
  });
});
