import { createHash } from "node:crypto";
import type { ProviderProfile } from "../types";

export function slugFromProfileUrl(url: string): string | null {
  const match = /\/in\/([^/?#]+)/i.exec(url);
  if (!match) return null;
  try {
    return decodeURIComponent(match[1]!).toLowerCase();
  } catch {
    return match[1]!.toLowerCase();
  }
}

export function profileUrl(baseUrl: string, slug: string): string {
  return `${baseUrl}/in/${encodeURIComponent(slug)}/`;
}

/** "Jean Dupont, CFA 🚀" → { firstName: "Jean", lastName: "Dupont" } */
export function splitName(full: string): { firstName: string; lastName: string } {
  const cleaned = full
    .split(",")[0]!
    .replace(/[^\p{L}\p{M}'’\- ]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
  const [first = "", ...rest] = cleaned.split(" ");
  return { firstName: first, lastName: rest.join(" ") };
}

/** "CFO chez Nova | SaaS" → { title: "CFO", company: "Nova" } */
export function splitHeadline(headline: string): { title: string; company: string } {
  const first = headline.split(/\s[|•]\s/)[0]!.trim();
  const at = /^(.+?)\s+(?:chez|at|@|-)\s+(.+)$/i.exec(first);
  if (at) return { title: at[1]!.trim(), company: at[2]!.trim() };
  return { title: first, company: "" };
}

const NOISE = [
  /^[•·]?\s*(1er|2e|3e( et \+)?|1st|2nd|3rd\+?)(\s+degree connection)?$/i,
  /^(relation de|connection of) /i,
  /^(voir le profil|view .+profile)/i,
  /^(se connecter|connect|message|suivre|follow|en attente|pending|envoyer un message)$/i,
  /^(statut|status)\s*:/i,
  /^\d+\s+(relations? en commun|mutual connections?)/i,
  /^(actuellement|current|passé|past)\s*:/i,
];

/** Screen-reader text LinkedIn appends to links ("Voir le profil de …", "View …’s profile"). */
const SCREEN_READER = /(voir le profil de|view)\s.*$/i;

export function cleanLines(text: string): string[] {
  const seen = new Set<string>();
  return text
    .split("\n")
    .map((l) => l.replace(SCREEN_READER, "").replace(/\s+/g, " ").trim())
    .filter((l) => l.length > 0 && !NOISE.some((re) => re.test(l)))
    .filter((l) => (seen.has(l) ? false : (seen.add(l), true)));
}

export type RawCard = { slug: string; anchorText: string; text: string };

/** Turns a result card (search, reactions, visitors) into a profile; missing fields stay empty. */
export function profileFromCard(baseUrl: string, card: RawCard, extra: Pick<ProviderProfile, "signal" | "signalDetail"> = { signal: null, signalDetail: null }): ProviderProfile {
  const lines = cleanLines(card.text);
  const anchorName = cleanLines(card.anchorText)[0] ?? "";
  const nameLine = anchorName || lines[0] || card.slug;
  const rest = lines.filter((l) => l !== nameLine);
  const headline = rest[0] ?? "";
  const location = rest[1] && rest[1].length < 60 ? rest[1] : "";
  const { firstName, lastName } = splitName(nameLine);
  const { title, company } = splitHeadline(headline);
  return {
    externalId: card.slug,
    profileUrl: profileUrl(baseUrl, card.slug),
    firstName: firstName || card.slug,
    lastName,
    headline,
    title,
    company,
    companySize: "",
    industry: "",
    location,
    ...extra,
  };
}

/** Profile known only by its URL (list import): the name is guessed from the slug. */
export function profileFromSlug(baseUrl: string, slug: string): ProviderProfile {
  const words = slug.split("-").filter((w) => w && !/\d/.test(w));
  const cap = (w: string) => w.charAt(0).toUpperCase() + w.slice(1);
  return {
    externalId: slug,
    profileUrl: profileUrl(baseUrl, slug),
    firstName: words[0] ? cap(words[0]) : slug,
    lastName: words.slice(1).map(cap).join(" "),
    headline: "",
    title: "",
    company: "",
    companySize: "",
    industry: "",
    location: "",
    signal: null,
    signalDetail: null,
  };
}

/** Stable id for a message seen in a thread: the same text from the same person yields the same id. */
export function messageId(slug: string, text: string, occurrence: number): string {
  return `li-${createHash("sha1").update(`${slug}\u0000${text.trim()}\u0000${occurrence}`).digest("hex").slice(0, 24)}`;
}

/**
 * Inbound messages after the last outbound one: what is still waiting for an answer.
 * Older history (before our last message) is never replayed as new replies.
 */
export function unansweredTail<T extends { outbound: boolean }>(messages: T[]): T[] {
  let lastOutbound = -1;
  messages.forEach((m, i) => {
    if (m.outbound) lastOutbound = i;
  });
  return messages.slice(lastOutbound + 1).filter((m) => !m.outbound);
}

/** Builds a people search from targeting when no search URL was given. */
export function buildSearchUrl(baseUrl: string, query: { titles: string[]; keywords: string[]; locations: string[] }): string {
  const group = (terms: string[]) => (terms.length === 0 ? null : terms.length === 1 ? `"${terms[0]}"` : `(${terms.map((t) => `"${t}"`).join(" OR ")})`);
  const parts = [group(query.titles), group(query.keywords), group(query.locations)].filter(Boolean);
  const url = new URL(`${baseUrl}/search/results/people/`);
  if (parts.length > 0) url.searchParams.set("keywords", parts.join(" AND "));
  url.searchParams.set("origin", "GLOBAL_SEARCH_HEADER");
  return url.toString();
}

export function withPage(url: string, page: number): string {
  const u = new URL(url);
  u.searchParams.set("page", String(page));
  return u.toString();
}
