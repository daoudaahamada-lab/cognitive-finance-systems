import type { MeetingStatus, ProspectStage } from "@prisma/client";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { beforeEach, describe, expect, it } from "vitest";
import { RestoreMeetingButton } from "@/app/(app)/meetings/meeting-buttons";
import { ReasonRow } from "@/app/(app)/prospects/[id]/score-reasons";
import { snoozeControl } from "@/app/(app)/prospects/stage-rules";
import type { ScoreReason } from "@/server/agents/scorer";
import { attentionItems } from "@/server/services/attention";
import { listMeetings, setMeetingStatus } from "@/server/services/meetings";
import { applyManualStage, snoozeProspect } from "@/server/services/prospects";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

const NOW = new Date("2026-10-16T14:00:00Z");
const DAY = 86_400_000;

async function fixture() {
  const { workspace, account } = await createWorkspace();
  const campaign = await createCampaign(workspace.id, account.id);
  let n = 0;
  async function prospect(stage: ProspectStage) {
    n += 1;
    return db.prospect.create({
      data: {
        workspaceId: workspace.id, campaignId: campaign.id, accountId: account.id,
        externalId: `fix-${n}`, profileUrl: `https://www.linkedin.com/in/fix-${n}`, firstName: "Léa", lastName: `Martin${n}`, source: "SEARCH", stage,
      },
    });
  }
  async function meeting(startsAt: Date, status: MeetingStatus) {
    const p = await prospect("MEETING_BOOKED");
    return db.meeting.create({ data: { workspaceId: workspace.id, prospectId: p.id, campaignId: campaign.id, startsAt, status } });
  }
  return { workspace, prospect, meeting };
}

describe("prospect page: 'Suspendre les envois'", () => {
  beforeEach(resetDb);

  it("shows only where sends can be suspended, even when a snooze is running", () => {
    const later = new Date(NOW.getTime() + 7 * DAY);
    const earlier = new Date(NOW.getTime() - DAY);
    expect(snoozeControl("MEETING_BOOKED", later, NOW)).toBeNull();
    expect(snoozeControl("REPLIED", later, NOW)).toBeNull();
    expect(snoozeControl("NOT_INTERESTED", null, NOW)).toBeNull();
    expect(snoozeControl("QUALIFIED", later, NOW)).toEqual({ until: later });
    // An expired snooze reads as no snooze: no 'Envois suspendus jusqu'au …', no 'Reprendre maintenant'.
    expect(snoozeControl("MESSAGED", earlier, NOW)).toEqual({ until: null });
    expect(snoozeControl("NEW", null, NOW)).toEqual({ until: null });
  });

  it("hides a snooze left on a booked prospect and brings it back after 'Requalifier'", async () => {
    const { workspace, prospect } = await fixture();
    const booked = await prospect("MEETING_BOOKED");
    // MCP snooze_prospect can still snooze any stage.
    await snoozeProspect(workspace.id, booked.id, 7);
    const bookedNow = await db.prospect.findUniqueOrThrow({ where: { id: booked.id } });
    expect(bookedNow.snoozedUntil).not.toBeNull();
    expect(snoozeControl(bookedNow.stage, bookedNow.snoozedUntil, new Date())).toBeNull();

    const excluded = await prospect("DISQUALIFIED");
    await snoozeProspect(workspace.id, excluded.id, 3);
    let row = await db.prospect.findUniqueOrThrow({ where: { id: excluded.id } });
    expect(snoozeControl(row.stage, row.snoozedUntil, new Date())).toBeNull();

    await applyManualStage(workspace.id, excluded.id, "requalify");
    row = await db.prospect.findUniqueOrThrow({ where: { id: excluded.id } });
    expect(row.stage).toBe("QUALIFIED");
    expect(snoozeControl(row.stage, row.snoozedUntil, new Date())).toEqual({ until: row.snoozedUntil });

    // 'Reprendre maintenant' (0 days) clears it; the durations stay offered.
    await snoozeProspect(workspace.id, excluded.id, 0);
    row = await db.prospect.findUniqueOrThrow({ where: { id: excluded.id } });
    expect(snoozeControl(row.stage, row.snoozedUntil, new Date())).toEqual({ until: null });
  });
});

describe("prospect page: score breakdown bar", () => {
  const render = (reason: ScoreReason) => renderToStaticMarkup(createElement("ul", null, createElement(ReasonRow, { reason })));
  const track = (html: string) => /<span aria-hidden="true" class="([^"]*)">/.exec(html)?.[1] ?? "";
  const fill = (html: string) => /<span class="(block h-full[^"]*)" style="width:([^"]*)"/.exec(html)?.slice(1) ?? [];

  it("darkens the whole track for a criterion worth nothing, which an empty fill could not show", () => {
    for (const points of [0, -5]) {
      const html = render({ label: "Taille d'entreprise", points, max: 20 });
      expect(track(html)).toContain("bg-line-strong");
      expect(track(html)).not.toContain("bg-surface-2");
      expect(html).toContain(`${points} / 20`);
    }
  });

  it("fills a partial criterion in brand and a full one in success, on the pale track", () => {
    const half = render({ label: "Secteur", points: 10, max: 20 });
    expect(track(half)).toContain("bg-surface-2");
    expect(track(half)).not.toContain("bg-line-strong");
    expect(fill(half)).toEqual([expect.stringContaining("bg-brand-600"), "50%"]);

    const full = render({ label: "Poste", points: 30, max: 30 });
    expect(fill(full)).toEqual([expect.stringContaining("bg-success"), "100%"]);
  });

  it("keeps the favourable or unfavourable reading for AI reasons without a scale", () => {
    expect(render({ label: "Budget probable", points: 1, max: 0 })).toContain("Favorable");
    expect(render({ label: "Hors cible", points: 0, max: 0 })).toContain("Défavorable");
  });
});

describe("meetings: 'Rétablir' a canceled meeting", () => {
  beforeEach(resetDb);

  it("brings it back to 'À confirmer' when passed, or 'À venir' when ahead", async () => {
    const { workspace, meeting } = await fixture();
    const now = new Date();
    const passed = await meeting(new Date(now.getTime() - 2 * DAY), "CANCELED");
    const ahead = await meeting(new Date(now.getTime() + 2 * DAY), "CANCELED");
    const countToConfirm = async () => (await attentionItems(workspace.id)).find((i) => i.kind === "meetings_to_confirm")?.count ?? 0;

    let result = await listMeetings(workspace.id, now);
    expect(result.history.map((m) => m.status)).toEqual(["CANCELED", "CANCELED"]);
    expect(await countToConfirm()).toBe(0);

    // What the button sends: meetingStatusAction(meetingId, "SCHEDULED").
    await setMeetingStatus(workspace.id, passed.id, "SCHEDULED");
    await setMeetingStatus(workspace.id, ahead.id, "SCHEDULED");

    result = await listMeetings(workspace.id, now);
    expect(result.toConfirm.map((m) => m.id)).toEqual([passed.id]);
    expect(result.upcoming.map((m) => m.id)).toEqual([ahead.id]);
    expect(result.history).toEqual([]);
    expect(result.stats.canceled).toBe(0);
    expect(await countToConfirm()).toBe(1);
  });

  it("names the button after its visible label and the prospect", () => {
    const html = renderToStaticMarkup(createElement(RestoreMeetingButton, { meetingId: "m1", name: "Léa Martin" }));
    expect(html).toContain('aria-label="Rétablir – Léa Martin"');
    expect(html).toMatch(/<\/svg> Rétablir<\/button>/);
  });
});
