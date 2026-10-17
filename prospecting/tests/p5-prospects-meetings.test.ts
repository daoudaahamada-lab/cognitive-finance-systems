import type { MeetingStatus, ProspectStage } from "@prisma/client";
import { beforeEach, describe, expect, it } from "vitest";
import { dateBlock, dayLabel, formatTime, groupByDay, knownTimeZone } from "@/app/(app)/meetings/dates";
import { canLogMeeting, canSnooze, manualStageActions } from "@/app/(app)/prospects/stage-rules";
import { attentionItems } from "@/server/services/attention";
import { UserError } from "@/server/services/errors";
import { listMeetings, setMeetingStatus, showRate } from "@/server/services/meetings";
import { applyManualStage } from "@/server/services/prospects";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

const ZONE = "Europe/Paris";
const NOW = new Date("2026-10-16T14:00:00Z"); // Friday 16 October, 16:00 in Paris
const HOUR = 3_600_000;
const DAY = 86_400_000;

describe("meeting dates", () => {
  it("labels days relative to today, in the workspace time zone", () => {
    expect(dayLabel(new Date("2026-10-16T20:00:00Z"), NOW, ZONE)).toBe("Aujourd'hui");
    expect(dayLabel(new Date("2026-10-17T08:00:00Z"), NOW, ZONE)).toBe("Demain");
    expect(dayLabel(new Date("2026-10-15T08:00:00Z"), NOW, ZONE)).toBe("Hier");
    expect(dayLabel(new Date("2026-10-19T12:30:00Z"), NOW, ZONE)).toBe("lun. 19 oct.");
    expect(dayLabel(new Date("2025-10-12T08:00:00Z"), NOW, ZONE)).toBe("dim. 12 oct. 2025");
    // 22:30 UTC is already Saturday in Paris.
    expect(dayLabel(new Date("2026-10-16T22:30:00Z"), NOW, ZONE)).toBe("Demain");
    expect(dayLabel(new Date("2026-10-16T22:30:00Z"), NOW, "UTC")).toBe("Aujourd'hui");
  });

  it("formats the time and the date block, and survives an unknown zone", () => {
    expect(formatTime(new Date("2026-10-19T12:30:00Z"), ZONE)).toBe("14:30");
    expect(dateBlock(new Date("2026-10-19T12:30:00Z"), ZONE)).toEqual({ day: "19", month: "oct." });
    expect(knownTimeZone("Nowhere/Void")).toBeUndefined();
    expect(knownTimeZone(ZONE)).toBe(ZONE);
    expect(() => dayLabel(new Date("2026-10-19T12:30:00Z"), NOW, "Nowhere/Void")).not.toThrow();
  });

  it("groups consecutive items by calendar day", () => {
    const dates = ["2026-10-16T15:00:00Z", "2026-10-16T21:00:00Z", "2026-10-16T23:00:00Z", "2026-10-19T09:00:00Z"].map((d) => new Date(d));
    const groups = groupByDay(dates, (d) => d, NOW, ZONE);
    expect(groups.map((g) => [g.label, g.items.length])).toEqual([
      ["Aujourd'hui", 2],
      ["Demain", 1],
      ["lun. 19 oct.", 1],
    ]);
    expect(groups[0]!.key).toBe("2026-10-16");
    expect(groupByDay([], (d: Date) => d, NOW, ZONE)).toEqual([]);
  });
});

describe("prospect page rules", () => {
  it("offers stage buttons only where they apply", () => {
    expect(manualStageActions("NEW")).toEqual(["exclude", "not_interested"]);
    expect(manualStageActions("REPLIED")).toEqual(["not_interested"]);
    expect(manualStageActions("DISQUALIFIED")).toEqual(["requalify"]);
    // No empty band: nothing to offer once a meeting is booked or the prospect said no.
    expect(manualStageActions("MEETING_BOOKED")).toEqual([]);
    expect(manualStageActions("NOT_INTERESTED")).toEqual([]);
  });

  it("suspends sends only while the engine still has something to send", () => {
    expect(["NEW", "QUALIFIED", "INVITED", "CONNECTED", "MESSAGED"].every(canSnooze)).toBe(true);
    expect(["REPLIED", "MEETING_BOOKED", "NOT_INTERESTED", "DISQUALIFIED", "UNRESPONSIVE"].some(canSnooze)).toBe(false);
    expect(canLogMeeting("REPLIED")).toBe(true);
    expect(canLogMeeting("MEETING_BOOKED")).toBe(false);
  });

  it("offers exactly the stage changes the service accepts", async () => {
    await resetDb();
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id);
    const stages: ProspectStage[] = ["NEW", "QUALIFIED", "DISQUALIFIED", "INVITED", "CONNECTED", "MESSAGED", "REPLIED", "UNRESPONSIVE"];
    let n = 0;
    for (const stage of stages) {
      for (const action of ["exclude", "requalify"] as const) {
        n += 1;
        const prospect = await db.prospect.create({
          data: {
            workspaceId: workspace.id, campaignId: campaign.id, accountId: account.id,
            externalId: `rule-${n}`, profileUrl: `https://www.linkedin.com/in/rule-${n}`, firstName: "Léa", lastName: "Martin", source: "SEARCH", stage,
          },
        });
        const offered = manualStageActions(stage).includes(action);
        const result = applyManualStage(workspace.id, prospect.id, action);
        if (offered) await expect(result).resolves.toBeUndefined();
        else await expect(result).rejects.toBeInstanceOf(UserError);
      }
    }
  });
});

describe("meetings triage", () => {
  beforeEach(resetDb);

  async function fixture() {
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id);
    let n = 0;
    async function meeting(startsAt: Date, status: MeetingStatus = "SCHEDULED") {
      n += 1;
      const prospect = await db.prospect.create({
        data: {
          workspaceId: workspace.id, campaignId: campaign.id, accountId: account.id,
          externalId: `m${n}`, profileUrl: `https://www.linkedin.com/in/m${n}`, firstName: `Prénom${n}`, lastName: "Test",
          company: "Acme", source: "SEARCH", stage: "MEETING_BOOKED",
        },
      });
      return db.meeting.create({ data: { workspaceId: workspace.id, prospectId: prospect.id, campaignId: campaign.id, startsAt, status } });
    }
    return { workspace, meeting };
  }

  it("splits meetings into to confirm, upcoming and history, with the show rate", async () => {
    const { workspace, meeting } = await fixture();
    const pastRecent = await meeting(new Date(NOW.getTime() - 2 * HOUR));
    const pastOld = await meeting(new Date(NOW.getTime() - 5 * DAY));
    const soon = await meeting(new Date(NOW.getTime() + 2 * HOUR));
    const later = await meeting(new Date(NOW.getTime() + 3 * DAY));
    const held = await meeting(new Date(NOW.getTime() - 10 * DAY), "COMPLETED");
    const heldOld = await meeting(new Date(NOW.getTime() - 20 * DAY), "COMPLETED");
    const missed = await meeting(new Date(NOW.getTime() - 7 * DAY), "NO_SHOW");
    const canceled = await meeting(new Date(NOW.getTime() + 5 * DAY), "CANCELED");

    const result = await listMeetings(workspace.id, NOW);
    // Oldest unresolved first: it has waited longest for an answer.
    expect(result.toConfirm.map((m) => m.id)).toEqual([pastOld.id, pastRecent.id]);
    expect(result.upcoming.map((m) => m.id)).toEqual([soon.id, later.id]);
    // A canceled meeting is resolved, even when its date is still ahead.
    expect(result.history.map((m) => m.id)).toEqual([canceled.id, missed.id, held.id, heldOld.id]);
    expect(result.past.map((m) => m.id)).toEqual([canceled.id, pastRecent.id, pastOld.id, missed.id, held.id, heldOld.id]);
    expect(result.stats).toEqual({ completed: 2, noShow: 1, canceled: 1, showRate: 2 / 3 });
    expect(result.toConfirm[0]!.prospect).toMatchObject({ firstName: "Prénom2", company: "Acme" });
    expect(result.toConfirm[0]!.campaign.name).toBe("CFO PME");
  });

  it("resolves a meeting to confirm and updates the dashboard attention count", async () => {
    const { workspace, meeting } = await fixture();
    const first = await meeting(new Date(Date.now() - 2 * DAY));
    await meeting(new Date(Date.now() - DAY));
    const countToConfirm = async () => (await attentionItems(workspace.id)).find((i) => i.kind === "meetings_to_confirm")?.count ?? 0;
    expect(await countToConfirm()).toBe(2);

    await setMeetingStatus(workspace.id, first.id, "COMPLETED");

    const result = await listMeetings(workspace.id);
    expect(result.toConfirm).toHaveLength(1);
    expect(result.history.map((m) => m.id)).toEqual([first.id]);
    expect(result.stats).toMatchObject({ completed: 1, noShow: 0, showRate: 1 });
    expect(await countToConfirm()).toBe(1);
    await expect(setMeetingStatus("someone-else", first.id, "NO_SHOW")).rejects.toBeInstanceOf(UserError);
    expect((await listMeetings("someone-else")).past).toEqual([]);
  });

  it("has no show rate before any outcome", () => {
    expect(showRate(0, 0)).toBeNull();
    expect(showRate(31, 4)).toBeCloseTo(0.886, 3);
  });
});
