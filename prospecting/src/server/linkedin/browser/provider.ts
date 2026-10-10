import { randomUUID } from "node:crypto";
import { rm } from "node:fs/promises";
import type { Locator, Page } from "playwright-core";
import {
  ProviderActionError,
  ProviderAuthError,
  ProviderLimitError,
  type AccountRef,
  type ConnectAccountInput,
  type ConnectedAccount,
  type LinkedInProvider,
  type ProfileUpdate,
  type ProviderEvent,
  type ProviderProfile,
  type SearchQuery,
} from "../types";
import { browserConfig } from "./config";
import { browse, pause, typeHuman } from "./humanize";
import { buildSearchUrl, messageId, profileFromCard, profileFromSlug, slugFromProfileUrl, splitHeadline, splitName, unansweredTail, withPage, type RawCard } from "./parse";
import { AUTH_WALLS, CSS, LABELS, WARNINGS } from "./selectors";
import { BrowserSessions } from "./session";

/** Search pages read per call at most (10 results each). */
const MAX_PAGES_PER_CALL = 4;
const MAX_THREADS_PER_SCAN = 15;
const MAX_CONNECTIONS_PER_SCAN = 40;

type ThreadMessage = { sender: string | null; text: string };

async function firstVisible(...candidates: Locator[]): Promise<Locator | null> {
  for (const locator of candidates) {
    const count = await locator.count().catch(() => 0);
    for (let i = 0; i < count; i++) {
      const item = locator.nth(i);
      if (await item.isVisible().catch(() => false)) return item;
    }
  }
  return null;
}

async function textOf(locator: Locator): Promise<string> {
  if ((await locator.count()) === 0) return "";
  return (await locator.innerText().catch(() => "")).replace(/\s+/g, " ").trim();
}

/** First profile link of each list item (later links in a card are mutual connections, not the person). */
function cardsIn(page: Page, scope: string): Promise<RawCard[]> {
  return page.evaluate((scopeSelector) => {
    const root = document.querySelector(scopeSelector) ?? document.body;
    const slugOf = (href: string | null) => {
      const m = href ? /\/in\/([^/?#]+)/.exec(href) : null;
      if (!m) return null;
      try {
        return decodeURIComponent(m[1]!).toLowerCase();
      } catch {
        return m[1]!.toLowerCase();
      }
    };
    const out: { slug: string; anchorText: string; text: string }[] = [];
    const seen = new Set<string>();
    // Innermost list items holding a profile link (":scope" keeps the item itself from matching "li").
    const items = Array.from(root.querySelectorAll("li")).filter((li) => li.querySelector('a[href*="/in/"]') && !li.querySelector(":scope li a[href*='/in/']"));
    const anchors = items.length > 0 ? items.map((li) => li.querySelector<HTMLAnchorElement>('a[href*="/in/"]')!) : Array.from(root.querySelectorAll<HTMLAnchorElement>('a[href*="/in/"]'));
    for (const a of anchors) {
      const slug = slugOf(a.getAttribute("href"));
      if (!slug || seen.has(slug)) continue;
      seen.add(slug);
      const card = (a.closest("li") as HTMLElement | null) ?? a.parentElement ?? a;
      // The visible name sits in an aria-hidden span; the link also carries screen-reader text.
      const visibleName = a.querySelector<HTMLElement>('span[aria-hidden="true"]');
      out.push({ slug, anchorText: (visibleName ?? a).innerText ?? "", text: card.innerText ?? "" });
    }
    return out;
  }, scope);
}

/**
 * Drives the user's own LinkedIn session in Chromium, the way a person would:
 * one account per persistent profile, one action at a time, pauses between steps.
 * Only the worker process runs it; the web app talks to it through the bridge.
 */
export class BrowserProvider implements LinkedInProvider {
  readonly name = "browser";
  private readonly ownSlugs = new Map<string, string>();
  private readonly lastEventsScan = new Map<string, number>();
  private readonly seenThreads = new Map<string, Map<string, string>>();

  constructor(readonly sessions = new BrowserSessions()) {}

  // ------------------------------------------------------------------ session

  async connectAccount(input: ConnectAccountInput): Promise<ConnectedAccount> {
    if (!input.sessionCookie?.trim()) throw new ProviderAuthError("Le cookie de session LinkedIn (li_at) est requis.");
    const externalId = `br-${randomUUID()}`;
    try {
      const me = await this.useCookie(externalId, input.sessionCookie);
      return { externalId, fullName: me.name || input.fullName, headline: me.headline || input.headline, accountType: input.accountType };
    } catch (error) {
      await this.sessions.close(externalId);
      await rm(this.sessions.profileDir(externalId), { recursive: true, force: true });
      throw error;
    }
  }

  async updateSession(account: AccountRef, sessionCookie: string): Promise<ConnectedAccount> {
    const me = await this.useCookie(account.externalId, sessionCookie);
    return { externalId: account.externalId, fullName: me.name, headline: me.headline, accountType: "FREE" };
  }

  /** Opens LinkedIn with the stored session and reports who is logged in (no side effect). */
  async checkSession(account: AccountRef) {
    return this.sessions.withPage(account.externalId, (page) => this.whoAmI(account.externalId, page));
  }

  private async useCookie(accountId: string, cookie: string) {
    await this.sessions.setSessionCookie(accountId, cookie);
    this.ownSlugs.delete(accountId);
    return this.sessions.withPage(accountId, (page) => this.whoAmI(accountId, page));
  }

  private url(path: string): string {
    return /^https?:\/\//i.test(path) ? path : `${browserConfig.baseUrl()}${path}`;
  }

  private async goto(page: Page, path: string) {
    await page.goto(this.url(path), { waitUntil: "domcontentloaded" });
    await this.assertSession(page);
  }

  private async assertSession(page: Page) {
    const { pathname } = new URL(page.url());
    if (AUTH_WALLS.some((wall) => pathname.startsWith(wall))) {
      throw new ProviderAuthError("Session LinkedIn expirée ou vérification de sécurité demandée : mettez à jour le cookie du compte.");
    }
  }

  private async whoAmI(accountId: string, page: Page) {
    await this.goto(page, "/in/me/");
    await page.waitForURL((url) => /\/in\/(?!me\/?$)[^/]+/.test(url.pathname), { timeout: 15_000 }).catch(() => undefined);
    await this.assertSession(page);
    const slug = slugFromProfileUrl(page.url());
    if (!slug || slug === "me") throw new ProviderAuthError("Impossible d'ouvrir votre propre profil avec cette session LinkedIn.");
    this.ownSlugs.set(accountId, slug);
    const profile = await this.readProfile(page);
    return { slug, name: `${profile.firstName} ${profile.lastName}`.trim(), headline: profile.headline ?? "" };
  }

  private async ownSlug(accountId: string, page: Page): Promise<string> {
    return this.ownSlugs.get(accountId) ?? (await this.whoAmI(accountId, page)).slug;
  }

  // ---------------------------------------------------------------- profiles

  private async readProfile(page: Page): Promise<ProfileUpdate> {
    const h1 = page.locator("main h1").first();
    await h1.waitFor({ timeout: 15_000 });
    const { firstName, lastName } = splitName((await h1.innerText()).trim());
    const headline = await textOf(page.locator(`main ${CSS.headline}`).first());
    const location = await textOf(page.locator(`main ${CSS.location}`).first());
    return { firstName, lastName, headline, ...splitHeadline(headline), location };
  }

  private async openProfile(page: Page, slug: string) {
    await this.goto(page, `/in/${encodeURIComponent(slug)}/`);
    try {
      await page.locator("main h1").first().waitFor({ timeout: 15_000 });
    } catch {
      const body = await page.locator("body").innerText().catch(() => "");
      if (WARNINGS.notFound.test(body)) throw new ProviderActionError("PROFILE_NOT_FOUND", "profil introuvable ou indisponible");
      throw new ProviderActionError("UNEXPECTED_PAGE", "page de profil non reconnue");
    }
    await browse(page);
  }

  private topCard(page: Page): Locator {
    return page.locator("main section").filter({ has: page.locator("h1") }).first();
  }

  private async dismissDialogs(page: Page) {
    await page.keyboard.press("Escape").catch(() => undefined);
    await pause(300, 800);
  }

  private async limitWarning(page: Page): Promise<boolean> {
    const text = await page.locator('[role="dialog"], [role="alert"], .artdeco-toast-item').allInnerTexts().catch(() => []);
    return text.some((t) => WARNINGS.weeklyLimit.test(t));
  }

  // ------------------------------------------------------------------ search

  async search(account: AccountRef, query: SearchQuery, cursor: string | null, limit: number) {
    // Buying signals need data LinkedIn's own pages do not expose: nothing to fetch here.
    if (query.source === "SIGNALS" || query.source === "IMPORT" || limit <= 0) return { profiles: [], nextCursor: null };
    const base = browserConfig.baseUrl();

    return this.sessions.withPage(account.externalId, async (page) => {
      const own = await this.ownSlug(account.externalId, page);
      const keep = (cards: RawCard[]) => cards.filter((c) => c.slug !== own);

      if (query.source === "PROFILE_VISITORS") {
        await this.goto(page, "/me/profile-views/");
        await pause(1500, 3500);
        const profiles = keep(await cardsIn(page, "main")).map((c) => profileFromCard(base, c, { signal: "PROFILE_VISIT", signalDetail: null }));
        return { profiles, nextCursor: null };
      }

      if (query.source === "POST_ENGAGERS") {
        const index = cursor ? Number(cursor) : 0;
        const postUrl = query.postUrls[index];
        if (!postUrl) return { profiles: [], nextCursor: null };
        const next = index + 1 < query.postUrls.length ? String(index + 1) : null;
        await this.goto(page, postUrl);
        await pause(1500, 3500);
        const button = await firstVisible(page.getByRole("button", { name: LABELS.reactions }));
        if (!button) return { profiles: [], nextCursor: next };
        await button.click();
        const dialog = page.getByRole("dialog").last();
        await dialog.waitFor({ timeout: 10_000 }).catch(() => undefined);
        for (let i = 0; i < 4; i++) {
          await dialog.evaluate((el) => el.querySelector("ul")?.parentElement?.scrollBy(0, 2000)).catch(() => undefined);
          await pause(800, 1800);
        }
        const cards = keep(await cardsIn(page, '[role="dialog"]'));
        await this.dismissDialogs(page);
        return { profiles: cards.map((c) => profileFromCard(base, c, { signal: "POST_ENGAGEMENT", signalDetail: postUrl })), nextCursor: next };
      }

      const searchUrl = query.searchUrl && /\/search\/results\/people/.test(query.searchUrl) ? query.searchUrl : buildSearchUrl(base, query);
      let pageNumber = cursor ? Number(cursor) : 1;
      const profiles: ProviderProfile[] = [];
      for (let read = 0; read < MAX_PAGES_PER_CALL && profiles.length < limit; read++) {
        await this.goto(page, withPage(searchUrl, pageNumber));
        await page.locator("main").waitFor();
        await pause(1500, 4000);
        const cards = keep(await cardsIn(page, "main"));
        if (cards.length === 0) return { profiles, nextCursor: null };
        profiles.push(...cards.map((c) => profileFromCard(base, c)));
        pageNumber++;
      }
      return { profiles, nextCursor: String(pageNumber) };
    });
  }

  /** Imported URLs are not visited now; details are refreshed when the invitation is sent. */
  async lookupProfiles(_account: AccountRef, profileUrls: string[]) {
    const base = browserConfig.baseUrl();
    return profileUrls.map(slugFromProfileUrl).filter((s): s is string => Boolean(s)).map((slug) => profileFromSlug(base, slug));
  }

  // ----------------------------------------------------------------- actions

  async sendInvitation(account: AccountRef, profileId: string, note: string | null, _now?: Date): Promise<ProfileUpdate> {
    return this.sessions.withPage(account.externalId, async (page) => {
      await this.openProfile(page, profileId);
      const details = await this.readProfile(page);
      const card = this.topCard(page);

      if (await firstVisible(card.getByRole("button", { name: LABELS.pendingAria }), card.getByRole("button", { name: LABELS.pending }))) {
        throw new ProviderActionError("ALREADY_PENDING", "invitation déjà en attente");
      }
      let connect = await firstVisible(card.getByRole("button", { name: LABELS.connectAria }), card.getByRole("button", { name: LABELS.connect }));
      if (!connect) {
        const more = await firstVisible(card.getByRole("button", { name: LABELS.more }));
        if (more) {
          await more.click();
          await pause(500, 1200);
          connect = await firstVisible(
            card.getByRole("button", { name: LABELS.connectAria }),
            card.getByRole("menuitem", { name: LABELS.connectAria }),
            card.getByRole("button", { name: LABELS.connect }),
            card.getByRole("menuitem", { name: LABELS.connect }),
          );
          if (!connect) await this.dismissDialogs(page);
        }
      }
      if (!connect) {
        if ((await card.getByText(LABELS.firstDegree).count()) > 0) throw new ProviderActionError("ALREADY_CONNECTED", "déjà en relation");
        throw new ProviderActionError("CONNECT_UNAVAILABLE", "pas de bouton « Se connecter » sur ce profil");
      }

      await pause(600, 1500);
      await connect.click();
      const dialog = () => page.getByRole("dialog").last();
      await dialog().waitFor({ timeout: 8_000 }).catch(() => undefined);
      if (await dialog().isVisible().catch(() => false)) {
        const text = await dialog().innerText().catch(() => "");
        if (WARNINGS.weeklyLimit.test(text)) {
          await this.dismissDialogs(page);
          throw new ProviderLimitError("LinkedIn signale la limite d'invitations.");
        }
        if (WARNINGS.emailRequired.test(text)) {
          await this.dismissDialogs(page);
          throw new ProviderActionError("CONNECT_UNAVAILABLE", "LinkedIn demande l'adresse e-mail de la personne");
        }
        let sent = false;
        if (note) {
          const add = await firstVisible(dialog().getByRole("button", { name: LABELS.addNote }));
          if (add) {
            await add.click();
            await pause(500, 1200);
            const box = dialog().locator("textarea").first();
            if (await box.isVisible().catch(() => false)) {
              await typeHuman(page, box, note);
              const send = await firstVisible(dialog().getByRole("button", { name: LABELS.sendInvitation }));
              if (send && (await send.isEnabled())) {
                await send.click();
                sent = true;
              }
            }
          }
        }
        if (!sent) {
          // No note, or notes not available on this account (Premium upsell): send without one.
          const plain = await firstVisible(dialog().getByRole("button", { name: LABELS.sendWithoutNote }), dialog().getByRole("button", { name: LABELS.sendInvitation }));
          if (!plain) {
            await this.dismissDialogs(page);
            throw new ProviderActionError("UNEXPECTED_PAGE", "fenêtre d'invitation non reconnue");
          }
          await plain.click();
        }
        await dialog().waitFor({ state: "hidden", timeout: 10_000 }).catch(() => undefined);
      }
      await pause(1000, 2500);
      if (await this.limitWarning(page)) throw new ProviderLimitError("LinkedIn signale la limite d'invitations.");
      return details;
    });
  }

  async sendMessage(account: AccountRef, profileId: string, text: string, _now?: Date) {
    return this.sessions.withPage(account.externalId, async (page) => {
      await this.openProfile(page, profileId);
      const card = this.topCard(page);
      const button = await firstVisible(
        card.getByRole("button", { name: LABELS.messageAria }),
        card.getByRole("button", { name: LABELS.message }),
        card.getByRole("link", { name: LABELS.messageAria }),
        card.getByRole("link", { name: LABELS.message }),
      );
      if (!button) throw new ProviderActionError("MESSAGE_UNAVAILABLE", "pas de bouton « Message » (pas encore en relation ?)");
      await pause(500, 1500);
      await button.click();

      const composer = page.locator(CSS.composer).last();
      try {
        await composer.waitFor({ timeout: 15_000 });
      } catch {
        await this.dismissDialogs(page);
        throw new ProviderActionError("MESSAGE_UNAVAILABLE", "la fenêtre de message ne s'est pas ouverte (InMail ou restriction ?)");
      }
      // Clear any draft left in the box before typing.
      await composer.click();
      await page.keyboard.press("ControlOrMeta+A");
      await page.keyboard.press("Delete");
      await typeHuman(page, composer, text);

      const form = composer.locator("xpath=ancestor::form[1]");
      const send = await firstVisible(form.getByRole("button", { name: LABELS.send }));
      if (!send) throw new ProviderActionError("UNEXPECTED_PAGE", "bouton d'envoi introuvable");
      await send.click();
      try {
        await page.waitForFunction((el) => !(el as HTMLElement).innerText.trim(), await composer.elementHandle(), { timeout: 10_000 });
      } catch {
        throw new ProviderActionError("UNEXPECTED_PAGE", "l'envoi du message n'a pas été confirmé");
      }
      await pause(800, 2000);
      const close = await firstVisible(page.getByRole("button", { name: LABELS.closeConversation }));
      await close?.click().catch(() => undefined);
      return { externalId: `li-out-${randomUUID()}` };
    });
  }

  // -------------------------------------------------------------- diagnosis

  /**
   * Read-only check of everything the provider relies on, against the real site:
   * nothing is clicked except opening pages. Used by `npm run linkedin:check`.
   */
  async diagnose(account: AccountRef, query: SearchQuery): Promise<{ check: string; ok: boolean; detail: string }[]> {
    const report: { check: string; ok: boolean; detail: string }[] = [];
    const record = (check: string, ok: boolean, detail: string) => report.push({ check, ok, detail });
    await this.sessions.withPage(account.externalId, async (page) => {
      const me = await this.whoAmI(account.externalId, page);
      record("Session", true, `connecté en tant que ${me.name || "?"} (/in/${me.slug})`);

      const searchUrl = query.searchUrl || buildSearchUrl(browserConfig.baseUrl(), query);
      await this.goto(page, searchUrl);
      await pause(2000, 3000);
      const cards = (await cardsIn(page, "main")).filter((c) => c.slug !== me.slug);
      const sample = cards.slice(0, 3).map((c) => profileFromCard(browserConfig.baseUrl(), c));
      record("Recherche", cards.length > 0, `${cards.length} profils lus sur la première page${sample.length ? ` ; ex. ${sample.map((p) => `${p.firstName} ${p.lastName} — ${p.headline || "titre ?"}`).join(" / ")}` : ""}`);

      if (cards[0]) {
        await this.goto(page, `/in/${encodeURIComponent(cards[0].slug)}/`);
        const ok = await page.locator("main h1").first().waitFor({ timeout: 15_000 }).then(() => true, () => false);
        if (ok) {
          const details = await this.readProfile(page);
          record("Profil", Boolean(details.headline), `${details.firstName} ${details.lastName} · titre : ${details.headline || "non trouvé"} · lieu : ${details.location || "non trouvé"}`);
          const card = this.topCard(page);
          const seen = {
            "Se connecter": await firstVisible(card.getByRole("button", { name: LABELS.connectAria }), card.getByRole("button", { name: LABELS.connect })),
            "En attente": await firstVisible(card.getByRole("button", { name: LABELS.pendingAria })),
            Message: await firstVisible(card.getByRole("button", { name: LABELS.messageAria }), card.getByRole("button", { name: LABELS.message }), card.getByRole("link", { name: LABELS.message })),
            Plus: await firstVisible(card.getByRole("button", { name: LABELS.more })),
          };
          const found = Object.entries(seen).filter(([, v]) => v).map(([k]) => k);
          record("Boutons du profil", found.length > 0, found.length ? `trouvés : ${found.join(", ")}` : "aucun bouton reconnu dans l'en-tête du profil");
        } else {
          record("Profil", false, "en-tête du profil (h1) introuvable");
        }
      }

      await this.goto(page, "/mynetwork/invite-connect/connections/");
      await pause(2000, 3000);
      const connections = await cardsIn(page, "main");
      record("Relations", connections.length > 0, `${connections.length} relations lues`);

      await this.goto(page, "/messaging/");
      await pause(2000, 3000);
      const threads = await page.locator('a[href*="/messaging/thread/"]').evaluateAll((as) => as.map((a) => a.getAttribute("href")));
      record("Messagerie", threads.length > 0, `${threads.length} conversations listées`);
      if (threads[0]) {
        await this.goto(page, threads[0]);
        await pause(2000, 3000);
        const thread = await this.readThread(page, me.slug);
        record("Conversation", thread.messages.length > 0 && Boolean(thread.participant), `${thread.messages.length} messages lus, interlocuteur : ${thread.participant ?? "non trouvé"}, dont ${thread.messages.filter((m) => m.sender === me.slug).length} de vous`);
      }
    });
    return report;
  }

  // ------------------------------------------------------------------ events

  async fetchEvents(account: AccountRef, now: Date): Promise<ProviderEvent[]> {
    const id = account.externalId;
    const last = this.lastEventsScan.get(id) ?? 0;
    if (Date.now() - last < browserConfig.eventsIntervalMs()) return [];
    this.lastEventsScan.set(id, Date.now());

    return this.sessions.withPage(id, async (page) => {
      const own = await this.ownSlug(id, page);
      const events: ProviderEvent[] = [];

      // Accepted invitations show up at the top of the connections list.
      await this.goto(page, "/mynetwork/invite-connect/connections/");
      await page.locator("main").waitFor();
      await pause(1500, 3000);
      for (const card of (await cardsIn(page, "main")).slice(0, MAX_CONNECTIONS_PER_SCAN)) {
        if (card.slug !== own) events.push({ kind: "invite_accepted", profileId: card.slug, at: now });
      }

      // Conversations whose preview changed since the last scan.
      await this.goto(page, "/messaging/");
      await pause(1500, 3000);
      const threads = await page.evaluate((max) => {
        const seen = new Set<string>();
        const out: { href: string; preview: string }[] = [];
        for (const a of Array.from(document.querySelectorAll<HTMLAnchorElement>('a[href*="/messaging/thread/"]'))) {
          const href = a.getAttribute("href")!;
          if (seen.has(href)) continue;
          seen.add(href);
          out.push({ href, preview: ((a.closest("li") as HTMLElement | null) ?? a).innerText });
          if (out.length >= max) break;
        }
        return out;
      }, MAX_THREADS_PER_SCAN);

      const known = this.seenThreads.get(id) ?? new Map<string, string>();
      for (const thread of threads) {
        if (known.get(thread.href) === thread.preview) continue;
        await this.goto(page, thread.href);
        await page.locator(CSS.threadEvent).first().waitFor({ timeout: 10_000 }).catch(() => undefined);
        const { participant, messages } = await this.readThread(page, own);
        if (participant) {
          const tail = unansweredTail(messages.map((m) => ({ ...m, outbound: m.sender === own })).filter((m) => m.sender === own || m.sender === participant));
          const occurrences = new Map<string, number>();
          for (const message of tail) {
            const n = (occurrences.get(message.text) ?? 0) + 1;
            occurrences.set(message.text, n);
            events.push({ kind: "message_received", profileId: participant, text: message.text, externalId: messageId(participant, message.text, n), at: now });
          }
        }
        known.set(thread.href, thread.preview);
        await pause(1000, 2500);
      }
      this.seenThreads.set(id, known);
      return events;
    });
  }

  private async readThread(page: Page, own: string): Promise<{ participant: string | null; messages: ThreadMessage[] }> {
    return page.evaluate(
      ({ ownSlug, eventSelector, bodySelector }) => {
        const slugOf = (href: string | null) => {
          const m = href ? /\/in\/([^/?#]+)/.exec(href) : null;
          return m ? decodeURIComponent(m[1]!).toLowerCase() : null;
        };
        const messages: { sender: string | null; text: string }[] = [];
        let sender: string | null = null;
        for (const event of Array.from(document.querySelectorAll(eventSelector))) {
          const link = event.querySelector('a[href*="/in/"]');
          if (link) sender = slugOf(link.getAttribute("href"));
          for (const body of Array.from(event.querySelectorAll<HTMLElement>(bodySelector))) {
            const text = body.innerText.trim();
            if (text) messages.push({ sender, text });
          }
        }
        const slugs = Array.from(document.querySelectorAll('main a[href*="/in/"]')).map((a) => slugOf(a.getAttribute("href")));
        const participant = slugs.find((s) => s && s !== ownSlug) ?? null;
        return { participant, messages };
      },
      { ownSlug: own, eventSelector: CSS.threadEvent, bodySelector: CSS.messageBody },
    );
  }
}
