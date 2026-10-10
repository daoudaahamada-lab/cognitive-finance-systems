/**
 * Background worker: runs the prospecting engine on a fixed interval.
 *   npm run worker
 */
import { db } from "@/server/db";
import { engineDeps } from "@/server/engine/deps";
import { runTick } from "@/server/engine/tick";

const intervalMs = Math.max(1, Number(process.env.WORKER_INTERVAL_SECONDS ?? "10")) * 1000;
let stopping = false;

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
    if (wait > 0) await new Promise((resolve) => setTimeout(resolve, wait));
  }
  await db.$disconnect();
}

for (const signal of ["SIGINT", "SIGTERM"] as const) {
  process.on(signal, () => {
    stopping = true;
  });
}

console.log(`[engine] worker started, tick every ${intervalMs / 1000}s (TIME_SCALE=${process.env.TIME_SCALE ?? "1"})`);
void loop();
