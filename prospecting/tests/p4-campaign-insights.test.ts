import type { ProspectStage } from "@prisma/client";
import { beforeEach, describe, expect, it } from "vitest";
import { rates } from "@/server/domain/rates";
import { DAY, HOUR } from "@/server/domain/time";
import {
  effectiveSettings,
  firstSentence,
  followUpSummary,
  launchPlan,
  launchReadiness,
  nextActions,
  personalizationLabel,
  readinessChecks,
  sendingWindowLabel,
} from "@/server/services/campaign-insights";
import { listCampaigns } from "@/server/services/campaigns";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

beforeEach(resetDb);

// Saturday 17 October 2026, 12:00 in Paris.
const SATURDAY = new Date("2026-10-17T10:00:00Z");
// Monday 19 October 2026, 11:00 in Paris.
const MONDAY = new Date("2026-10-19T09:00:00Z");
const DEFAULT_DELAYS = [
  { delayDays: 3, template: "{{firstName}}, je me permets de relancer." },
  { delayDays: 5, template: "Dernière relance {{firstName}}." },
];

let seq = 0;
async function prospect(workspaceId: string, campaignId: string, accountId: string, data: { stage?: ProspectStage; nextActionAt?: Date; followUpsSent?: number; snoozedUntil?: Date } = {}) {
  seq += 1;
  return db.prospect.create({
    data: {
      workspaceId, campaignId, accountId, externalId: `p4-${seq}`, profileUrl: `https://www.linkedin.com/in/p4-${seq}`,
      firstName: "Léa", lastName: `Durand ${seq}`, source: "SEARCH", ...data,
    },
  });
}

async function draft(overrides: Parameters<typeof createCampaign>[2] = {}, account: { provider?: string; status?: "ACTIVE" | "PAUSED" | "DISCONNECTED"; statusReason?: string; lastDiagnosisOk?: boolean | null } = {}) {
  const { workspace, account: acc } = await createWorkspace();
  const updated = await db.linkedInAccount.update({ where: { id: acc.id }, data: account });
  const campaign = await createCampaign(workspace.id, acc.id, { status: "DRAFT", setterMode: "APPROVAL", sources: ["SEARCH"], ...overrides });
  const full = await db.campaign.findUniqueOrThrow({ where: { id: campaign.id }, include: { account: true } });
  return { workspace, account: updated, campaign: full };
}

describe("launch readiness", () => {
  it("is ready for a well-configured simulator draft, with no session line", async () => {
    const { workspace, campaign } = await draft({ bookingUrl: "" });
    const readiness = await launchReadiness(campaign, workspace, SATURDAY);
    expect(readiness.blocked).toBe(false);
    expect(readiness.checks.map((c) => [c.key, c.level])).toEqual([
      ["account", "ok"],
      ["targeting", "ok"],
      ["booking", "ok"],
      ["setter", "ok"],
    ]);
    // The workspace's link applies when the campaign has none.
    expect(readiness.checks.find((c) => c.key === "booking")?.detail).toBe("Celui des Réglages");
  });

  it("blocks the launch while the account is paused, and links to /accounts", async () => {
    const { workspace, campaign, account } = await draft({}, { status: "PAUSED", statusReason: "Session expirée" });
    const readiness = await launchReadiness(campaign, workspace, SATURDAY);
    expect(readiness.blocked).toBe(true);
    const line = readiness.checks.find((c) => c.key === "account")!;
    expect(line.level).toBe("blocker");
    expect(line.detail).toContain("Session expirée");
    expect(line.fix?.href).toBe(`/accounts#${account.id}`);
  });

  it("sends a disconnected account's campaign back to the editor", async () => {
    const { workspace, campaign } = await draft({}, { status: "DISCONNECTED" });
    const line = readinessChecks({ campaign, workspace, prospectCount: 0 }).find((c) => c.key === "account")!;
    expect(line.level).toBe("blocker");
    expect(line.fix?.href).toBe(`/campaigns/${campaign.id}/edit#general`);
  });

  it("requires a criterion for the search, or imported prospects without any source", async () => {
    const { workspace, campaign } = await draft({ titles: [], keywords: [], searchUrl: "" });
    const targeting = (count: number, c = campaign) => readinessChecks({ campaign: c, workspace, prospectCount: count }).find((x) => x.key === "targeting")!;
    expect(targeting(0).level).toBe("blocker");
    expect(targeting(0).fix?.href).toBe(`/campaigns/${campaign.id}/edit#ciblage`);

    const importOnly = { ...campaign, sources: [] };
    expect(targeting(0, importOnly).level).toBe("blocker");
    expect(targeting(12, importOnly)).toMatchObject({ level: "ok", detail: "12 profils importés" });

    const withUrl = { ...campaign, searchUrl: "https://www.linkedin.com/search/results/people/?keywords=cfo" };
    expect(targeting(0, withUrl).level).toBe("ok");
  });

  it("requires a booking link while the setter is on", async () => {
    const { workspace, campaign } = await draft({ bookingUrl: "" });
    const noLink = { ...workspace, bookingUrl: "" };
    const booking = (c = campaign) => readinessChecks({ campaign: c, workspace: noLink, prospectCount: 0 }).find((x) => x.key === "booking")!;
    expect(booking()).toMatchObject({ level: "blocker", fix: { href: "/settings" } });
    expect(booking({ ...campaign, setterMode: "OFF" }).level).toBe("info");
    expect(booking({ ...campaign, bookingUrl: "https://cal.example.com/x" })).toMatchObject({ level: "ok", detail: "Propre à la campagne" });
  });

  it("warns about buying signals and an unverified session on a real account", async () => {
    const { workspace, campaign } = await draft({ sources: ["SEARCH", "SIGNALS"] }, { provider: "browser", lastDiagnosisOk: null });
    const checks = readinessChecks({ campaign, workspace, prospectCount: 0, now: SATURDAY });
    expect(checks.find((c) => c.key === "signals")?.level).toBe("warn");
    expect(checks.find((c) => c.key === "session")?.level).toBe("warn");
    expect(checks.find((c) => c.key === "targeting")?.level).toBe("ok");

    const verified = { ...campaign, account: { ...campaign.account, lastDiagnosisOk: true, lastDiagnosedAt: new Date(SATURDAY.getTime() - HOUR) } };
    expect(readinessChecks({ campaign: verified, workspace, prospectCount: 0, now: SATURDAY }).find((c) => c.key === "session")).toMatchObject({
      level: "ok", detail: "Dernière vérification il y a 1 h",
    });

    // Signals alone find nobody with a real account.
    const signalsOnly = { ...campaign, sources: ["SIGNALS" as const] };
    expect(readinessChecks({ campaign: signalsOnly, workspace, prospectCount: 0 }).find((c) => c.key === "targeting")?.level).toBe("blocker");
  });

  it("recommends the approval mode to start", async () => {
    const { workspace, campaign } = await draft({ setterMode: "AUTO" });
    const line = readinessChecks({ campaign, workspace, prospectCount: 0 }).find((c) => c.key === "setter")!;
    expect(line).toMatchObject({ level: "info", label: "Setter : Validation recommandé pour démarrer" });
  });

  it("describes what will happen from the settings", async () => {
    const { campaign } = await draft({ weeklyProspectTarget: 150, minScore: 55, followUps: DEFAULT_DELAYS }, {});
    const window = { ...campaign, account: { ...campaign.account, sendingDays: [1, 2, 3, 4, 5], sendingStart: "09:00", sendingEnd: "18:00" } };
    const text = launchPlan(window, 0).join(" ");
    expect(text).toBe(
      "~150 profils/semaine, invitation si note ≥ 55, premier message 4 h après acceptation, relances à J+3 et J+8, setter en mode Validation. " +
        "Envois lun–ven 9 h–18 h ; la séquence s'arrête dès que le prospect répond, et à J+15 sans réponse.",
    );
  });
});

describe("settings summary", () => {
  it("reads follow-ups as cumulative days from the first message", () => {
    expect(followUpSummary(DEFAULT_DELAYS)).toBe("J+3 et J+8 après le premier message");
    expect(followUpSummary([{ delayDays: 2 }, { delayDays: 2 }, { delayDays: 4 }])).toBe("J+2, J+4 et J+8 après le premier message");
    expect(followUpSummary([])).toBe("Aucune relance");
  });

  it("never says personalisation is simply on without Claude", () => {
    expect(personalizationLabel(true, "rules")).toBe("Activée, sans effet tant que Claude n'est pas configuré");
    expect(personalizationLabel(true, "claude")).toMatch(/^Activée/);
    expect(personalizationLabel(false, "rules")).toMatch(/^Désactivée/);
  });

  it("formats the sending window", () => {
    const base = { timezone: "Europe/Paris", sendingDays: [1, 2, 3, 4, 5], sendingStart: "09:00", sendingEnd: "18:00" };
    expect(sendingWindowLabel(base)).toBe("lun–ven 9 h–18 h");
    expect(sendingWindowLabel({ ...base, sendingDays: [1, 3, 5], sendingStart: "08:30" })).toBe("lun, mer et ven 8 h 30–18 h");
    expect(sendingWindowLabel({ ...base, sendingDays: [1, 2, 3, 4, 5, 6, 7], sendingStart: "00:00", sendingEnd: "00:00" })).toBe("tous les jours 24 h/24");
    expect(sendingWindowLabel({ ...base, timezone: "America/New_York" })).toBe("lun–ven 9 h–18 h (America/New_York)");
  });

  it("shows where the booking link and the offer come from", () => {
    const workspace = { bookingUrl: "https://cal.example.com/demo", offer: "Nous automatisons le reporting. En deux semaines." };
    expect(effectiveSettings({ bookingUrl: "", offer: "" }, workspace)).toEqual({
      bookingUrl: { value: "https://cal.example.com/demo", origin: "workspace" },
      offer: { value: "Nous automatisons le reporting.", origin: "workspace" },
    });
    expect(effectiveSettings({ bookingUrl: "https://cal.example.com/c", offer: "Audit gratuit !  Sans engagement." }, workspace)).toEqual({
      bookingUrl: { value: "https://cal.example.com/c", origin: "campaign" },
      offer: { value: "Audit gratuit !", origin: "campaign" },
    });
    expect(effectiveSettings({ bookingUrl: " ", offer: "" }, { bookingUrl: "", offer: "" }).bookingUrl.origin).toBe("none");
    expect(firstSentence("Une offre sans point final")).toBe("Une offre sans point final");
  });
});

describe("next actions", () => {
  it("counts what the engine will do next and reports the sending window", async () => {
    const { workspace, account } = await createWorkspace({ allWeek: false });
    const campaign = await createCampaign(workspace.id, account.id, { followUps: DEFAULT_DELAYS });
    const ids = [workspace.id, campaign.id, account.id] as const;
    await prospect(...ids, { stage: "QUALIFIED" });
    await prospect(...ids, { stage: "QUALIFIED" });
    await prospect(...ids, { stage: "QUALIFIED", snoozedUntil: new Date(MONDAY.getTime() + 2 * DAY) });
    await prospect(...ids, { stage: "INVITED" });
    await prospect(...ids, { stage: "CONNECTED", nextActionAt: new Date(MONDAY.getTime() + 2 * HOUR) });
    await prospect(...ids, { stage: "MESSAGED", followUpsSent: 0, nextActionAt: new Date(MONDAY.getTime() + 5 * HOUR) });
    await prospect(...ids, { stage: "MESSAGED", followUpsSent: 1, nextActionAt: new Date(MONDAY.getTime() - HOUR) });
    await prospect(...ids, { stage: "MESSAGED", followUpsSent: 0, nextActionAt: new Date(MONDAY.getTime() + 3 * DAY) });
    // Every follow-up sent: the next action is the give-up, not a follow-up.
    await prospect(...ids, { stage: "MESSAGED", followUpsSent: 2, nextActionAt: new Date(MONDAY.getTime() + HOUR) });
    await db.linkedInAccount.update({
      where: { id: account.id },
      data: { lastError: "Page LinkedIn inattendue", lastErrorAt: MONDAY, invitesPausedUntil: new Date(MONDAY.getTime() + DAY) },
    });
    const full = await db.campaign.findUniqueOrThrow({ where: { id: campaign.id }, include: { account: true } });

    const monday = await nextActions(full, MONDAY);
    expect(monday).toMatchObject({
      toInvite: 2,
      pendingInvites: 1,
      firstMessages: 1,
      followUpsSoon: 2,
      window: { label: "lun–ven 9 h–18 h", open: true },
      account: { lastError: "Page LinkedIn inattendue" },
    });
    expect(monday.invitesPausedUntil).toEqual(new Date(MONDAY.getTime() + DAY));

    const saturday = await nextActions(full, SATURDAY);
    expect(saturday.window.open).toBe(false);
  });
});

describe("campaign list", () => {
  it("computes the reply rate like the dashboard: replies over contacted prospects", async () => {
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id);
    const stages: ProspectStage[] = ["CONNECTED", "MESSAGED", "MESSAGED", "UNRESPONSIVE", "REPLIED", "MEETING_BOOKED"];
    for (const stage of stages) await prospect(workspace.id, campaign.id, account.id, { stage });
    const [listed] = await listCampaigns(workspace.id);
    // 5 contacted (2 in sequence, 1 unresponsive, 2 replied), 2 replies.
    expect(listed!.funnel.messaged).toBe(5);
    expect(rates(listed!.funnel).reply).toBe(0.4);
  });
});
