/**
 * Background worker: runs the prospecting engine on a fixed interval and owns the
 * LinkedIn browsers (the web app reaches them through the local bridge).
 *   npm run worker
 */
export {};

// Set before anything resolves a provider: this process owns the browsers.
process.env.VELA_ROLE = "worker";

const { db } = await import("@/server/db");
const { engineDeps } = await import("@/server/engine/deps");
const { runTick } = await import("@/server/engine/tick");
const { localBrowserProvider } = await import("@/server/linkedin");
const { bridgeConfig, startBridge } = await import("@/server/linkedin/bridge");

const intervalMs = Math.max(1, Number(process.env.WORKER_INTERVAL_SECONDS ?? "10")) * 1000;
let stopping = false;
/** Ends the wait between two ticks early, so a stop request is handled at once. */
let wake: (() => void) | undefined;

const bridge = await startBridge(localBrowserProvider()).catch((error: Error) => {
  console.error(`[bridge] could not listen on 127.0.0.1:${bridgeConfig().port}: ${error.message}`);
  return null;
});
if (bridge) console.log(`[bridge] LinkedIn bridge on 127.0.0.1:${bridgeConfig().port}`);

async function loop() {
  while (!stopping) {
    const started = Date.now();
    try {
      const results = await runTick(engineDeps({ now: new Date() }));
      for (const r of results) {
        const o = r.outreach;
        if (r.error) console.error(`[engine] account ${r.accountId}: ${r.error}`);
        else if (r.events || r.sourced || o?.invites || o?.messages || o?.unresponsive) {
          console.log(
            `[engine] account ${r.accountId}: ${r.events} events, ${r.sourced} sourced, ${r.scored} scored, ` +
              `${o?.invites ?? 0} invites, ${o?.messages ?? 0} messages${o?.skipped ? ` (${o.skipped})` : ""}`,
          );
        }
      }
    } catch (error) {
      console.error("[engine] tick failed", error);
    }
    const wait = intervalMs - (Date.now() - started);
    if (wait > 0 && !stopping) {
      await new Promise<void>((resolve) => {
        const timer = setTimeout(resolve, wait);
        wake = () => {
          clearTimeout(timer);
          resolve();
        };
      });
    }
  }
  bridge?.close();
  await localBrowserProvider().sessions.closeAll();
  await db.$disconnect();
  console.log("[engine] worker stopped");
  process.exit(0);
}

for (const signal of ["SIGINT", "SIGTERM"] as const) {
  process.on(signal, () => {
    stopping = true;
    wake?.();
  });
}

console.log(`[engine] worker started, tick every ${intervalMs / 1000}s (simulator TIME_SCALE=${process.env.TIME_SCALE ?? "1"})`);
void loop();
