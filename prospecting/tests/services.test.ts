import { beforeEach, describe, expect, it } from "vitest";
import { HOUR } from "@/server/domain/time";
import { runTick } from "@/server/engine/tick";
import { connectAccount } from "@/server/services/accounts";
import { login, signup } from "@/server/services/auth";
import { campaignSchema, createCampaign, importProspects } from "@/server/services/campaigns";
import { UserError } from "@/server/services/errors";
import { SimulatorProvider } from "@/server/linkedin/simulator/provider";
import { approveDraft, handBackToAi, rejectDraft, sendHumanReply } from "@/server/services/inbox";
import { createCampaign as createTestCampaign, createWorkspace, db, deps, resetDb } from "./helpers";

beforeEach(resetDb);

const validCampaign = {
  name: "Test",
  sources: '["SEARCH"]',
  titles: '["CFO"]',
  keywords: "",
  industries: "SaaS, Conseil",
  locations: "Paris\nLyon",
  companySizes: [],
  signals: [],
  postUrls: "[]",
  exclusions: "[]",
  minScore: "60",
  weeklyProspectTarget: "100",
  offer: "Offre",
  persona: "",
  inviteNote: "",
  firstMessage: "Bonjour {{firstName}}",
  followUps: JSON.stringify([{ delayDays: 3, template: "Relance {{firstName}}" }]),
  setterMode: "AUTO",
  bookingUrl: "",
};

describe("auth", () => {
  it("signs up into a Pro trial workspace and logs in", async () => {
    const user = await signup({ name: "Léa", email: "lea@example.com", password: "password123", company: "Nova" });
    const membership = await db.membership.findFirstOrThrow({ where: { userId: user.id }, include: { workspace: true } });
    expect(membership.workspace.plan).toBe("PRO");
    expect(membership.workspace.trialEndsAt!.getTime()).toBeGreaterThan(Date.now());
    expect((await login({ email: "lea@example.com", password: "password123" })).id).toBe(user.id);
    await expect(login({ email: "lea@example.com", password: "wrong-password" })).rejects.toBeInstanceOf(UserError);
    await expect(signup({ name: "X", email: "lea@example.com", password: "password123", company: "Y" })).rejects.toBeInstanceOf(UserError);
  });
});

describe("plan limits", () => {
  it("caps LinkedIn accounts per plan", async () => {
    const { workspace } = await createWorkspace({ plan: "PRO" });
    await expect(connectAccount(workspace.id, { fullName: "Second", headline: "", accountType: "FREE" })).rejects.toThrow(/un seul compte/);
    await db.workspace.update({ where: { id: workspace.id }, data: { plan: "AGENCY" } });
    await connectAccount(workspace.id, { fullName: "Second", headline: "", accountType: "FREE" });
    expect(await db.linkedInAccount.count({ where: { workspaceId: workspace.id } })).toBe(2);
  });

  it("parses campaign forms and refuses what the plan does not include", async () => {
    const { workspace, account } = await createWorkspace({ plan: "STARTER" });
    const parsed = campaignSchema.parse({ ...validCampaign, accountId: account.id });
    expect(parsed.industries).toEqual(["SaaS", "Conseil"]);
    expect(parsed.locations).toEqual(["Paris", "Lyon"]);
    expect(parsed.inviteNote).toBeNull();
    await expect(createCampaign(workspace.id, parsed)).rejects.toThrow(/setter/i);
    const created = await createCampaign(workspace.id, { ...parsed, setterMode: "OFF" });
    expect(created.status).toBe("DRAFT");
  });

  it("normalizes browser line endings in templates", () => {
    const parsed = campaignSchema.parse({
      ...validCampaign,
      accountId: "x",
      firstMessage: "Bonjour\r\n\r\nSuite",
      followUps: JSON.stringify([{ delayDays: 2, template: "a\r\nb" }]),
    });
    expect(parsed.firstMessage).toBe("Bonjour\n\nSuite");
    expect(parsed.followUps[0]!.template).toBe("a\nb");
  });

  it("rejects unknown template variables", () => {
    const result = campaignSchema.safeParse({ ...validCampaign, accountId: "x", firstMessage: "Bonjour {{prenom}}" });
    expect(result.success).toBe(false);
  });
});

describe("list import", () => {
  it("pulls profile URLs out of any CSV, dedupes them and keeps imported people whatever their score", async () => {
    const { workspace, account } = await createWorkspace();
    const campaign = await createTestCampaign(workspace.id, account.id, { minScore: 100, sources: [], exclusions: [] });
    const csv = [
      "name,url",
      "Camille,https://www.linkedin.com/in/camille-durand-42/",
      "Paul,https://fr.linkedin.com/in/paul-roux",
      "Dup,https://www.linkedin.com/in/camille-durand-42",
      "Bad,https://example.com/in/nobody",
    ].join("\n");
    const result = await importProspects(workspace.id, campaign.id, csv);
    expect(result).toEqual({ found: 2, imported: 2, skipped: 0 });
    const prospects = await db.prospect.findMany({ where: { campaignId: campaign.id } });
    expect(prospects.map((p) => p.firstName).sort()).toEqual(["Camille", "Paul"]);
    expect(prospects.every((p) => p.stage === "QUALIFIED" && p.source === "IMPORT")).toBe(true);

    const again = await importProspects(workspace.id, campaign.id, csv);
    expect(again.imported).toBe(0);
  });

  it("still applies exclusions to imported people", async () => {
    const { workspace, account } = await createWorkspace();
    const [camilleProfile] = await new SimulatorProvider(db, 1).lookupProfiles(account, ["https://www.linkedin.com/in/camille-durand"]);
    // Exclusions match the job title, headline, company and industry (e.g. a competitor's name).
    const campaign = await createTestCampaign(workspace.id, account.id, { sources: [], exclusions: [camilleProfile!.company] });
    await importProspects(workspace.id, campaign.id, "https://www.linkedin.com/in/camille-durand\nhttps://www.linkedin.com/in/paul-roux");
    const camille = await db.prospect.findFirstOrThrow({ where: { campaignId: campaign.id, firstName: "Camille" } });
    expect(camille.stage).toBe("DISQUALIFIED");
  });

  it("is not available on Starter", async () => {
    const { workspace, account } = await createWorkspace({ plan: "STARTER" });
    const campaign = await createTestCampaign(workspace.id, account.id, { setterMode: "OFF" });
    await expect(importProspects(workspace.id, campaign.id, "https://www.linkedin.com/in/a-b")).rejects.toThrow(/Pro/);
  });
});

describe("inbox", () => {
  async function workspaceWithDrafts() {
    const { workspace, account } = await createWorkspace();
    await createTestCampaign(workspace.id, account.id, { setterMode: "APPROVAL" });
    let now = new Date("2026-10-05T07:00:00Z");
    for (let i = 0; i < 120 && (await db.draft.count({ where: { status: "PENDING" } })) < 2; i++) {
      await runTick(deps(now), { workspaceId: workspace.id });
      now = new Date(now.getTime() + 2 * HOUR);
    }
    const drafts = await db.draft.findMany({ where: { status: "PENDING" }, include: { conversation: true } });
    expect(drafts.length).toBeGreaterThanOrEqual(2);
    return { workspace, drafts };
  }

  it("sends an approved draft exactly once, with the human's edits", async () => {
    const { workspace, drafts } = await workspaceWithDrafts();
    const draft = drafts[0]!;
    await approveDraft(workspace.id, draft.id, "Texte relu par un humain");
    const last = await db.message.findFirstOrThrow({ where: { conversationId: draft.conversationId }, orderBy: { sentAt: "desc" } });
    expect(last).toMatchObject({ body: "Texte relu par un humain", author: "AI", direction: "OUTBOUND" });
    await expect(approveDraft(workspace.id, draft.id)).rejects.toBeInstanceOf(UserError);
  });

  it("hands the thread to a human when a draft is rejected", async () => {
    const { workspace, drafts } = await workspaceWithDrafts();
    await rejectDraft(workspace.id, drafts[1]!.id);
    const conversation = await db.conversation.findUniqueOrThrow({ where: { id: drafts[1]!.conversationId } });
    expect(conversation.status).toBe("NEEDS_HUMAN");
  });

  it("records human replies and lets the setter answer again on hand-back", async () => {
    const { workspace, drafts } = await workspaceWithDrafts();
    const conversationId = drafts[0]!.conversationId;
    await sendHumanReply(workspace.id, conversationId, "Je m'en occupe.", false);
    expect((await db.conversation.findUniqueOrThrow({ where: { id: conversationId } })).status).toBe("HUMAN");
    expect(await db.draft.count({ where: { conversationId, status: "PENDING" } })).toBe(0);

    await db.message.create({ data: { conversationId, direction: "INBOUND", author: "PROSPECT", body: "Oui, on peut en parler ?" } });
    await handBackToAi(workspace.id, conversationId);
    expect(await db.draft.count({ where: { conversationId, status: "PENDING" } })).toBe(1);
  });

  it("never touches another workspace's conversations", async () => {
    const { drafts } = await workspaceWithDrafts();
    const other = await db.workspace.create({ data: { name: "Other" } });
    await expect(approveDraft(other.id, drafts[0]!.id)).rejects.toBeInstanceOf(UserError);
    await expect(sendHumanReply(other.id, drafts[0]!.conversationId, "hi", false)).rejects.toBeInstanceOf(UserError);
  });
});
