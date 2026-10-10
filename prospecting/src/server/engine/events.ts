import type { LinkedInAccount } from "@prisma/client";
import { HOUR, addScaled } from "@/server/domain/time";
import type { ProviderEvent } from "@/server/linkedin/types";
import { logActivity } from "./activity";
import { ensureConversation, runSetter } from "./conversation";
import type { EngineDeps } from "./deps";

/** Pause between an accepted invitation and the first message, so it does not look automated. */
export const FIRST_MESSAGE_DELAY = 4 * HOUR;

/** Stages a reply moves forward; later stages (meeting, refusal) are never rolled back by a reply. */
const REPLYABLE_STAGES = new Set(["INVITED", "CONNECTED", "MESSAGED", "UNRESPONSIVE"]);

export async function syncEvents(deps: EngineDeps, account: LinkedInAccount): Promise<number> {
  const provider = deps.providerFor(account.provider);
  const events = await provider.fetchEvents({ externalId: account.externalId }, deps.now);
  for (const event of events) await handleEvent(deps, account, event);
  return events.length;
}

export async function handleEvent(deps: EngineDeps, account: LinkedInAccount, event: ProviderEvent) {
  const { db, now } = deps;
  const prospect = await db.prospect.findFirst({
    where: { accountId: account.id, externalId: event.profileId },
  });
  // Someone we never contacted through this product: nothing to track.
  if (!prospect) return;
  const base = {
    workspaceId: prospect.workspaceId, campaignId: prospect.campaignId,
    prospectId: prospect.id, accountId: account.id, at: now,
  };

  switch (event.kind) {
    case "invite_accepted": {
      if (prospect.stage !== "INVITED") return;
      await db.prospect.update({
        where: { id: prospect.id },
        data: {
          stage: "CONNECTED",
          stageChangedAt: now,
          connectedAt: event.at,
          nextActionAt: addScaled(now, FIRST_MESSAGE_DELAY),
        },
      });
      await logActivity(db, { ...base, type: "INVITE_ACCEPTED" });
      return;
    }

    case "message_received": {
      const conversation = await ensureConversation(deps, prospect);
      const duplicate = await db.message.findFirst({
        where: { conversationId: conversation.id, externalId: event.externalId },
      });
      if (duplicate) return;
      await db.message.create({
        data: {
          conversationId: conversation.id, direction: "INBOUND", author: "PROSPECT",
          body: event.text, externalId: event.externalId, sentAt: event.at,
        },
      });
      await db.conversation.update({
        where: { id: conversation.id },
        data: { unread: true, lastMessageAt: event.at },
      });
      await db.prospect.update({
        where: { id: prospect.id },
        data: REPLYABLE_STAGES.has(prospect.stage)
          ? { stage: "REPLIED", stageChangedAt: now, repliedAt: event.at, nextActionAt: null }
          : { repliedAt: event.at },
      });
      await logActivity(db, { ...base, type: "REPLY_RECEIVED" });
      await runSetter(deps, conversation.id);
      return;
    }

    case "meeting_booked": {
      await db.meeting.create({
        data: {
          workspaceId: prospect.workspaceId, prospectId: prospect.id, campaignId: prospect.campaignId,
          startsAt: event.startsAt, origin: "calendar", createdAt: now,
        },
      });
      await db.prospect.update({
        where: { id: prospect.id },
        data: { stage: "MEETING_BOOKED", stageChangedAt: now, nextActionAt: null },
      });
      await db.conversation.updateMany({
        where: { prospectId: prospect.id },
        data: { status: "CLOSED", unread: true, escalationReason: null },
      });
      await logActivity(db, { ...base, type: "MEETING_BOOKED", data: { startsAt: event.startsAt.toISOString() } });
      return;
    }
  }
}
