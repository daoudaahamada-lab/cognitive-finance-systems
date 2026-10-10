"use server";

import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import { engineDeps } from "@/server/engine/deps";
import { runTick } from "@/server/engine/tick";

/** Runs one engine pass for the current workspace (the worker does this continuously). */
export async function runEngineNow() {
  const { workspace } = await requireContext();
  await runTick(engineDeps(), { workspaceId: workspace.id });
  revalidatePath("/", "layout");
}
