import { existsSync } from "node:fs";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { chromium as playwright } from "playwright-core";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { ruleAgents } from "@/server/agents";
import { HOUR } from "@/server/domain/time";
import { runTick } from "@/server/engine/tick";
import { BrowserProvider } from "@/server/linkedin/browser/provider";
import { ProviderActionError, ProviderAuthError, ProviderLimitError, type SearchQuery } from "@/server/linkedin/types";
import { createCampaign, db, resetDb } from "./helpers";
import { startMockLinkedIn } from "./linkedin-mock";

/** An explicit binary, a preinstalled one, or the browser from `npx playwright-core install chromium`. */
function findChromium(): string | undefined {
  const candidates = [process.env.LINKEDIN_CHROMIUM_PATH, "/opt/pw-browsers/chromium"];
  try {
    candidates.push(playwright.executablePath());
  } catch {
    // No browser downloaded for this Playwright version.
  }
  return candidates.find((candidate) => candidate && existsSync(candidate));
}
const chromium = findChromium();

let mock: Awaited<ReturnType<typeof startMockLinkedIn>>;
let provider: BrowserProvider;
let profilesDir: string;
let account: { externalId: string };

const query = (overrides: Partial<SearchQuery> = {}): SearchQuery => ({
  source: "SEARCH", titles: ["CFO", "DAF"], keywords: ["SaaS"], industries: [], locations: [], companySizes: [], signals: [], postUrls: [], ...overrides,
});
const now = () => new Date();
async function rejection(promise: Promise<unknown>) {
  try {
    await promise;
  } catch (error) {
    return error;
  }
  throw new Error("expected a rejection");
}

describe.skipIf(!chromium)("browser LinkedIn provider (against a local mock)", () => {
  beforeAll(async () => {
    mock = await startMockLinkedIn();
    profilesDir = await mkdtemp(path.join(tmpdir(), "vela-li-"));
    Object.assign(process.env, {
      LINKEDIN_BASE_URL: mock.url,
      LINKEDIN_PROFILES_DIR: profilesDir,
      LINKEDIN_PACE: "0",
      LINKEDIN_EVENTS_INTERVAL_MINUTES: "0",
      LINKEDIN_CHROMIUM_PATH: chromium,
    });
    provider = new BrowserProvider();
    const connected = await provider.connectAccount({ fullName: "", headline: "", accountType: "PREMIUM", sessionCookie: mock.state.cookie });
    account = { externalId: connected.externalId };
    expect(connected).toMatchObject({ fullName: "Alex Martin", headline: "Fondateur chez Clarity", accountType: "PREMIUM" });
  }, 60_000);

  afterAll(async () => {
    await provider?.sessions.closeAll();
    await mock?.close();
    await rm(profilesDir, { recursive: true, force: true });
  });

  it("refuses an invalid session cookie", async () => {
    const error = await rejection(new BrowserProvider().connectAccount({ fullName: "", headline: "", accountType: "FREE", sessionCookie: "wrong-cookie-wrong-cookie-wrong" }));
    expect(error).toBeInstanceOf(ProviderAuthError);
  });

  it("searches people, page by page, keeping only the person of each card", async () => {
    const page1 = await provider.search(account, query(), null, 10);
    expect(mock.state.searches[0]).toContain("keywords=%28%22CFO%22+OR+%22DAF%22%29+AND+%22SaaS%22");
    expect(page1.profiles).toHaveLength(10);
    expect(page1.nextCursor).toBe("2");
    expect(page1.profiles[0]).toMatchObject({ externalId: "prospect-1", firstName: "Camille", lastName: "Durand", headline: "CFO chez Nova 1 | SaaS", title: "CFO", company: "Nova 1", location: "Paris" });
    const slugs = page1.profiles.map((p) => p.externalId);
    expect(slugs).not.toContain("mutual-friend");
    expect(slugs).not.toContain("aside-person");

    const rest = await provider.search(account, query(), page1.nextCursor, 50);
    expect(rest.profiles.map((p) => p.externalId)).toEqual(Array.from({ length: 13 }, (_, i) => `prospect-${i + 11}`));
    expect(rest.nextCursor).toBeNull();
  });

  it("uses a search URL chosen by the user as is", async () => {
    await provider.search(account, query({ searchUrl: `${mock.url}/search/results/people/?keywords=custom&geoUrn=%5B%22105015875%22%5D` }), null, 5);
    expect(mock.state.searches.at(-1)).toContain("geoUrn=");
    expect(mock.state.searches.at(-1)).toContain("keywords=custom");
  });

  it("reads people from post reactions and profile visitors, and skips signals", async () => {
    const engagers = await provider.search(account, query({ source: "POST_ENGAGERS", postUrls: [`${mock.url}/feed/update/urn:li:activity:1/`] }), null, 20);
    expect(engagers.profiles.map((p) => p.externalId)).toEqual(["prospect-23", "in-more"]);
    expect(engagers.profiles[0]!.signal).toBe("POST_ENGAGEMENT");
    const visitors = await provider.search(account, query({ source: "PROFILE_VISITORS" }), null, 20);
    expect(visitors.profiles.map((p) => p.externalId)).toEqual(["prospect-21", "prospect-22"]);
    expect((await provider.search(account, query({ source: "SIGNALS" }), null, 20)).profiles).toEqual([]);
  });

  it("reads a profile known only by its URL, without touching it", async () => {
    expect(await provider.enrichProfile(account, "in-more")).toMatchObject({ firstName: "Paul", lastName: "Roux", title: "DAF", company: "Atlas", location: "Lyon" });
    expect(mock.state.invitations).toEqual([]);
  });

  it("sends invitations with and without a note, from the top card only", async () => {
    const details = await provider.sendInvitation(account, "prospect-1", "Bonjour Camille,\nravi d'échanger.", now());
    expect(details).toMatchObject({ title: "CFO", company: "Nova 1 | SaaS".split(" | ")[0], location: "Paris" });
    await provider.sendInvitation(account, "prospect-2", null, now());
    await provider.sendInvitation(account, "in-more", null, now());
    expect(mock.state.invitations).toEqual([
      { slug: "prospect-1", note: "Bonjour Camille,\nravi d'échanger." },
      { slug: "prospect-2", note: null },
      { slug: "in-more", note: null },
    ]);
  });

  it("reports why an invitation cannot be sent", async () => {
    const code = async (slug: string) => ((await rejection(provider.sendInvitation(account, slug, null, now()))) as ProviderActionError).code;
    expect(await code("already-pending")).toBe("ALREADY_PENDING");
    expect(await code("already-friend")).toBe("ALREADY_CONNECTED");
    expect(await code("follow-only")).toBe("CONNECT_UNAVAILABLE");
    expect(await code("email-person")).toBe("CONNECT_UNAVAILABLE");
    expect(await code("nobody-here")).toBe("PROFILE_NOT_FOUND");
    expect(await rejection(provider.sendInvitation(account, "limit-person", null, now()))).toBeInstanceOf(ProviderLimitError);
    expect(mock.state.invitations.map((i) => i.slug)).not.toContain("limit-person");
  });

  it("sends multi-line messages and refuses when there is no Message button", async () => {
    await provider.sendMessage(account, "already-friend", "Bonjour Hugo,\n\nmerci pour la connexion !", now());
    expect(mock.state.messages.at(-1)).toEqual({ slug: "already-friend", text: "Bonjour Hugo,\n\nmerci pour la connexion !" });
    const error = (await rejection(provider.sendMessage(account, "follow-only", "Bonjour", now()))) as ProviderActionError;
    expect(error.code).toBe("MESSAGE_UNAVAILABLE");
  });

  it("detects accepted invitations and new replies, without replaying old history", async () => {
    mock.accept("prospect-1");
    await provider.sendMessage(account, "prospect-1", "Merci pour la connexion Camille !", now());
    mock.reply("prospect-1", "Avec plaisir, on peut en parler ?");
    // Hugo wrote long ago, before our last message: not a new reply.
    mock.reply("already-friend", "Ancien message");
    await provider.sendMessage(account, "already-friend", "Une relance", now());

    const events = await provider.fetchEvents(account, now());
    expect(events).toContainEqual(expect.objectContaining({ kind: "invite_accepted", profileId: "prospect-1" }));
    const replies = events.filter((e) => e.kind === "message_received");
    expect(replies).toEqual([expect.objectContaining({ profileId: "prospect-1", text: "Avec plaisir, on peut en parler ?" })]);

    const again = (await provider.fetchEvents(account, now())).filter((e) => e.kind === "message_received");
    expect(again).toEqual([]);
  });

  it("raises an auth error when the session expires", async () => {
    const original = mock.state.cookie;
    mock.state.cookie = "rotated-by-linkedin-0000000000";
    try {
      expect(await rejection(provider.search(account, query(), null, 5))).toBeInstanceOf(ProviderAuthError);
    } finally {
      mock.state.cookie = original;
    }
  });

  it("runs the engine end to end: source, invite, message, reply with the setter", async () => {
    await resetDb();
    const fresh = await startMockLinkedIn();
    process.env.LINKEDIN_BASE_URL = fresh.url;
    const engineProvider = new BrowserProvider();
    try {
      const connected = await engineProvider.connectAccount({ fullName: "", headline: "", accountType: "PREMIUM", sessionCookie: fresh.state.cookie });
      const workspace = await db.workspace.create({ data: { name: "W", bookingUrl: "https://cal.example.com/alex" } });
      const li = await db.linkedInAccount.create({
        data: { workspaceId: workspace.id, provider: "browser", externalId: connected.externalId, fullName: connected.fullName, accountType: "PREMIUM", sendingDays: [1, 2, 3, 4, 5, 6, 7], sendingStart: "00:00", sendingEnd: "00:00" },
      });
      await createCampaign(workspace.id, li.id, { sources: ["SEARCH"], titles: ["CFO"], industries: [], locations: [], exclusions: [], minScore: 0, setterMode: "AUTO", inviteNote: null });
      const deps = (at: Date) => ({ db, agents: ruleAgents(), providerFor: () => engineProvider, now: at });

      let at = new Date();
      const first = await runTick(deps(at), { workspaceId: workspace.id });
      expect(first[0]?.error).toBeUndefined();
      expect(first[0]).toMatchObject({ sourced: 23 });
      expect(fresh.state.invitations).toHaveLength(1); // a real account sends one invitation at a time

      const invited = fresh.state.invitations[0]!.slug;
      fresh.accept(invited);
      at = new Date(at.getTime() + HOUR);
      await runTick(deps(at), { workspaceId: workspace.id });
      expect((await db.prospect.findFirstOrThrow({ where: { externalId: invited } })).stage).toBe("CONNECTED");

      at = new Date(at.getTime() + 5 * HOUR);
      await runTick(deps(at), { workspaceId: workspace.id });
      expect(fresh.state.messages.map((m) => m.slug)).toContain(invited);

      fresh.reply(invited, "Oui, ça m'intéresse, on peut en parler ?");
      at = new Date(at.getTime() + HOUR);
      await runTick(deps(at), { workspaceId: workspace.id });
      const answer = fresh.state.messages.filter((m) => m.slug === invited).at(-1)!;
      expect(answer.text).toContain("https://cal.example.com/demo"); // the campaign's booking link
      expect((await db.prospect.findFirstOrThrow({ where: { externalId: invited } })).stage).toBe("REPLIED");
    } finally {
      process.env.LINKEDIN_BASE_URL = mock.url;
      await engineProvider.sessions.closeAll();
      await fresh.close();
    }
  }, 120_000);
});
