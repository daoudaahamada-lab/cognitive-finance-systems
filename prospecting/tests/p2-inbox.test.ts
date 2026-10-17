import { beforeEach, describe, expect, it } from "vitest";
import { insertAt, nextBusinessDayAt10 } from "@/app/(app)/inbox/compose";
import { formatCompactTime } from "@/app/(app)/inbox/format";
import { afterActionUrl, doneMessage, foldSequence, parseTab, threadNavigation } from "@/app/(app)/inbox/navigation";
import { UserError } from "@/server/services/errors";
import {
  approveDraft,
  closeAsNotInterested,
  getThread,
  hasLaunchedCampaign,
  inboxCounts,
  listConversations,
  logMeeting,
  oldestConversationId,
  rejectDraft,
} from "@/server/services/inbox";
import { listMeetings } from "@/server/services/meetings";
import { createCampaign, createWorkspace, db, resetDb } from "./helpers";

describe("inbox helpers", () => {
  const now = new Date("2026-10-16T14:00:00Z");
  const zone = "Europe/Paris";

  it("writes compact times for the conversation list", () => {
    expect(formatCompactTime(new Date(now.getTime() - 20_000), now, zone)).toBe("à l'instant");
    expect(formatCompactTime(new Date(now.getTime() - 59 * 60_000), now, zone)).toBe("59 min");
    expect(formatCompactTime(new Date(now.getTime() - 11 * 3_600_000), now, zone)).toBe("11 h");
    expect(formatCompactTime(new Date("2026-10-15T08:00:00Z"), now, zone)).toBe("hier");
    expect(formatCompactTime(new Date("2026-10-12T08:00:00Z"), now, zone)).toBe("12 oct.");
    expect(formatCompactTime(new Date("2025-10-12T08:00:00Z"), now, zone)).toBe("12 oct. 2025");
    expect(formatCompactTime(null, now, zone)).toBe("—");
    // An unknown zone falls back to the runtime's instead of throwing.
    expect(formatCompactTime(new Date("2026-10-12T08:00:00Z"), now, "Nowhere/Void")).toMatch(/oct\./);
  });

  it("locates the thread and picks the next one after an action", () => {
    const ids = ["a", "b", "c"];
    expect(threadNavigation(ids, "b")).toEqual({ position: 2, prevId: "a", nextId: "c", afterId: "c" });
    // The last thread wraps to the newest other one; manual paging does not wrap.
    expect(threadNavigation(ids, "c")).toEqual({ position: 3, prevId: "b", nextId: null, afterId: "a" });
    expect(threadNavigation(["c"], "c")).toEqual({ position: 1, prevId: null, nextId: null, afterId: null });
    // A thread outside the list (search, other tab) moves on to the first one.
    expect(threadNavigation(ids, "z")).toMatchObject({ position: 0, afterId: "a" });
  });

  it("keeps the tab and search when moving on after an action", () => {
    const form = new FormData();
    form.set("tab", "drafts");
    form.set("q", " Dupont ");
    form.set("next", "conv_2");
    form.set("name", "Alexandre");
    expect(afterActionUrl(form, "sent")).toBe("/inbox?tab=drafts&q=Dupont&c=conv_2&done=Alexandre&did=sent");

    const last = new FormData();
    last.set("tab", "nope");
    last.set("next", "");
    last.set("name", "Léa");
    expect(afterActionUrl(last, "handled")).toBe("/inbox?tab=todo&done=L%C3%A9a&did=handled");
    // Forms that do not come from the inbox page (no tab field) do not redirect.
    expect(afterActionUrl(new FormData(), "sent")).toBeNull();
    expect(parseTab("ai")).toBe("ai");
    expect(doneMessage("sent", "Alexandre")).toBe("Réponse envoyée à Alexandre");
    expect(doneMessage("not_interested", "Léa")).toContain("Pas intéressé");
  });

  it("folds the older sequence messages only past three of them", () => {
    const seq = (n: number) => Array.from({ length: n }, (_, i) => ({ id: `s${i}`, author: "SEQUENCE" }));
    const reply = { id: "r", author: "PROSPECT" };
    expect(foldSequence([...seq(3), reply]).folded).toHaveLength(0);
    const folded = foldSequence([...seq(4), reply, { id: "ai", author: "AI" }]);
    expect(folded.folded.map((m) => m.id)).toEqual(["s0", "s1", "s2"]);
    expect(folded.visible.map((m) => m.id)).toEqual(["s3", "r", "ai"]);
  });

  it("inserts chips at the cursor with sensible spacing", () => {
    expect(insertAt("Bonjour ,", 8, 8, "Alexandre")).toEqual({ value: "Bonjour Alexandre,", caret: 17 });
    expect(insertAt("Bonjour", 7, 7, "Alexandre")).toEqual({ value: "Bonjour Alexandre", caret: 17 });
    expect(insertAt("", 0, 0, "https://cal.example.com")).toEqual({ value: "https://cal.example.com", caret: 23 });
    expect(insertAt("Voici le lien : X merci", 16, 17, "https://cal.example.com").value).toBe("Voici le lien : https://cal.example.com merci");
  });

  it("prefills the meeting with the next business day at 10:00", () => {
    expect(nextBusinessDayAt10(new Date(2026, 9, 14, 16, 30))).toBe("2026-10-15T10:00"); // Wednesday → Thursday
    expect(nextBusinessDayAt10(new Date(2026, 9, 16, 9, 0))).toBe("2026-10-19T10:00"); // Friday → Monday
    expect(nextBusinessDayAt10(new Date(2026, 9, 17, 9, 0))).toBe("2026-10-19T10:00"); // Saturday → Monday
    expect(nextBusinessDayAt10(new Date(2026, 11, 31, 9, 0))).toBe("2027-01-01T10:00");
  });
});

describe("inbox services", () => {
  beforeEach(resetDb);

  async function fixture(options: { campaignBookingUrl?: string } = {}) {
    const { workspace, account } = await createWorkspace();
    const campaign = await createCampaign(workspace.id, account.id, {
      setterMode: "APPROVAL",
      ...(options.campaignBookingUrl === undefined ? {} : { bookingUrl: options.campaignBookingUrl }),
    });
    let n = 0;
    async function thread(input: { lastMessageAt: Date; draft?: boolean; status?: "AI_ACTIVE" | "NEEDS_HUMAN" | "HUMAN" | "CLOSED"; unread?: boolean }) {
      n += 1;
      const prospect = await db.prospect.create({
        data: {
          workspaceId: workspace.id, campaignId: campaign.id, accountId: account.id,
          externalId: `p${n}`, profileUrl: `https://www.linkedin.com/in/p${n}`, firstName: `Prénom${n}`, lastName: "Test",
          company: "Acme", source: "SEARCH", stage: "REPLIED",
        },
      });
      const conversation = await db.conversation.create({
        data: {
          workspaceId: workspace.id, prospectId: prospect.id, accountId: account.id,
          status: input.status ?? "AI_ACTIVE", unread: input.unread ?? true, lastIntent: "INTERESTED", lastMessageAt: input.lastMessageAt,
          messages: {
            create: [
              { direction: "OUTBOUND", author: "SEQUENCE", body: "Bonjour, merci d'avoir accepté.", sentAt: new Date(input.lastMessageAt.getTime() - 3_600_000) },
              { direction: "INBOUND", author: "PROSPECT", body: "Avec plaisir, dites-m'en plus.", sentAt: input.lastMessageAt },
            ],
          },
          ...(input.draft ? { drafts: { create: { body: "Voici mon lien de réservation.", intent: "INTERESTED", rationale: "Intéressé." } } } : {}),
        },
      });
      return { prospect, conversation };
    }
    return { workspace, campaign, thread };
  }

  it("lists proposed replies with their text and intent", async () => {
    const { workspace, thread } = await fixture();
    const { conversation } = await thread({ lastMessageAt: new Date("2026-10-15T10:00:00Z"), draft: true });
    const [row] = await listConversations(workspace.id, "drafts");
    expect(row!.id).toBe(conversation.id);
    expect(row!.drafts[0]).toMatchObject({ body: "Voici mon lien de réservation.", intent: "INTERESTED" });
  });

  it("offers the campaign booking link, else the workspace one", async () => {
    const withCampaignLink = await fixture({ campaignBookingUrl: "https://cal.example.com/campagne" });
    const a = await withCampaignLink.thread({ lastMessageAt: new Date() });
    expect((await getThread(withCampaignLink.workspace.id, a.conversation.id))!.bookingUrl).toBe("https://cal.example.com/campagne");

    await resetDb();
    const fallback = await fixture({ campaignBookingUrl: "" });
    const b = await fallback.thread({ lastMessageAt: new Date() });
    expect((await getThread(fallback.workspace.id, b.conversation.id))!.bookingUrl).toBe("https://cal.example.com/demo");
    expect(await getThread("someone-else", b.conversation.id)).toBeNull();
  });

  it("finds the thread waiting longest and knows when campaigns are launched", async () => {
    const { workspace, campaign, thread } = await fixture();
    const old = await thread({ lastMessageAt: new Date("2026-10-01T10:00:00Z"), status: "NEEDS_HUMAN" });
    await thread({ lastMessageAt: new Date("2026-10-10T10:00:00Z"), status: "NEEDS_HUMAN" });
    await thread({ lastMessageAt: new Date("2026-09-01T10:00:00Z"), status: "AI_ACTIVE", unread: false });
    expect(await oldestConversationId(workspace.id, "todo")).toBe(old.conversation.id);
    expect(await hasLaunchedCampaign(workspace.id)).toBe(true);
    await db.campaign.update({ where: { id: campaign.id }, data: { status: "DRAFT", launchedAt: null } });
    expect(await hasLaunchedCampaign(workspace.id)).toBe(false);
  });

  it("logs a meeting from a thread: meeting created, stage booked, thread closed, proposal dropped", async () => {
    const { workspace, thread } = await fixture();
    const { prospect, conversation } = await thread({ lastMessageAt: new Date(), draft: true });
    expect((await inboxCounts(workspace.id)).drafts).toBe(1);
    const startsAt = new Date(Date.now() + 3 * 86_400_000);

    await logMeeting(workspace.id, prospect.id, startsAt);

    const meeting = await db.meeting.findFirstOrThrow({ where: { prospectId: prospect.id } });
    expect(meeting).toMatchObject({ startsAt, origin: "manual", status: "SCHEDULED" });
    expect((await db.prospect.findUniqueOrThrow({ where: { id: prospect.id } })).stage).toBe("MEETING_BOOKED");
    expect((await db.conversation.findUniqueOrThrow({ where: { id: conversation.id } })).status).toBe("CLOSED");
    expect(await db.draft.count({ where: { conversationId: conversation.id, status: "PENDING" } })).toBe(0);
    expect(await inboxCounts(workspace.id)).toMatchObject({ todo: 0, drafts: 0 });
    expect((await listMeetings(workspace.id)).upcoming.map((m) => m.id)).toContain(meeting.id);
    await expect(logMeeting(workspace.id, prospect.id, new Date("pas une date"))).rejects.toBeInstanceOf(UserError);
  });

  it("closes a thread as not interested and drops its pending proposal", async () => {
    const { workspace, thread } = await fixture();
    const { prospect, conversation } = await thread({ lastMessageAt: new Date(), draft: true });
    const draft = await db.draft.findFirstOrThrow({ where: { conversationId: conversation.id } });

    await closeAsNotInterested(workspace.id, conversation.id);

    expect((await db.prospect.findUniqueOrThrow({ where: { id: prospect.id } })).stage).toBe("NOT_INTERESTED");
    expect((await db.conversation.findUniqueOrThrow({ where: { id: conversation.id } })).status).toBe("CLOSED");
    expect(await inboxCounts(workspace.id)).toMatchObject({ todo: 0, drafts: 0 });
    // The proposal can no longer be sent to someone who said no.
    await expect(approveDraft(workspace.id, draft.id)).rejects.toBeInstanceOf(UserError);
    await expect(closeAsNotInterested("someone-else", conversation.id)).rejects.toBeInstanceOf(UserError);
  });

  it("words a refused proposal as such", async () => {
    const { workspace, thread } = await fixture();
    const { conversation } = await thread({ lastMessageAt: new Date(), draft: true });
    const draft = await db.draft.findFirstOrThrow({ where: { conversationId: conversation.id } });
    await rejectDraft(workspace.id, draft.id);
    const after = await db.conversation.findUniqueOrThrow({ where: { id: conversation.id } });
    expect(after).toMatchObject({ status: "NEEDS_HUMAN", escalationReason: "Réponse proposée refusée : à vous de répondre." });
  });
});
