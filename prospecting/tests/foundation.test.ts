import { beforeEach, describe, expect, it } from "vitest";
import { cn } from "@/lib/cn";
import { deltaRatio, formatAgo, plural } from "@/lib/format";
import { ACTIVITY_LABELS, ACTIVITY_VISUALS, semanticTone } from "@/lib/labels";
import { sequenceEndDay, sequenceTimeline } from "@/server/domain/followups";
import { rates } from "@/server/domain/rates";
import { HOUR, MINUTE } from "@/server/domain/time";
import { runTick } from "@/server/engine/tick";
import { SimulatorProvider } from "@/server/linkedin/simulator/provider";
import { funnelFromStages } from "@/server/services/campaigns";
import { engineStatus, isSimulatorOnly } from "@/server/services/engine-status";
import { createWorkspace, db, deps, resetDb } from "./helpers";

const NOW = new Date("2026-10-05T07:00:00Z");

describe("UI helpers", () => {
  it("merges the custom type scale, radii and shadows", () => {
    expect(cn("text-h1 font-semibold text-ink")).toBe("text-h1 font-semibold text-ink");
    expect(cn("text-sm", "text-2xs")).toBe("text-2xs");
    expect(cn("rounded-control", "rounded-full")).toBe("rounded-full");
    expect(cn("shadow-card", "shadow-none")).toBe("shadow-none");
  });

  it("maps legacy tone names to semantic tones", () => {
    expect(semanticTone("red")).toBe("danger");
    expect(semanticTone("gray")).toBe("neutral");
    expect(semanticTone("ai")).toBe("ai");
  });

  it("gives every activity type a label and a visual", () => {
    expect(Object.keys(ACTIVITY_VISUALS).sort()).toEqual(Object.keys(ACTIVITY_LABELS).sort());
  });

  it("formats short durations, deltas and French plurals", () => {
    expect(formatAgo(new Date(NOW.getTime() - 30_000), NOW)).toBe("à l'instant");
    expect(formatAgo(new Date(NOW.getTime() - 2 * MINUTE), NOW)).toBe("il y a 2 min");
    expect(formatAgo(new Date(NOW.getTime() - 3 * HOUR), NOW)).toBe("il y a 3 h");
    expect(deltaRatio(12, 10)).toBeCloseTo(0.2);
    expect(deltaRatio(5, 0)).toBeNull();
    expect(plural(0, "réponse")).toBe("0 réponse");
    expect(plural(3, "prospect trouvé", "prospects trouvés")).toBe("3 prospects trouvés");
  });
});

describe("domain helpers", () => {
  it("adds follow-up delays up from the first message", () => {
    const steps = [{ delayDays: 3 }, { delayDays: 5 }];
    expect(sequenceTimeline(steps)).toEqual([
      { index: 1, afterPrevDays: 3, dayFromFirst: 3 },
      { index: 2, afterPrevDays: 5, dayFromFirst: 8 },
    ]);
    expect(sequenceEndDay(steps)).toBe(15);
    expect(sequenceEndDay([])).toBe(7);
  });

  it("computes funnel rates and returns null on empty denominators", () => {
    const funnel = funnelFromStages({ INVITED: 10, CONNECTED: 2, MESSAGED: 4, UNRESPONSIVE: 2, REPLIED: 1, MEETING_BOOKED: 1 });
    expect(funnel.messaged).toBe(8);
    expect(rates(funnel)).toEqual({ acceptance: 10 / 20, reply: 2 / 8, meeting: 1 / 2 });
    expect(rates({ invited: 0, connected: 0, messaged: 0, replied: 0, meetings: 0 })).toEqual({ acceptance: null, reply: null, meeting: null });
  });
});

describe("engine status", () => {
  beforeEach(resetDb);

  it("reads ok, late and down from the last sync of active accounts", async () => {
    const { workspace, account } = await createWorkspace();
    expect((await engineStatus(workspace.id, NOW)).level).toBe("down");

    const at = (ago: number) => db.linkedInAccount.update({ where: { id: account.id }, data: { lastSyncedAt: new Date(NOW.getTime() - ago) } });
    await at(2 * MINUTE);
    const ok = await engineStatus(workspace.id, NOW);
    expect(ok).toMatchObject({ level: "ok", providers: ["simulator"], pausedAccounts: [], erroredAccounts: [] });
    expect(isSimulatorOnly(ok)).toBe(true);
    await at(20 * MINUTE);
    expect((await engineStatus(workspace.id, NOW)).level).toBe("late");
    await at(2 * HOUR);
    expect((await engineStatus(workspace.id, NOW)).level).toBe("down");

    // A pass in progress holds the lease: the engine is working.
    await db.linkedInAccount.update({ where: { id: account.id }, data: { lockedUntil: new Date(NOW.getTime() + 5 * MINUTE) } });
    expect(await engineStatus(workspace.id, NOW)).toMatchObject({ level: "ok", syncing: true });
  });

  it("lists paused accounts and is down without an active one", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: account.id }, data: { status: "PAUSED", statusReason: "Session expirée", lastSyncedAt: NOW } });
    const status = await engineStatus(workspace.id, NOW);
    expect(status.level).toBe("down");
    expect(status.pausedAccounts).toEqual([{ id: account.id, fullName: "Alex Martin", statusReason: "Session expirée" }]);
  });

  it("keeps a failed pass's error on the account until a pass succeeds", async () => {
    const { workspace, account } = await createWorkspace();
    const failing = deps(NOW);
    const simulator = new SimulatorProvider(db, 1);
    failing.providerFor = () => Object.assign(Object.create(simulator), { fetchEvents: () => Promise.reject(new Error("LinkedIn indisponible")) });

    const [result] = await runTick(failing, { workspaceId: workspace.id });
    expect(result?.error).toBe("LinkedIn indisponible");
    const status = await engineStatus(workspace.id, NOW);
    expect(status.erroredAccounts).toEqual([{ id: account.id, fullName: "Alex Martin", lastError: "LinkedIn indisponible", lastErrorAt: NOW }]);

    const later = new Date(NOW.getTime() + 10 * MINUTE);
    const [ok] = await runTick(deps(later), { workspaceId: workspace.id });
    expect(ok?.error).toBeUndefined();
    const fixed = await db.linkedInAccount.findUniqueOrThrow({ where: { id: account.id } });
    expect(fixed).toMatchObject({ lastError: null, lastErrorAt: null, lastSyncedAt: later });
  });
});
