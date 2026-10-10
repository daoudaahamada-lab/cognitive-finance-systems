import { timingSafeEqual } from "node:crypto";
import { NextResponse } from "next/server";
import { engineDeps } from "@/server/engine/deps";
import { runTick } from "@/server/engine/tick";

export const dynamic = "force-dynamic";

/** For external schedulers (cron, Cloud Scheduler): POST with `Authorization: Bearer <ENGINE_TICK_SECRET>`. */
export async function POST(request: Request) {
  const secret = Buffer.from(process.env.ENGINE_TICK_SECRET ?? "");
  const given = Buffer.from(request.headers.get("authorization")?.replace(/^Bearer\s+/i, "") ?? "");
  const ok = secret.length > 0 && given.length === secret.length && timingSafeEqual(given, secret);
  if (!ok) return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  const results = await runTick(engineDeps());
  return NextResponse.json({ accounts: results.length, results });
}
