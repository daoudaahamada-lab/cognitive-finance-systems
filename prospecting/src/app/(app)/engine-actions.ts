"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import { db } from "@/server/db";
import { engineDeps } from "@/server/engine/deps";
import { runTick } from "@/server/engine/tick";
import { plural } from "@/lib/format";

export type EngineRunState = { ok: boolean; message: string } | null;

/** Runs one engine pass for the current workspace now (the worker does this continuously) and sums it up. */
export async function runEngineNow(_?: EngineRunState): Promise<EngineRunState> {
  const { workspace } = await requireContext();
  const active = await db.linkedInAccount.count({ where: { workspaceId: workspace.id, status: "ACTIVE" } });
  if (active === 0) return { ok: false, message: "Aucun compte actif" };

  const deps = engineDeps();
  const results = await runTick(deps, { workspaceId: workspace.id });
  revalidatePath("/", "layout");
  if (results.length === 0) return { ok: true, message: "Synchronisation déjà en cours : réessayez dans une minute." };

  const failed = results.filter((r) => r.error);
  if (failed.length > 0) return { ok: false, message: failed.map((r) => r.error).join(" · ") };

  // Replies are logged with the pass's own timestamp.
  const replies = await db.activity.count({ where: { workspaceId: workspace.id, type: "REPLY_RECEIVED", createdAt: deps.now } });
  const sourced = results.reduce((sum, r) => sum + r.sourced, 0);
  const sent = results.reduce((sum, r) => sum + (r.outreach?.invites ?? 0) + (r.outreach?.messages ?? 0), 0);
  const outsideWindow = results.every((r) => r.outreach?.skipped === "outside_window");
  return {
    ok: true,
    message:
      `Synchronisé : ${plural(replies, "réponse")}, ${plural(sourced, "prospect trouvé", "prospects trouvés")}, ${plural(sent, "envoi")}` +
      (outsideWindow ? " (hors horaires d'envoi)" : ""),
  };
}
