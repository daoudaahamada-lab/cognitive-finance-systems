import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { ruleAgents } from "@/server/agents";
import { sendingWindowMinutes } from "@/server/domain/schedule";
import { HOUR, MINUTE } from "@/server/domain/time";
import { FIRST_MESSAGE_DELAY, handleEvent } from "@/server/engine/events";
import { runOutreach } from "@/server/engine/outreach";
import { actionSpacing } from "@/server/engine/pace";
import type { LinkedInProvider } from "@/server/linkedin/types";
import { createCampaign, createWorkspace, db, deps, resetDb } from "./helpers";

const NOW = new Date("2026-10-05T08:00:00Z"); // Monday 10:00 in Paris

/** A workspace with a simulator account and a real (browser) account, each with an invited prospect. */
async function invitedOnBothAccounts() {
  const { workspace, account: simulated } = await createWorkspace();
  const real = await db.linkedInAccount.create({
    data: {
      workspaceId: workspace.id, provider: "browser", externalId: "br-real", fullName: "Alex Martin",
      sendingDays: [1, 2, 3, 4, 5, 6, 7], sendingStart: "00:00", sendingEnd: "00:00",
    },
  });
  const invited = async (accountId: string, externalId: string) => {
    const campaign = await createCampaign(workspace.id, accountId);
    return db.prospect.create({
      data: {
        workspaceId: workspace.id, campaignId: campaign.id, accountId, externalId,
        profileUrl: `https://www.linkedin.com/in/${externalId}`, firstName: "Camille", lastName: "Durand",
        source: "SEARCH", stage: "INVITED", invitedAt: NOW,
      },
    });
  };
  return { simulated, real, simulatedProspect: await invited(simulated.id, "sim-1"), realProspect: await invited(real.id, "real-1") };
}

describe("real LinkedIn accounts", () => {
  let previousScale: string | undefined;

  beforeEach(async () => {
    await resetDb();
    previousScale = process.env.TIME_SCALE;
  });

  afterEach(() => {
    process.env.TIME_SCALE = previousScale;
  });

  it("always wait in real time, even when TIME_SCALE speeds up the simulator", async () => {
    process.env.TIME_SCALE = "720";
    const { simulated, real, simulatedProspect, realProspect } = await invitedOnBothAccounts();

    await handleEvent(deps(NOW), simulated, { kind: "invite_accepted", profileId: simulatedProspect.externalId, at: NOW });
    await handleEvent(deps(NOW), real, { kind: "invite_accepted", profileId: realProspect.externalId, at: NOW });

    const sim = await db.prospect.findUniqueOrThrow({ where: { id: simulatedProspect.id } });
    const live = await db.prospect.findUniqueOrThrow({ where: { id: realProspect.id } });
    expect(sim.nextActionAt!.getTime() - NOW.getTime()).toBe(FIRST_MESSAGE_DELAY / 720);
    expect(live.nextActionAt!.getTime() - NOW.getTime()).toBe(FIRST_MESSAGE_DELAY);
    expect(FIRST_MESSAGE_DELAY).toBe(4 * HOUR);
  });

  it("spread invitations and messages over the sending window instead of sending bursts", async () => {
    const { workspace } = await createWorkspace();
    const account = await db.linkedInAccount.create({
      data: { workspaceId: workspace.id, provider: "browser", externalId: "br-paced", fullName: "Alex Martin", sendingStart: "09:00", sendingEnd: "18:00" },
    });
    const campaign = await createCampaign(workspace.id, account.id);
    for (let i = 0; i < 6; i++) {
      await db.prospect.create({
        data: {
          workspaceId: workspace.id, campaignId: campaign.id, accountId: account.id, externalId: `p-${i}`,
          profileUrl: `https://www.linkedin.com/in/p-${i}`, firstName: "Camille", lastName: "Durand", title: "CFO", company: "Nova",
          source: "SEARCH", ...(i < 3 ? { stage: "QUALIFIED", score: 80 } : { stage: "CONNECTED", nextActionAt: NOW }),
        },
      });
    }
    const sent: string[] = [];
    const linkedin = {
      name: "browser",
      async sendInvitation(_: unknown, profileId: string) { sent.push(`invite ${profileId}`); },
      async sendMessage(_: unknown, profileId: string) { sent.push(`message ${profileId}`); return { externalId: `m-${sent.length}` }; },
    } as unknown as LinkedInProvider;
    const at = (offset: number) => ({ db, agents: ruleAgents(), providerFor: () => linkedin, now: new Date(NOW.getTime() + offset) });

    // 09:00 to 18:00 with the default caps: an invitation every 13.5 min, a message every 5.4 min.
    expect(sendingWindowMinutes(account)).toBe(540);
    expect(actionSpacing(540, 40)).toBe(13.5 * MINUTE);

    expect(await runOutreach(at(0), account)).toMatchObject({ invites: 1, messages: 1 });
    expect(await runOutreach(at(5 * MINUTE), account)).toMatchObject({ invites: 0, messages: 0 });
    expect(await runOutreach(at(6 * MINUTE), account)).toMatchObject({ invites: 0, messages: 1 });
    expect(await runOutreach(at(14 * MINUTE), account)).toMatchObject({ invites: 1, messages: 1 });
    expect(sent).toHaveLength(5);
  });

  it("read an imported profile before writing the invitation note", async () => {
    const { workspace } = await createWorkspace();
    const account = await db.linkedInAccount.create({
      data: { workspaceId: workspace.id, provider: "browser", externalId: "br-import", fullName: "Alex Martin", sendingDays: [1, 2, 3, 4, 5, 6, 7], sendingStart: "00:00", sendingEnd: "00:00" },
    });
    const campaign = await createCampaign(workspace.id, account.id, { sources: [] });
    // Imported from linkedin.com/in/jdupont: the URL is all we know.
    const prospect = await db.prospect.create({
      data: {
        workspaceId: workspace.id, campaignId: campaign.id, accountId: account.id, externalId: "jdupont",
        profileUrl: "https://www.linkedin.com/in/jdupont", firstName: "Jdupont", lastName: "", source: "IMPORT", stage: "QUALIFIED", score: 10,
      },
    });
    const notes: (string | null)[] = [];
    const linkedin = {
      name: "browser",
      async enrichProfile() { return { firstName: "Jean", lastName: "Dupont", headline: "CFO chez Nova", title: "CFO", company: "Nova" }; },
      async sendInvitation(_: unknown, __: string, note: string | null) { notes.push(note); },
    } as unknown as LinkedInProvider;

    await runOutreach({ db, agents: ruleAgents(), providerFor: () => linkedin, now: NOW }, account);

    expect(notes).toEqual(["Bonjour Jean, ravi d'échanger avec vous."]);
    expect(await db.prospect.findUniqueOrThrow({ where: { id: prospect.id } })).toMatchObject({ firstName: "Jean", lastName: "Dupont", title: "CFO", company: "Nova", stage: "INVITED" });
  });
});
