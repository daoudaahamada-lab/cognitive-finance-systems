import type { AddressInfo } from "node:net";
import type { Server } from "node:http";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { RemoteBrowserProvider, startBridge } from "@/server/linkedin/bridge";
import {
  ProviderActionError,
  ProviderAuthError,
  ProviderLimitError,
  type AccountRef,
  type LinkedInProvider,
  type ProviderEvent,
} from "@/server/linkedin/types";

const SECRET = "test-bridge-secret";
const account: AccountRef = { externalId: "br-1" };
const at = new Date("2026-10-12T09:30:00.000Z");

/** Stands in for the worker's browser provider: records what reaches it. */
const received: { method: string; args: unknown[] }[] = [];
const worker = {
  name: "browser",
  async sendMessage(_account: AccountRef, profileId: string, text: string, now: Date) {
    received.push({ method: "sendMessage", args: [profileId, text, now] });
    return { externalId: `out-${profileId}` };
  },
  async fetchEvents(): Promise<ProviderEvent[]> {
    return [{ kind: "message_received", profileId: "camille", text: "Ça m'intéresse, à mardi !", externalId: "m1", at }];
  },
  async enrichProfile(_account: AccountRef, profileId: string) {
    return { firstName: "Jean", lastName: "Dupont", title: profileId === "jdupont" ? "CFO" : "" };
  },
  async sendInvitation(_account: AccountRef, profileId: string) {
    if (profileId === "expired") throw new ProviderAuthError("session expirée");
    if (profileId === "limit") throw new ProviderLimitError("limite hebdomadaire");
    if (profileId === "pending") throw new ProviderActionError("ALREADY_PENDING", "déjà invité");
    return { title: "CFO" };
  },
} as unknown as LinkedInProvider;

let server: Server;
let port: number;

beforeAll(async () => {
  server = await startBridge(worker, { port: 0, secret: SECRET });
  port = (server.address() as AddressInfo).port;
});

afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));

describe("LinkedIn bridge (web app → worker)", () => {
  const remote = () => new RemoteBrowserProvider({ port, secret: SECRET });

  it("forwards actions with dates and accented text intact", async () => {
    // Hundreds of KB of multi-byte characters: some necessarily straddle the request's chunk boundaries.
    const text = `Bonjour Camille,\n${"é€".repeat(150_000)}`;
    await expect(remote().sendMessage(account, "camille", text, at)).resolves.toEqual({ externalId: "out-camille" });
    const [profileId, sentText, now] = received.at(-1)!.args as [string, string, Date];
    expect(profileId).toBe("camille");
    expect(sentText).toBe(text);
    expect(now).toBeInstanceOf(Date);
    expect(now.toISOString()).toBe(at.toISOString());

    const events = await remote().fetchEvents(account, at);
    expect(events).toMatchObject([{ kind: "message_received", text: "Ça m'intéresse, à mardi !" }]);
    expect(events[0]?.at).toBeInstanceOf(Date);
    expect(events[0]?.at.getTime()).toBe(at.getTime());
  });

  it("keeps provider errors typed so the engine can react", async () => {
    await expect(remote().enrichProfile(account, "jdupont")).resolves.toEqual({ firstName: "Jean", lastName: "Dupont", title: "CFO" });
    await expect(remote().sendInvitation(account, "anna", null, at)).resolves.toEqual({ title: "CFO" });
    await expect(remote().sendInvitation(account, "expired", null, at)).rejects.toBeInstanceOf(ProviderAuthError);
    await expect(remote().sendInvitation(account, "limit", null, at)).rejects.toBeInstanceOf(ProviderLimitError);
    const error = await remote().sendInvitation(account, "pending", null, at).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ProviderActionError);
    expect((error as ProviderActionError).code).toBe("ALREADY_PENDING");
  });

  it("refuses callers without the shared secret", async () => {
    const intruder = new RemoteBrowserProvider({ port, secret: "wrong-secret" });
    await expect(intruder.sendMessage(account, "camille", "hello", at)).rejects.toThrow(/unauthorized/);
    expect(received.filter((r) => r.args[1] === "hello")).toHaveLength(0);
  });

  it("reports a stopped worker as a retryable action error", async () => {
    const closed = await startBridge(worker, { port: 0, secret: SECRET });
    const closedPort = (closed.address() as AddressInfo).port;
    await new Promise<void>((resolve) => closed.close(() => resolve()));
    const error = await new RemoteBrowserProvider({ port: closedPort, secret: SECRET }).sendMessage(account, "camille", "hello", at).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ProviderActionError);
    expect((error as ProviderActionError).code).toBe("WORKER_UNAVAILABLE");
  });
});
