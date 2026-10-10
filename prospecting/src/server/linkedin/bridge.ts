import { createHash, timingSafeEqual } from "node:crypto";
import { createServer, type Server } from "node:http";
import { browserConfig } from "./browser/config";
import { profileFromSlug, slugFromProfileUrl } from "./browser/parse";
import {
  ProviderActionError,
  ProviderAuthError,
  ProviderLimitError,
  type AccountRef,
  type ActionErrorCode,
  type ConnectAccountInput,
  type ConnectedAccount,
  type LinkedInProvider,
  type ProfileUpdate,
  type ProviderEvent,
  type SearchQuery,
} from "./types";

/**
 * Only the worker drives browsers (a Chromium profile can be opened by one process).
 * The web app reaches it through this local bridge: same LinkedInProvider contract, over HTTP on 127.0.0.1.
 */
const METHODS = ["connectAccount", "updateSession", "search", "sendInvitation", "sendMessage", "fetchEvents"] as const;
type Method = (typeof METHODS)[number];

/** Methods whose last argument is the engine's `now`. */
const DATED: Method[] = ["sendInvitation", "sendMessage", "fetchEvents"];

export function bridgeConfig() {
  return {
    port: Number(process.env.LINKEDIN_BRIDGE_PORT ?? "4319"),
    // Both processes share DATABASE_URL, so a secret derived from it works without extra setup.
    secret: process.env.LINKEDIN_BRIDGE_SECRET || createHash("sha256").update(`vela-bridge:${process.env.DATABASE_URL ?? ""}`).digest("hex"),
  };
}

type WireError = { kind: "auth" | "limit" | "action" | "error"; code?: ActionErrorCode; message: string };

function toWire(error: unknown): WireError {
  if (error instanceof ProviderAuthError) return { kind: "auth", message: error.message };
  if (error instanceof ProviderLimitError) return { kind: "limit", message: error.message };
  if (error instanceof ProviderActionError) return { kind: "action", code: error.code, message: error.message };
  return { kind: "error", message: error instanceof Error ? error.message : String(error) };
}

function fromWire(error: WireError): Error {
  if (error.kind === "auth") return new ProviderAuthError(error.message);
  if (error.kind === "limit") return new ProviderLimitError(error.message);
  if (error.kind === "action") return new ProviderActionError(error.code ?? "UNEXPECTED_PAGE", error.message);
  return new Error(`Worker LinkedIn : ${error.message}`);
}

function sameSecret(given: string | undefined, expected: string): boolean {
  if (!given) return false;
  const a = Buffer.from(given);
  const b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}

/** Started by the worker: serves its local provider to the web app. */
export function startBridge(provider: LinkedInProvider, config = bridgeConfig()): Promise<Server> {
  const server = createServer((req, res) => {
    const reply = (status: number, body: unknown) => {
      res.writeHead(status, { "content-type": "application/json" });
      res.end(JSON.stringify(body));
    };
    if (req.method !== "POST" || req.url !== "/rpc") return reply(404, { error: { kind: "error", message: "not found" } });
    if (!sameSecret(req.headers["x-vela-bridge"] as string | undefined, config.secret)) return reply(401, { error: { kind: "error", message: "unauthorized" } });
    let raw = "";
    // Decode as a stream so accented characters split across chunks stay intact.
    req.setEncoding("utf8");
    req.on("data", (chunk: string) => {
      raw += chunk;
      if (raw.length > 1_000_000) req.destroy();
    });
    req.on("end", async () => {
      try {
        const { method, args } = JSON.parse(raw) as { method: Method; args: unknown[] };
        const fn = METHODS.includes(method) ? (provider[method] as ((...a: unknown[]) => Promise<unknown>) | undefined) : undefined;
        if (!fn) return reply(400, { error: { kind: "error", message: `unknown method ${method}` } });
        if (DATED.includes(method)) args[args.length - 1] = new Date(args[args.length - 1] as string);
        reply(200, { result: (await fn.apply(provider, args)) ?? null });
      } catch (error) {
        reply(200, { error: toWire(error) });
      }
    });
  });
  return new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(config.port, "127.0.0.1", () => resolve(server));
  });
}

/** Used outside the worker: forwards every browser action to it. */
export class RemoteBrowserProvider implements LinkedInProvider {
  readonly name = "browser";

  constructor(private readonly config = bridgeConfig()) {}

  private async call<T>(method: Method, args: unknown[]): Promise<T> {
    let response: Response;
    try {
      response = await fetch(`http://127.0.0.1:${this.config.port}/rpc`, {
        method: "POST",
        headers: { "content-type": "application/json", "x-vela-bridge": this.config.secret },
        body: JSON.stringify({ method, args }),
      });
    } catch {
      throw new ProviderActionError("WORKER_UNAVAILABLE", "le worker LinkedIn ne répond pas : lancez `npm run worker`");
    }
    const body = (await response.json().catch(() => ({ error: { kind: "error", message: `HTTP ${response.status}` } }))) as { result?: T; error?: WireError };
    if (body.error) throw fromWire(body.error);
    return body.result as T;
  }

  connectAccount(input: ConnectAccountInput) {
    return this.call<ConnectedAccount>("connectAccount", [input]);
  }

  updateSession(account: AccountRef, sessionCookie: string) {
    return this.call<ConnectedAccount>("updateSession", [account, sessionCookie]);
  }

  search(account: AccountRef, query: SearchQuery, cursor: string | null, limit: number) {
    return this.call<Awaited<ReturnType<LinkedInProvider["search"]>>>("search", [account, query, cursor, limit]);
  }

  /** No browser needed: imported URLs are parsed here. */
  async lookupProfiles(_account: AccountRef, profileUrls: string[]) {
    const base = browserConfig.baseUrl();
    return profileUrls.map(slugFromProfileUrl).filter((s): s is string => Boolean(s)).map((slug) => profileFromSlug(base, slug));
  }

  sendInvitation(account: AccountRef, profileId: string, note: string | null, now: Date) {
    return this.call<ProfileUpdate | null>("sendInvitation", [account, profileId, note, now]).then((r) => r ?? undefined);
  }

  sendMessage(account: AccountRef, profileId: string, text: string, now: Date) {
    return this.call<{ externalId: string }>("sendMessage", [account, profileId, text, now]);
  }

  async fetchEvents(account: AccountRef, now: Date): Promise<ProviderEvent[]> {
    const events = await this.call<ProviderEvent[]>("fetchEvents", [account, now]);
    return events.map((e) => ({ ...e, at: new Date(e.at), ...("startsAt" in e ? { startsAt: new Date(e.startsAt) } : {}) }) as ProviderEvent);
  }
}
