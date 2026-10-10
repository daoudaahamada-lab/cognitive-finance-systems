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

  sendInvitation(account: AccountRef, profileId: string, note: string | null, now: Date): Promise<void>;

  sendMessage(account: AccountRef, profileId: string, text: string, now: Date): Promise<{ externalId: string }>;

  /** Events that happened since the previous call (each is returned once). */
  fetchEvents(account: AccountRef, now: Date): Promise<ProviderEvent[]>;
}

export type AccountRef = { externalId: string };

export type ConnectAccountInput = {
  fullName: string;
  headline: string;
  accountType: AccountType;
};

export type ConnectedAccount = {
  externalId: string;
  fullName: string;
  headline: string;
  accountType: AccountType;
};

export type SearchQuery = {
  source: ProspectSource;
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
