import { randomUUID } from "node:crypto";
import type { Db } from "@/server/db";
import { createRng, hashString, pick, between, weighted, type Rng } from "@/server/domain/random";
import { DAY, HOUR, MINUTE, addScaled } from "@/server/domain/time";
import type {
  AccountRef,
  ConnectAccountInput,
  ConnectedAccount,
  LinkedInProvider,
  ProviderEvent,
  ProviderProfile,
  SearchQuery,
} from "../types";
import {
  COMPANY_PREFIXES,
  COMPANY_SIZES,
  COMPANY_SUFFIXES,
  FIRST_NAMES,
  INDUSTRIES,
  LAST_NAMES,
  LOCATIONS,
  REPLIES,
  SIGNAL_DETAILS,
  TITLES,
} from "./data";

type Intent = keyof typeof REPLIES;

/** How many people each source can surface for one query. */
const SOURCE_VOLUME = {
  SEARCH: 500,
  SIGNALS: 150,
  POST_ENGAGERS: 60,
  PROFILE_VISITORS: 40,
  IMPORT: 0,
} as const;

/** Probability that a generated field follows the campaign's targeting. */
const TARGETING_BIAS = 0.65;

const BUYING_SIGNALS = ["NEW_ROLE", "HIRING", "FUNDRAISING"];

/**
 * A stand-in for LinkedIn: it generates people, accepts some invitations, answers
 * some messages and books some meetings, all on a (scaled) human timeline.
 * State lives in the SimContact / SimEvent tables so the web app and the worker share it.
 */
export class SimulatorProvider implements LinkedInProvider {
  readonly name = "simulator";

  constructor(
    private readonly db: Db,
    /** Overrides TIME_SCALE (tests pass 1 for real-time arithmetic). */
    private readonly scale?: number,
  ) {}

  async connectAccount(input: ConnectAccountInput): Promise<ConnectedAccount> {
    return {
      externalId: `sim-acc-${randomUUID()}`,
      fullName: input.fullName,
      headline: input.headline,
      accountType: input.accountType,
    };
  }

  async search(account: AccountRef, query: SearchQuery, cursor: string | null, limit: number) {
    const volume = query.source === "POST_ENGAGERS"
      ? SOURCE_VOLUME.POST_ENGAGERS * query.postUrls.length
      : SOURCE_VOLUME[query.source];
    const start = cursor ? Number(cursor) : 0;
    const end = Math.min(start + Math.max(0, limit), volume);
    const queryKey = `${account.externalId}:${JSON.stringify(query)}`;

    const profiles: ProviderProfile[] = [];
    for (let i = start; i < end; i++) {
      const profileId = `sim-${hashString(`${queryKey}:${i}`).toString(36)}${i.toString(36)}`;
      profiles.push(generateProfile(profileId, query, i));
    }
    await this.rememberPeople(account, profiles);
    return { profiles, nextCursor: end < volume ? String(end) : null };
  }

  async lookupProfiles(account: AccountRef, profileUrls: string[]) {
    const profiles: ProviderProfile[] = [];
    for (const url of profileUrls) {
      const slug = /linkedin\.com\/in\/([^/?#]+)/i.exec(url)?.[1];
      if (!slug) continue;
      profiles.push(profileFromSlug(decodeURIComponent(slug)));
    }
    await this.rememberPeople(account, profiles);
    return profiles;
  }

  async sendInvitation(account: AccountRef, profileId: string, _note: string | null, now: Date) {
    const contact = await this.contact(account, profileId);
    const rng = createRng(`${profileId}:accept`);
    const acceptance = 0.4 + (contact.hasSignal ? 0.25 : 0);
    if (rng() < acceptance) {
      await this.schedule(account, profileId, "invite_accepted", {}, addScaled(now, between(rng, 1 * HOUR, 72 * HOUR), this.scale));
    }
  }

  async sendMessage(account: AccountRef, profileId: string, text: string, now: Date) {
    const contact = await this.contact(account, profileId);
    const updated = await this.db.simContact.update({
      where: { id: contact.id },
      data: { inboundCount: { increment: 1 } },
    });
    const rng = createRng(`${profileId}:msg:${updated.inboundCount}`);

    // Someone who is already about to answer does not schedule a second answer.
    const pending = await this.db.simEvent.count({
      where: { accountExternalId: account.externalId, profileId, deliveredAt: null, kind: { in: ["message_received", "meeting_booked"] } },
    });
    if (pending === 0 && !updated.booked) {
      await this.react(account, updated, text, rng, now);
    }
    return { externalId: `sim-msg-${randomUUID()}` };
  }

  async fetchEvents(account: AccountRef, now: Date): Promise<ProviderEvent[]> {
    const due = await this.db.simEvent.findMany({
      where: { accountExternalId: account.externalId, deliveredAt: null, dueAt: { lte: now } },
      orderBy: { dueAt: "asc" },
      take: 200,
    });
    const events: ProviderEvent[] = [];
    for (const row of due) {
      // Claim each row so concurrent callers never deliver it twice.
      const claimed = await this.db.simEvent.updateMany({
        where: { id: row.id, deliveredAt: null },
        data: { deliveredAt: now },
      });
      if (claimed.count === 0) continue;
      const payload = (row.payload ?? {}) as Record<string, string>;
      if (row.kind === "invite_accepted") {
        await this.db.simContact.updateMany({
          where: { accountExternalId: account.externalId, profileId: row.profileId },
          data: { connected: true },
        });
        events.push({ kind: "invite_accepted", profileId: row.profileId, at: row.dueAt });
      } else if (row.kind === "message_received") {
        events.push({
          kind: "message_received",
          profileId: row.profileId,
          text: payload.text ?? "",
          externalId: `sim-msg-${row.id}`,
          at: row.dueAt,
        });
      } else if (row.kind === "meeting_booked") {
        events.push({ kind: "meeting_booked", profileId: row.profileId, startsAt: new Date(payload.startsAt ?? row.dueAt), at: row.dueAt });
      }
    }
    return events;
  }

  // -------------------------------------------------------------------------

  private async react(
    account: AccountRef,
    contact: { id: string; profileId: string; hasSignal: boolean; lastIntent: string | null },
    text: string,
    rng: Rng,
    now: Date,
  ) {
    const sentLink = /https?:\/\//i.test(text);
    const last = contact.lastIntent;

    if (sentLink && (last === "INTERESTED" || last === "QUESTION" || last === "OBJECTION")) {
      if (rng() < 0.65) {
        const bookedAt = addScaled(now, between(rng, 30 * MINUTE, 12 * HOUR), this.scale);
        const startsAt = nextBusinessSlot(new Date(bookedAt.getTime() + between(rng, 1, 5) * DAY), rng);
        await this.db.simContact.update({ where: { id: contact.id }, data: { booked: true } });
        await this.schedule(account, contact.profileId, "meeting_booked", { startsAt: startsAt.toISOString() }, bookedAt);
        return;
      }
      return this.reply(account, contact, "QUESTION", rng, now);
    }

    let replyChance: number;
    let intents: Record<Intent, number>;
    if (last === null || last === "OUT_OF_OFFICE") {
      replyChance = 0.22 + (contact.hasSignal ? 0.12 : 0);
      intents = { INTERESTED: 30, QUESTION: 25, OBJECTION: 15, NOT_INTERESTED: 18, OUT_OF_OFFICE: 6, SENSITIVE: 6 };
    } else if (last === "QUESTION" || last === "OBJECTION" || last === "INTERESTED") {
      replyChance = 0.7;
      intents = { INTERESTED: 50, QUESTION: 15, OBJECTION: 10, NOT_INTERESTED: 25, OUT_OF_OFFICE: 0, SENSITIVE: 0 };
    } else {
      // NOT_INTERESTED or SENSITIVE: being contacted again annoys people.
      replyChance = 0.15;
      intents = { INTERESTED: 0, QUESTION: 0, OBJECTION: 0, NOT_INTERESTED: 0, OUT_OF_OFFICE: 0, SENSITIVE: 1 };
    }
    if (rng() >= replyChance) return;
    return this.reply(account, contact, weighted(rng, intents), rng, now);
  }

  private async reply(account: AccountRef, contact: { id: string; profileId: string }, intent: Intent, rng: Rng, now: Date) {
    await this.db.simContact.update({ where: { id: contact.id }, data: { lastIntent: intent } });
    const text = pick(rng, REPLIES[intent]!);
    await this.schedule(account, contact.profileId, "message_received", { text, intent }, addScaled(now, between(rng, 20 * MINUTE, 30 * HOUR), this.scale));
  }

  private async schedule(account: AccountRef, profileId: string, kind: string, payload: Record<string, string>, dueAt: Date) {
    await this.db.simEvent.create({
      data: { accountExternalId: account.externalId, profileId, kind, payload, dueAt },
    });
  }

  private async rememberPeople(account: AccountRef, profiles: ProviderProfile[]) {
    if (profiles.length === 0) return;
    await this.db.simContact.createMany({
      data: profiles.map((p) => ({
        accountExternalId: account.externalId,
        profileId: p.externalId,
        firstName: p.firstName,
        hasSignal: p.signal !== null,
      })),
      skipDuplicates: true,
    });
  }

  private async contact(account: AccountRef, profileId: string) {
    return this.db.simContact.upsert({
      where: { accountExternalId_profileId: { accountExternalId: account.externalId, profileId } },
      create: { accountExternalId: account.externalId, profileId, firstName: "" },
      update: {},
    });
  }
}

// ---------------------------------------------------------------------------
// Profile generation
// ---------------------------------------------------------------------------

function biased(rng: Rng, wanted: string[], pool: readonly string[]): string {
  return wanted.length > 0 && rng() < TARGETING_BIAS ? pick(rng, wanted) : pick(rng, pool);
}

function slugify(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function companyName(rng: Rng): string {
  return `${pick(rng, COMPANY_PREFIXES)} ${pick(rng, COMPANY_SUFFIXES)}`;
}

export function generateProfile(profileId: string, query: SearchQuery, index: number): ProviderProfile {
  const rng = createRng(profileId);
  const firstName = pick(rng, FIRST_NAMES);
  const lastName = pick(rng, LAST_NAMES);
  const title = biased(rng, query.titles, TITLES);
  const industry = biased(rng, query.industries, INDUSTRIES);
  const location = biased(rng, query.locations, LOCATIONS);
  const companySize = biased(rng, query.companySizes, COMPANY_SIZES);
  const company = companyName(rng);
  const keyword = query.keywords.length > 0 && rng() < 0.5 ? pick(rng, query.keywords) : null;

  let signal: string | null = null;
  let signalDetail: string | null = null;
  switch (query.source) {
    case "SIGNALS":
      signal = pick(rng, query.signals.length > 0 ? query.signals : BUYING_SIGNALS);
      break;
    case "POST_ENGAGERS":
      signal = "POST_ENGAGEMENT";
      signalDetail = `${pick(rng, SIGNAL_DETAILS.POST_ENGAGEMENT!)} : ${query.postUrls[index % Math.max(1, query.postUrls.length)] ?? ""}`;
      break;
    case "PROFILE_VISITORS":
      signal = "PROFILE_VISIT";
      break;
    default:
      if (rng() < 0.1) signal = "NEW_ROLE";
  }
  if (signal && !signalDetail) signalDetail = pick(rng, SIGNAL_DETAILS[signal] ?? [""]);

  return {
    externalId: profileId,
    profileUrl: `https://www.linkedin.com/in/${slugify(`${firstName}-${lastName}`)}-${profileId.slice(-6)}`,
    firstName,
    lastName,
    headline: keyword ? `${title} chez ${company} | ${keyword}` : `${title} chez ${company}`,
    title,
    company,
    companySize,
    industry,
    location,
    signal,
    signalDetail,
  };
}

function profileFromSlug(slug: string): ProviderProfile {
  const rng = createRng(`slug:${slug}`);
  const words = slug.split("-").filter((w) => w && !/\d/.test(w));
  const capitalize = (w: string) => w.charAt(0).toUpperCase() + w.slice(1);
  const firstName = words[0] ? capitalize(words[0]) : pick(rng, FIRST_NAMES);
  const lastName = words.length > 1 ? words.slice(1).map(capitalize).join(" ") : pick(rng, LAST_NAMES);
  const title = pick(rng, TITLES);
  const company = companyName(rng);
  return {
    externalId: `sim-in-${slug.toLowerCase()}`,
    profileUrl: `https://www.linkedin.com/in/${slug}`,
    firstName,
    lastName,
    headline: `${title} chez ${company}`,
    title,
    company,
    companySize: pick(rng, COMPANY_SIZES),
    industry: pick(rng, INDUSTRIES),
    location: pick(rng, LOCATIONS),
    signal: null,
    signalDetail: null,
  };
}

/** Rounds to a weekday at 9:00-17:00 UTC on the hour, like a real booking page would offer. */
function nextBusinessSlot(from: Date, rng: Rng): Date {
  const slot = new Date(from);
  slot.setUTCMinutes(0, 0, 0);
  slot.setUTCHours(8 + Math.floor(rng() * 8));
  while (slot.getUTCDay() === 0 || slot.getUTCDay() === 6) slot.setUTCDate(slot.getUTCDate() + 1);
  return slot;
}
