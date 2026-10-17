import type { ProspectStage } from "@prisma/client";
import { beforeEach, describe, expect, it } from "vitest";
import { launchPlan, launchReadiness, prospectTally, readinessChecks } from "@/server/services/campaign-insights";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

beforeEach(resetDb);

const SATURDAY = new Date("2026-10-17T10:00:00Z");

let seq = 0;
async function addProspects(workspaceId: string, campaignId: string, accountId: string, stage: ProspectStage, count: number) {
  for (let i = 0; i < count; i++) {
    seq += 1;
    await db.prospect.create({
      data: {
        workspaceId, campaignId, accountId, externalId: `p4r-${seq}`, profileUrl: `https://www.linkedin.com/in/p4r-${seq}`,
        firstName: "Léa", lastName: `Durand ${seq}`, source: "IMPORT", stage,
        ...(stage === "DISQUALIFIED" ? { disqualifiedReason: "Exclusion : Recrutement" } : {}),
      },
    });
  }
}

/** An import-only draft (no source, no criterion) on a simulator account; the booking link comes from the workspace. */
async function importDraft(stages: Partial<Record<ProspectStage, number>>) {
  const { workspace, account } = await createWorkspace();
  const created = await createCampaign(workspace.id, account.id, { status: "DRAFT", setterMode: "APPROVAL", sources: [], titles: [], bookingUrl: "" });
  for (const [stage, count] of Object.entries(stages)) await addProspects(workspace.id, created.id, account.id, stage as ProspectStage, count);
  const campaign = await db.campaign.findUniqueOrThrow({ where: { id: created.id }, include: { account: true } });
  return { workspace, campaign };
}

const targeting = (checks: ReturnType<typeof readinessChecks>) => checks.find((c) => c.key === "targeting")!;

describe("launch readiness counts prospects by stage", () => {
  it("tallies what the engine can still do with each prospect", () => {
    expect(prospectTally({ NEW: 1, QUALIFIED: 8, DISQUALIFIED: 3, INVITED: 2, MESSAGED: 1, REPLIED: 4 })).toEqual({
      total: 19, toContact: 9, excluded: 3, inSequence: 3,
    });
    expect(prospectTally({})).toEqual({ total: 0, toContact: 0, excluded: 0, inSequence: 0 });
  });

  it("blocks an import-only draft whose imports were all set aside", async () => {
    const { workspace, campaign } = await importDraft({ DISQUALIFIED: 12 });
    const readiness = await launchReadiness(campaign, workspace, SATURDAY);
    expect(readiness.blocked).toBe(true);
    expect(readiness.prospects).toMatchObject({ total: 12, toContact: 0, excluded: 12 });
    expect(targeting(readiness.checks)).toMatchObject({
      level: "blocker",
      detail: "12 profils importés, tous écartés : choisissez une source de prospects ou importez une autre liste.",
    });
    // The plan never says they will be invited.
    expect(readiness.plan[0]).toMatch(/^12 profils importés écartés, donc jamais invités/);
  });

  it("counts only the profiles still to contact, and names the ones set aside", async () => {
    const { workspace, campaign } = await importDraft({ QUALIFIED: 9, DISQUALIFIED: 3 });
    const readiness = await launchReadiness(campaign, workspace, SATURDAY);
    expect(readiness.blocked).toBe(false);
    expect(targeting(readiness.checks)).toMatchObject({ level: "ok", detail: "12 profils importés, dont 3 écartés" });
    expect(readiness.plan[0]).toMatch(/^9 des 12 profils importés invités quelle que soit leur note \(3 écartés\), premier message/);
  });

  it("agrees the possessive with a single profile", async () => {
    const { campaign } = await importDraft({});
    const one = { total: 1, toContact: 1, excluded: 0, inSequence: 0 };
    expect(launchPlan(campaign, one)[0]).toMatch(/^1 profil importé invité quelle que soit sa note, /);
    expect(launchPlan(campaign, { ...one, total: 2, excluded: 1 })[0]).toMatch(/^1 des 2 profils importés invité quelle que soit sa note \(1 écarté\), /);
    expect(launchPlan(campaign, { total: 1, toContact: 0, excluded: 1, inSequence: 0 })[0]).toMatch(/^1 profil importé écarté, donc jamais invité, /);
  });

  it("lets a paused import-only campaign resume while prospects are still in the sequence", async () => {
    const { workspace, campaign } = await importDraft({});
    const paused = { ...campaign, status: "PAUSED" as const };
    const inSequence = { total: 5, toContact: 0, excluded: 1, inSequence: 4 };
    expect(targeting(readinessChecks({ campaign: paused, workspace, prospectCount: inSequence })).level).toBe("ok");
    // Everyone finished or set aside: resuming would do nothing.
    const finished = { total: 5, toContact: 0, excluded: 1, inSequence: 0 };
    expect(targeting(readinessChecks({ campaign: paused, workspace, prospectCount: finished }))).toMatchObject({
      level: "blocker",
      detail: "Plus aucun prospect à contacter : choisissez une source de prospects ou importez une autre liste.",
    });
  });

  it("does not let set-aside imports stand in for sources that find nobody", async () => {
    const { workspace, account } = await createWorkspace();
    await db.linkedInAccount.update({ where: { id: account.id }, data: { provider: "browser" } });
    const created = await createCampaign(workspace.id, account.id, { status: "DRAFT", setterMode: "APPROVAL", sources: ["SIGNALS"] });
    const campaign = await db.campaign.findUniqueOrThrow({ where: { id: created.id }, include: { account: true } });
    const allAside = { total: 4, toContact: 0, excluded: 4, inSequence: 0 };
    expect(targeting(readinessChecks({ campaign, workspace, prospectCount: allAside })).level).toBe("blocker");
    expect(targeting(readinessChecks({ campaign, workspace, prospectCount: { ...allAside, toContact: 1, total: 5 } })).level).toBe("ok");
  });
});

describe("blocker details read on their own", () => {
  it("names the missing booking link without relying on the line's label", async () => {
    const { workspace, campaign } = await importDraft({ QUALIFIED: 1 });
    const booking = readinessChecks({ campaign, workspace: { ...workspace, bookingUrl: "" }, prospectCount: 1 }).find((c) => c.key === "booking")!;
    expect(booking.level).toBe("blocker");
    expect(booking.detail).toBe("Aucun lien de réservation : le setter l'envoie aux prospects intéressés. Renseignez-le dans les Réglages (ou dans la campagne).");
  });
});
