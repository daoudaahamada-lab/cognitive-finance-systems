import type { Agents } from "@/server/agents";
import { defaultAgents } from "@/server/agents";
import { db as defaultDb, type Db } from "@/server/db";
import { getProvider } from "@/server/linkedin";
import type { LinkedInProvider } from "@/server/linkedin/types";

export type EngineDeps = {
  db: Db;
  agents: Agents;
  /** Provider for an account's `provider` column. */
  providerFor: (name: string) => LinkedInProvider;
  now: Date;
};

export function engineDeps(overrides: Partial<EngineDeps> = {}): EngineDeps {
  const db = overrides.db ?? defaultDb;
  return {
    db,
    agents: overrides.agents ?? defaultAgents(),
    providerFor: overrides.providerFor ?? ((name) => getProvider(db, name)),
    now: overrides.now ?? new Date(),
  };
}
