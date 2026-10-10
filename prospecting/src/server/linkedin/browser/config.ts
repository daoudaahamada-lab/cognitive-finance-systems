import path from "node:path";

/** Everything the browser provider reads from the environment, resolved at call time. */
export const browserConfig = {
  baseUrl: () => (process.env.LINKEDIN_BASE_URL ?? "https://www.linkedin.com").replace(/\/+$/, ""),
  /** One persistent Chromium profile per account lives here. */
  profilesDir: () => path.resolve(process.env.LINKEDIN_PROFILES_DIR ?? ".linkedin-profiles"),
  headless: () => process.env.LINKEDIN_HEADLESS !== "false",
  /** Optional Chromium/Chrome binary; otherwise Playwright's own (npx playwright-core install chromium). */
  executablePath: () => process.env.LINKEDIN_CHROMIUM_PATH || undefined,
  /** Multiplies every human-like pause; 0 disables them (tests). */
  pace: () => {
    const value = Number(process.env.LINKEDIN_PACE ?? "1");
    return Number.isFinite(value) && value >= 0 ? value : 1;
  },
  /** Minimum time between two scans of connections and messages for one account. */
  eventsIntervalMs: () => Math.max(0, Number(process.env.LINKEDIN_EVENTS_INTERVAL_MINUTES ?? "15")) * 60_000,
  /** Close an account's browser after this much idle time. */
  idleCloseMs: () => 10 * 60_000,
};
