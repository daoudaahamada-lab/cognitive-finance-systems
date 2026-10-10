import type { AddressInfo } from "node:net";
import { describe, expect, it } from "vitest";
import { RemoteBrowserProvider, startBridge } from "@/server/linkedin/bridge";
import { buildSearchUrl, cleanLines, messageId, profileFromCard, slugFromProfileUrl, splitHeadline, splitName, unansweredTail } from "@/server/linkedin/browser/parse";
import { ProviderActionError, ProviderAuthError, ProviderLimitError, type LinkedInProvider } from "@/server/linkedin/types";

describe("LinkedIn parsing", () => {
  it("reads slugs from any profile URL", () => {
    expect(slugFromProfileUrl("https://www.linkedin.com/in/Camille-Durand-42/?miniProfileUrn=abc")).toBe("camille-durand-42");
    expect(slugFromProfileUrl("/in/l%C3%A9a-martin/")).toBe("léa-martin");
    expect(slugFromProfileUrl("https://www.linkedin.com/company/nova")).toBeNull();
  });

  it("splits names and headlines the way people write them", () => {
    expect(splitName("Jean-Luc Dupont, CFA 🚀")).toEqual({ firstName: "Jean-Luc", lastName: "Dupont" });
    expect(splitHeadline("Directeur financier chez Nova | SaaS B2B")).toEqual({ title: "Directeur financier", company: "Nova" });
    expect(splitHeadline("CFO @ Atlas")).toEqual({ title: "CFO", company: "Atlas" });
    expect(splitHeadline("Head of Sales at Orion • Ex-Google")).toEqual({ title: "Head of Sales", company: "Orion" });
    expect(splitHeadline("J'aide les PME à piloter leur trésorerie")).toEqual({ title: "J'aide les PME à piloter leur trésorerie", company: "" });
  });

  it("drops degree badges, buttons and screen-reader text from cards", () => {
    const card = profileFromCard("https://www.linkedin.com", {
      slug: "lea-martin",
      anchorText: "Léa MartinVoir le profil de Léa Martin",
      text: "Léa MartinVoir le profil de Léa Martin\n• 2e\nCFO chez Nova\nParis, Île-de-France\n3 relations en commun\nSe connecter",
    });
    expect(card).toMatchObject({ firstName: "Léa", lastName: "Martin", headline: "CFO chez Nova", title: "CFO", company: "Nova", location: "Paris, Île-de-France" });
    expect(cleanLines("Statut : en ligne\nView Léa’s profile\nMessage")).toEqual([]);
  });

  it("only treats messages after our last one as new replies", () => {
    const thread = [
      { outbound: false, text: "ancien" },
      { outbound: true, text: "notre relance" },
      { outbound: false, text: "réponse 1" },
      { outbound: false, text: "réponse 2" },
    ];
    expect(unansweredTail(thread).map((m) => m.text)).toEqual(["réponse 1", "réponse 2"]);
    expect(unansweredTail([{ outbound: true, text: "x" }])).toEqual([]);
    expect(messageId("lea", "ok", 1)).toBe(messageId("lea", "ok ", 1));
    expect(messageId("lea", "ok", 1)).not.toBe(messageId("lea", "ok", 2));
  });

  it("builds a boolean keyword search from targeting", () => {
    const url = new URL(buildSearchUrl("https://www.linkedin.com", { titles: ["CFO", "DAF"], keywords: ["SaaS"], locations: [] }));
    expect(url.pathname).toBe("/search/results/people/");
    expect(url.searchParams.get("keywords")).toBe('("CFO" OR "DAF") AND "SaaS"');
  });
});

describe("worker bridge", () => {
  const at = new Date("2026-10-12T10:00:00Z");
  const fake: LinkedInProvider = {
    name: "browser",
    connectAccount: async (input) => ({ externalId: "br-1", fullName: "Alex", headline: "", accountType: input.accountType }),
    search: async () => ({ profiles: [], nextCursor: null }),
    lookupProfiles: async () => [],
    sendInvitation: async (_a, profileId) => {
      if (profileId === "limit") throw new ProviderLimitError("limite");
      if (profileId === "auth") throw new ProviderAuthError("expirée");
      if (profileId === "gone") throw new ProviderActionError("PROFILE_NOT_FOUND", "introuvable");
      return { title: "CFO" };
    },
    sendMessage: async (_a, _p, _t, now) => ({ externalId: `sent-${now instanceof Date ? now.toISOString() : "not-a-date"}` }),
    fetchEvents: async () => [
      { kind: "invite_accepted", profileId: "lea", at },
      { kind: "meeting_booked", profileId: "lea", startsAt: at, at },
    ],
  };

  async function connect(secret = "s3cret") {
    const server = await startBridge(fake, { port: 0, secret: "s3cret" });
    const { port } = server.address() as AddressInfo;
    return { server, remote: new RemoteBrowserProvider({ port, secret }) };
  }

  it("forwards calls with dates and typed errors intact", async () => {
    const { server, remote } = await connect();
    try {
      expect(await remote.sendInvitation({ externalId: "br-1" }, "lea", null, at)).toEqual({ title: "CFO" });
      expect(await remote.sendMessage({ externalId: "br-1" }, "lea", "hi", at)).toEqual({ externalId: `sent-${at.toISOString()}` });
      const events = await remote.fetchEvents({ externalId: "br-1" }, at);
      expect(events[0]!.at).toBeInstanceOf(Date);
      expect(events[1]).toMatchObject({ kind: "meeting_booked", startsAt: at });
      await expect(remote.sendInvitation({ externalId: "br-1" }, "limit", null, at)).rejects.toBeInstanceOf(ProviderLimitError);
      await expect(remote.sendInvitation({ externalId: "br-1" }, "auth", null, at)).rejects.toBeInstanceOf(ProviderAuthError);
      await expect(remote.sendInvitation({ externalId: "br-1" }, "gone", null, at)).rejects.toMatchObject({ code: "PROFILE_NOT_FOUND" });
      expect(await remote.lookupProfiles({ externalId: "br-1" }, ["https://www.linkedin.com/in/lea-martin/", "nope"])).toHaveLength(1);
    } finally {
      server.close();
    }
  });

  it("rejects a wrong secret and reports a stopped worker", async () => {
    const { server, remote } = await connect("wrong");
    try {
      await expect(remote.connectAccount({ fullName: "", headline: "", accountType: "FREE" })).rejects.toThrow(/unauthorized/);
    } finally {
      server.close();
    }
    const down = new RemoteBrowserProvider({ port: 1, secret: "x" });
    await expect(down.sendMessage({ externalId: "br-1" }, "lea", "hi", at)).rejects.toMatchObject({ code: "WORKER_UNAVAILABLE" });
  });
});
