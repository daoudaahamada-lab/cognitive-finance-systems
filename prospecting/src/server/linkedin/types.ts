import type { AccountType, ProspectSource } from "@prisma/client";

/**
 * Everything the product needs from LinkedIn. The simulator implements it today;
 * a real provider (Unipile, a browser worker, ...) plugs in behind the same contract.
 */
export interface LinkedInProvider {
  readonly name: string;

  connectAccount(input: ConnectAccountInput): Promise<ConnectedAccount>;

  /** One page of people for a campaign source. `cursor` is opaque; null starts over. */
  search(
    account: AccountRef,
    query: SearchQuery,
    cursor: string | null,
    limit: number,
  ): Promise<{ profiles: ProviderProfile[]; nextCursor: string | null }>;

  /** Resolves profile URLs (list import). Unknown URLs are left out. */
  lookupProfiles(account: AccountRef, profileUrls: string[]): Promise<ProviderProfile[]>;

  /** May return fresher profile details seen while sending (title, company...). */
  sendInvitation(account: AccountRef, profileId: string, note: string | null, now: Date): Promise<ProfileUpdate | void>;

  sendMessage(account: AccountRef, profileId: string, text: string, now: Date): Promise<{ externalId: string }>;

  /** Events that happened since the previous call (each is returned once). */
  fetchEvents(account: AccountRef, now: Date): Promise<ProviderEvent[]>;

  /** Replaces the session of an existing account (new cookie). */
  updateSession?(account: AccountRef, sessionCookie: string): Promise<ConnectedAccount>;
}

/**
 * Errors a provider raises so the engine can react instead of failing the whole tick.
 */
export class ProviderAuthError extends Error {
  readonly kind = "auth";
}

/** LinkedIn warned about a limit (weekly invitations...): stop that action for a while. */
export class ProviderLimitError extends Error {
  readonly kind = "limit";
}

export type ActionErrorCode =
  | "ALREADY_CONNECTED"
  | "ALREADY_PENDING"
  | "CONNECT_UNAVAILABLE"
  | "MESSAGE_UNAVAILABLE"
  | "PROFILE_NOT_FOUND"
  | "UNEXPECTED_PAGE"
  | "WORKER_UNAVAILABLE";

/** Codes that say something about the prospect, as opposed to the session or the machine. */
export const PROSPECT_ERROR_CODES: ActionErrorCode[] = ["CONNECT_UNAVAILABLE", "MESSAGE_UNAVAILABLE", "PROFILE_NOT_FOUND"];

/** One action on one profile failed; the rest of the tick goes on. */
export class ProviderActionError extends Error {
  readonly kind = "action";
  constructor(
    readonly code: ActionErrorCode,
    message: string,
  ) {
    super(message);
  }
}

export type ProfileUpdate = Partial<Pick<ProviderProfile, "firstName" | "lastName" | "headline" | "title" | "company" | "location">>;

export type AccountRef = { externalId: string };

export type ConnectAccountInput = {
  fullName: string;
  headline: string;
  accountType: AccountType;
  /** LinkedIn session cookie (li_at) for providers that drive a real session. */
  sessionCookie?: string;
};

export type ConnectedAccount = {
  externalId: string;
  fullName: string;
  headline: string;
  accountType: AccountType;
};

export type SearchQuery = {
  source: ProspectSource;
  /** LinkedIn people-search URL chosen by the user; providers that can use it take it as is. */
  searchUrl?: string;
  titles: string[];
  keywords: string[];
  industries: string[];
  locations: string[];
  companySizes: string[];
  signals: string[];
  postUrls: string[];
};

export type ProviderProfile = {
  externalId: string;
  profileUrl: string;
  firstName: string;
  lastName: string;
  headline: string;
  title: string;
  company: string;
  companySize: string;
  industry: string;
  location: string;
  signal: string | null;
  signalDetail: string | null;
};

export type ProviderEvent =
  | { kind: "invite_accepted"; profileId: string; at: Date }
  | { kind: "message_received"; profileId: string; text: string; externalId: string; at: Date }
  | { kind: "meeting_booked"; profileId: string; startsAt: Date; at: Date };
