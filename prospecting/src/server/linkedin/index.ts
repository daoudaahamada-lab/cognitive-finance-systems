import type { Db } from "@/server/db";
import { SimulatorProvider } from "./simulator/provider";
import type { LinkedInProvider } from "./types";

export type { LinkedInProvider } from "./types";

/** Resolves the provider that owns an account (accounts remember which provider connected them). */
export function getProvider(db: Db, name: string = process.env.LINKEDIN_PROVIDER ?? "simulator"): LinkedInProvider {
  switch (name) {
    case "simulator":
      return new SimulatorProvider(db);
    default:
      throw new Error(`Unknown LinkedIn provider "${name}". Only "simulator" ships in this version.`);
  }
}
