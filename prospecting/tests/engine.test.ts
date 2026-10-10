import { beforeEach, describe, expect, it } from "vitest";
import { classifyIntent } from "@/server/agents/setter";
import { DAY, HOUR } from "@/server/domain/time";
import { runTick } from "@/server/engine/tick";
import { createCampaign, createWorkspace, db, deps, resetDb } from "./helpers";

const START = new Date("2026-10-05T07:00:00Z"); // Monday 09:00 in Paris

async function simulate(workspaceId: string, from: Date, days: number, step = 2 * HOUR) {
  let now = from;
  const end = from.getTime() + days * DAY;
  while (now.getTime() < end) {
    const results = await runTick(deps(now), { workspaceId });
    for (const r of results) expect(r.error).toBeUndefined();
    now = new Date(now.getTime() + step);
  }
  return now;
}

beforeEach(resetDb);

describe("prospecting engine on the simulator", () => {
  it("runs the full funnel without ever exceeding LinkedIn quotas", async () => {
    const { workspace, account } = await createWorkspace({ accountType: "FREE" });
    await createCampaign(workspace.id, account.id);

    await simulate(workspace.id, START, 21);

    const stages = await db.prospect.groupBy({ by: ["stage"], where: { workspaceId: workspace.id }, _count: true });
    const count = (stage: string) => stages.find((s) => s.stage === stage)?._count ?? 0;
    expect(count("DISQUALIFIED")).toBeGreaterThan(0);
    expect(count("MESSAGED") + count("REPLIED") + count("MEETING_BOOKED") + count("NOT_INTERESTED") + count("UNRESPONSIVE")).toBeGreaterThan(10);

    // Quotas: free account => at most 40 invites in any 24h and 100 in any 7 days.
    const invites = await db.activity.findMany({ where: { accountId: account.id, type: "INVITE_SENT" }, orderBy: { createdAt: "asc" } });
    expect(invites.length).toBeGreaterThan(100);
    for (let i = 0; i < invites.length; i++) {
      const t = invites[i]!.createdAt.getTime();
      const inDay = invites.filter((x) => x.createdAt.getTime() > t - DAY && x.createdAt.getTime() <= t).length;
      const inWeek = invites.filter((x) => x.createdAt.getTime() > t - 7 * DAY && x.createdAt.getTime() <= t).length;
      expect(inDay).toBeLessThanOrEqual(40);
      expect(inWeek).toBeLessThanOrEqual(100);
    }

    // Only qualified people get invited, and each person at most once.
    const invitedIds = invites.map((i) => i.prospectId);
    expect(new Set(invitedIds).size).toBe(invitedIds.length);
    const invitedProspects = await db.prospect.findMany({ where: { id: { in: invitedIds as string[] } } });
    for (const p of invitedProspects) expect(p.score! >= 50 || p.source === "IMPORT").toBe(true);
    expect(invitedProspects.some((p) => p.industry === "Recrutement")).toBe(false);

    // The setter answered, escalated and booked meetings.
    const types = await db.activity.groupBy({ by: ["type"], where: { workspaceId: workspace.id }, _count: true });
    const n = (type: string) => types.find((t) => t.type === type)?._count ?? 0;
    expect(n("REPLY_RECEIVED")).toBeGreaterThan(0);
    expect(n("AI_REPLY_SENT")).toBeGreaterThan(0);
    expect(n("FOLLOW_UP_SENT")).toBeGreaterThan(0);
    expect(await db.meeting.count({ where: { workspaceId: workspace.id } })).toBeGreaterThan(0);
  });

  it("follows the sequence timing and stops at the first reply", async () => {
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id);
    await simulate(workspace.id, START, 25);

    const prospects = await db.prospect.findMany({
      where: { campaignId: campaign.id, firstMessagedAt: { not: null } },
      include: { conversation: { include: { messages: { orderBy: { sentAt: "asc" } } } } },
    });
    expect(prospects.length).toBeGreaterThan(0);
    for (const p of prospects) {
      const messages = p.conversation?.messages ?? [];
      const sequence = messages.filter((m) => m.author === "SEQUENCE");
      expect(sequence.length).toBeLessThanOrEqual(3); // first message + 2 follow-ups
      // Follow-up 1 waits 3 days, follow-up 2 waits 4 more days.
      if (sequence[1]) expect(sequence[1].sentAt.getTime() - sequence[0]!.sentAt.getTime()).toBeGreaterThanOrEqual(3 * DAY);
      if (sequence[2]) expect(sequence[2].sentAt.getTime() - sequence[1]!.sentAt.getTime()).toBeGreaterThanOrEqual(4 * DAY);
      // A reply stops the sequence, except "out of office", which resumes it a week later.
      for (const [i, m] of messages.entries()) {
        if (m.author !== "SEQUENCE") continue;
        const lastInbound = messages.slice(0, i).filter((x) => x.direction === "INBOUND").at(-1);
        if (lastInbound) expect({ body: lastInbound.body, intent: classifyIntent(lastInbound.body) }).toMatchObject({ intent: "OUT_OF_OFFICE" });
        if (lastInbound) expect(m.sentAt.getTime() - lastInbound.sentAt.getTime()).toBeGreaterThanOrEqual(7 * DAY - HOUR);
      }
    }
    // Nobody who refused gets another automated message.
    const refused = await db.prospect.findMany({
      where: { campaignId: campaign.id, stage: "NOT_INTERESTED" },
      include: { conversation: { include: { messages: { orderBy: { sentAt: "asc" } } } } },
    });
    for (const p of refused) {
      const msgs = p.conversation!.messages;
      const lastInbound = msgs.filter((m) => m.direction === "INBOUND").at(-1)!;
      const after = msgs.filter((m) => m.sentAt > lastInbound.sentAt && m.author === "SEQUENCE");
      expect(after).toEqual([]);
    }
  });

  it("drafts replies instead of sending them in approval mode", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id, { setterMode: "APPROVAL" });
    await simulate(workspace.id, START, 14);
    expect(await db.activity.count({ where: { workspaceId: workspace.id, type: "AI_REPLY_SENT" } })).toBe(0);
    expect(await db.draft.count({ where: { conversation: { workspaceId: workspace.id } } })).toBeGreaterThan(0);
  });

  it("hands every reply to a human when the setter is off", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id, { setterMode: "OFF" });
    await simulate(workspace.id, START, 14);
    expect(await db.activity.count({ where: { workspaceId: workspace.id, type: "AI_REPLY_SENT" } })).toBe(0);
    const replied = await db.conversation.count({ where: { workspaceId: workspace.id, messages: { some: { direction: "INBOUND" } } } });
    const needsHuman = await db.conversation.count({ where: { workspaceId: workspace.id, status: "NEEDS_HUMAN" } });
    expect(replied).toBeGreaterThan(0);
    expect(needsHuman).toBe(replied);
  });

  it("sends nothing outside the sending window", async () => {
    const { workspace, account } = await createWorkspace({ allWeek: false });
    await createCampaign(workspace.id, account.id);
    const saturday = new Date("2026-10-10T09:00:00Z");
    const [result] = await runTick(deps(saturday), { workspaceId: workspace.id });
    expect(result!.sourced).toBeGreaterThan(0);
    expect(result!.outreach?.skipped).toBe("outside_window");
    expect(await db.activity.count({ where: { accountId: account.id, type: "INVITE_SENT" } })).toBe(0);
  });

  it("never double-sends when two ticks run at the same time", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id);
    await runTick(deps(START), { workspaceId: workspace.id }); // source + score
    const later = new Date(START.getTime() + HOUR);
    await Promise.all([runTick(deps(later), { workspaceId: workspace.id }), runTick(deps(later), { workspaceId: workspace.id })]);
    const invites = await db.activity.findMany({ where: { accountId: account.id, type: "INVITE_SENT" } });
    expect(new Set(invites.map((i) => i.prospectId)).size).toBe(invites.length);
  });

  it("does not contact the same person from two campaigns", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id, { name: "A" });
    await createCampaign(workspace.id, account.id, { name: "B" });
    await simulate(workspace.id, START, 2);
    const dupes = await db.prospect.groupBy({ by: ["externalId"], where: { workspaceId: workspace.id }, _count: true, having: { externalId: { _count: { gt: 1 } } } });
    expect(dupes).toEqual([]);
  });
});
