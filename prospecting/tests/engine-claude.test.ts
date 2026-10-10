import { beforeEach, describe, expect, it } from "vitest";
import { claudeAgents } from "@/server/agents";
import { HOUR } from "@/server/domain/time";
import { runTick } from "@/server/engine/tick";
import { SimulatorProvider } from "@/server/linkedin/simulator/provider";
import { fakeClaude } from "./fake-claude";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

beforeEach(resetDb);

/** A stand-in Claude that scores everyone 85, adds a line to each message, and offers the booking link. */
function plausibleClaude() {
  return fakeClaude((call) => {
    const input = call.messages[0]!.content;
    if (input.includes("<profils>")) {
      const ids = [...input.matchAll(/"id":"(p\d+)"/g)].map((m) => m[1]);
      return { evaluations: ids.map((id) => ({ id, score: 85, summary: "Décideur financier d'une PME ciblée.", reasons: [{ label: "Poste de décision", favorable: true }] })) };
    }
    if (input.includes("<message_de_base>")) {
      const base = /<message_de_base>\n([\s\S]*)\n<\/message_de_base>/.exec(input)![1]!;
      return { message: `${base}\n\n(personnalisé)` };
    }
    return { intent: "INTERESTED", action: "reply", message: "Avec plaisir, voici mon agenda : https://cal.example.com/demo", reason: "Intérêt exprimé.", close_conversation: false };
  });
}

describe("engine with Claude agents", () => {
  it("records which agent scored, wrote and drafted", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id, { setterMode: "APPROVAL", inviteNote: null });
    const fake = plausibleClaude();
    const agents = claudeAgents(fake.client);

    let now = new Date("2026-10-05T07:00:00Z");
    for (let i = 0; i < 60; i++) {
      const results = await runTick({ db, agents, providerFor: () => new SimulatorProvider(db, 1), now }, { workspaceId: workspace.id });
      for (const r of results) expect(r.error).toBeUndefined();
      now = new Date(now.getTime() + 2 * HOUR);
    }

    const scored = await db.prospect.groupBy({ by: ["scoredBy"], where: { workspaceId: workspace.id, score: { not: null } }, _count: true });
    expect(scored.find((s) => s.scoredBy === "claude")?._count).toBeGreaterThan(0);
    const excludedByRules = await db.prospect.count({ where: { workspaceId: workspace.id, disqualifiedReason: { startsWith: "Exclusion" } } });
    const claudeScoredExcluded = await db.prospect.count({ where: { workspaceId: workspace.id, scoredBy: "claude", disqualifiedReason: { startsWith: "Exclusion" } } });
    expect(claudeScoredExcluded).toBe(0);
    expect(excludedByRules).toBeGreaterThan(0); // the "Recrutement" exclusion did trigger, and only rules decided it

    const sequence = await db.message.findMany({ where: { author: "SEQUENCE", conversation: { workspaceId: workspace.id } } });
    expect(sequence.length).toBeGreaterThan(0);
    expect(sequence.every((m) => m.body.endsWith("(personnalisé)"))).toBe(true);

    const drafts = await db.draft.findMany({ where: { conversation: { workspaceId: workspace.id } } });
    expect(drafts.length).toBeGreaterThan(0);
    expect(drafts.filter((d) => d.intent === "INTERESTED").every((d) => d.author === "claude")).toBe(true);
  });

  it("keeps templates verbatim for campaigns that turned personalization off", async () => {
    const { workspace, account } = await createWorkspace();
    await createCampaign(workspace.id, account.id, { aiPersonalization: false });
    const agents = claudeAgents(plausibleClaude().client);
    let now = new Date("2026-10-05T07:00:00Z");
    for (let i = 0; i < 30; i++) {
      await runTick({ db, agents, providerFor: () => new SimulatorProvider(db, 1), now }, { workspaceId: workspace.id });
      now = new Date(now.getTime() + 2 * HOUR);
    }
    const sequence = await db.message.findMany({ where: { author: "SEQUENCE", conversation: { workspaceId: workspace.id } } });
    expect(sequence.length).toBeGreaterThan(0);
    expect(sequence.some((m) => m.body.includes("(personnalisé)"))).toBe(false);
  });
});
