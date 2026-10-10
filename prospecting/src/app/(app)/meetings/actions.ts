"use server";

import type { MeetingStatus } from "@prisma/client";
import { revalidatePath } from "next/cache";
import { requireContext } from "@/server/auth/context";
import { setMeetingStatus } from "@/server/services/meetings";

export async function meetingStatusAction(meetingId: string, status: MeetingStatus) {
  const { workspace } = await requireContext();
  await setMeetingStatus(workspace.id, meetingId, status);
  revalidatePath("/meetings");
}
