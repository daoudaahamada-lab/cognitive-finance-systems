"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { requireContext } from "@/server/auth/context";
import {
  campaignSchema,
  createCampaign,
  importProspects,
  setCampaignStatus,
  updateCampaign,
} from "@/server/services/campaigns";
import { toActionState, type ActionState } from "@/server/services/errors";
import { parseForm } from "@/server/services/forms";

function formData(form: FormData) {
  return { ...Object.fromEntries(form), sources: form.getAll("sources"), companySizes: form.getAll("companySizes"), signals: form.getAll("signals") };
}

export async function saveCampaignAction(campaignId: string | null, _: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const parsed = parseForm(campaignSchema, formData(form));
  if ("state" in parsed) return parsed.state;
  let id = campaignId;
  try {
    if (campaignId) await updateCampaign(workspace.id, campaignId, parsed.data);
    else id = (await createCampaign(workspace.id, parsed.data)).id;
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/campaigns");
  if (!campaignId) redirect(`/campaigns/${id}`);
  return { ok: true, message: "Campagne enregistrée." };
}

export async function setCampaignStatusAction(campaignId: string, status: "ACTIVE" | "PAUSED" | "ARCHIVED", _: ActionState): Promise<ActionState> {
  const { workspace } = await requireContext();
  try {
    await setCampaignStatus(workspace.id, campaignId, status);
  } catch (error) {
    return toActionState(error);
  }
  revalidatePath("/", "layout");
  if (status === "ARCHIVED") redirect("/campaigns");
  return { ok: true, message: status === "ACTIVE" ? "Campagne lancée : le moteur s'en occupe." : "Campagne mise en pause." };
}

export async function importProspectsAction(campaignId: string, _: ActionState, form: FormData): Promise<ActionState> {
  const { workspace } = await requireContext();
  const file = form.get("file");
  let text = String(form.get("urls") ?? "");
  if (file instanceof File && file.size > 0) {
    if (file.size > 2_000_000) return { error: "Fichier trop lourd (2 Mo maximum)." };
    text += `\n${await file.text()}`;
  }
  try {
    const result = await importProspects(workspace.id, campaignId, text);
    revalidatePath(`/campaigns/${campaignId}`);
    return {
      ok: true,
      message: `${result.imported} prospect${result.imported > 1 ? "s" : ""} importé${result.imported > 1 ? "s" : ""}${result.skipped ? `, ${result.skipped} déjà connu${result.skipped > 1 ? "s" : ""} ou introuvable${result.skipped > 1 ? "s" : ""}` : ""}.`,
    };
  } catch (error) {
    return toActionState(error);
  }
}
