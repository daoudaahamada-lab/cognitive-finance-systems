import { mkdir } from "node:fs/promises";
import path from "node:path";
import { chromium, type BrowserContext, type Page } from "playwright-core";
import { browserConfig } from "./config";

type Entry = { context: BrowserContext; page: Page; idleTimer?: NodeJS.Timeout };

/**
 * One persistent Chromium profile per LinkedIn account (cookies survive restarts),
 * one page per account, and one action at a time per account.
 */
export class BrowserSessions {
  private readonly entries = new Map<string, Promise<Entry>>();
  private readonly queues = new Map<string, Promise<unknown>>();

  profileDir(accountId: string): string {
    if (!/^[\w-]+$/.test(accountId)) throw new Error(`Invalid account id "${accountId}"`);
    return path.join(browserConfig.profilesDir(), accountId);
  }

  /** Runs `fn` with the account's page, after any action already running on that account. */
  async withPage<T>(accountId: string, fn: (page: Page) => Promise<T>): Promise<T> {
    const previous = this.queues.get(accountId) ?? Promise.resolve();
    const run = previous.catch(() => undefined).then(async () => {
      const entry = await this.entry(accountId);
      if (entry.idleTimer) clearTimeout(entry.idleTimer);
      try {
        return await fn(entry.page);
      } finally {
        entry.idleTimer = setTimeout(() => void this.close(accountId), browserConfig.idleCloseMs());
        entry.idleTimer.unref?.();
      }
    });
    this.queues.set(accountId, run);
    try {
      return await run;
    } finally {
      if (this.queues.get(accountId) === run) this.queues.delete(accountId);
    }
  }

  async setSessionCookie(accountId: string, value: string) {
    const entry = await this.entry(accountId);
    const base = new URL(browserConfig.baseUrl());
    const domain = /linkedin\.com$/i.test(base.hostname) ? ".linkedin.com" : base.hostname;
    await entry.context.clearCookies({ name: "li_at" });
    const secure = base.protocol === "https:";
    // Chromium drops SameSite=None cookies that are not Secure (plain-HTTP test servers).
    // An expiry makes it a persistent cookie: without one Chromium forgets it when the browser closes.
    const expires = Math.floor(Date.now() / 1000) + 365 * 24 * 3600;
    await entry.context.addCookies([{ name: "li_at", value: value.trim(), domain, path: "/", httpOnly: true, secure, sameSite: secure ? "None" : "Lax", expires }]);
  }

  async close(accountId: string) {
    const pending = this.entries.get(accountId);
    if (!pending) return;
    this.entries.delete(accountId);
    const entry = await pending.catch(() => null);
    if (entry?.idleTimer) clearTimeout(entry.idleTimer);
    await entry?.context.close().catch(() => undefined);
  }

  async closeAll() {
    await Promise.all([...this.entries.keys()].map((id) => this.close(id)));
  }

  private entry(accountId: string): Promise<Entry> {
    let pending = this.entries.get(accountId);
    if (!pending) {
      pending = this.launch(accountId);
      this.entries.set(accountId, pending);
      pending.catch(() => this.entries.delete(accountId));
    }
    return pending;
  }

  private async launch(accountId: string): Promise<Entry> {
    const dir = this.profileDir(accountId);
    await mkdir(dir, { recursive: true });
    const context = await chromium.launchPersistentContext(dir, {
      headless: browserConfig.headless(),
      executablePath: browserConfig.executablePath(),
      viewport: { width: 1366, height: 900 },
      locale: "fr-FR",
    });
    context.setDefaultTimeout(20_000);
    // tsx/esbuild wraps named functions in __name(...); functions sent to page.evaluate run in the
    // page, where that helper does not exist. Defining it there keeps evaluate() working under tsx.
    await context.addInitScript({ content: "globalThis.__name = globalThis.__name || ((fn) => fn);" });
    const page = context.pages()[0] ?? (await context.newPage());
    return { context, page };
  }
}
