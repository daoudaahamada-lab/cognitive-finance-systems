import type { Db } from "@/server/db";
import { RemoteBrowserProvider } from "./bridge";
import { BrowserProvider } from "./browser/provider";
import { SimulatorProvider } from "./simulator/provider";
import type { LinkedInProvider } from "./types";

export type { LinkedInProvider } from "./types";

export const PROVIDERS = ["browser", "simulator"] as const;
export type ProviderName = (typeof PROVIDERS)[number];

let localBrowser: BrowserProvider | null = null;

/** The worker's own browser provider (one per process: it owns the Chromium profiles). */
export function localBrowserProvider(): BrowserProvider {
  localBrowser ??= new BrowserProvider();
  return localBrowser;
}

/** Resolves the provider that owns an account (accounts remember which provider connected them). */
export function getProvider(db: Db, name: string): LinkedInProvider {
  switch (name) {
    case "simulator":
      return new SimulatorProvider(db);
    case "browser":
      return process.env.VELA_ROLE === "worker" ? localBrowserProvider() : new RemoteBrowserProvider();
    default:
      throw new Error(`Unknown LinkedIn provider "${name}".`);
  }
}
