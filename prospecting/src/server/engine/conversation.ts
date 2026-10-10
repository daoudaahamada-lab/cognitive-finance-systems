import type { ActivityType, LinkedInAccount, MessageAuthor, Prisma, Prospect } from "@prisma/client";
import { parseFollowUps, FINAL_WAIT_DAYS } from "@/server/domain/followups";
import { planLimits } from "@/server/domain/plans";
import { DAY, addScaled } from "@/server/domain/time";
import { logActivity } from "./activity";
import type { EngineDeps } from "./deps";
import { accountQuota } from "./quota";
import { templateVars } from "./vars";

export async function ensureConversation(deps: EngineDeps, prospect: Pick<Prospect, "id" | "workspaceId" | "accountId">) {
  return deps.db.conversation.upsert({
    where: { prospectId: prospect.id },
    create: { workspaceId: prospect.workspaceId, prospectId: prospect.id, accountId: prospect.accountId },
    update: {},
  });
}

type OutboundInput = {
  prospect: Prospect & { account: LinkedInAccount };
  body: string;
  author: Exclude<MessageAuthor, "PROSPECT">;
  activity: ActivityType;
  data?: Prisma.InputJsonValue;
};

/** Sends a LinkedIn message and records it everywhere it shows up (thread, prospect, activity log). */
export async function sendOutbound(deps: EngineDeps, { prospect, body, author, activity, data }: OutboundInput) {
  const provider = deps.providerFor(prospect.account.provider);
  const { externalId } = await provider.sendMessage({ externalId: prospect.account.externalId }, prospect.externalId, body, deps.now);
  const conversation = await ensureConversation(deps, prospect);
  const message = await deps.db.message.create({
    data: { conversationId: conversation.id, direction: "OUTBOUND", author, body, externalId, sentAt: deps.now },
  });
  await deps.db.conversation.update({ where: { id: conversation.id }, data: { lastMessageAt: deps.now } });
  await deps.db.prospect.update({ where: { id: prospect.id }, data: { lastContactedAt: deps.now } });
  await logActivity(deps.db, {
    workspaceId: prospect.workspaceId,
    campaignId: prospect.campaignId,
    prospectId: prospect.id,
    accountId: prospect.accountId,
    type: activity,
    data,
    at: deps.now,
  });
  return message;
}

/** Stage changes the setter's reading of a reply implies, whatever the setter mode. */
async function applyIntent(deps: EngineDeps, prospect: Prospect, intent: string) {
  if (intent === "NOT_INTERESTED") {
    await deps.db.prospect.update({
      where: { id: prospect.id },
      data: { stage: "NOT_INTERESTED", stageChangedAt: deps.now, nextActionAt: null },
    });
    await logActivity(deps.db, {
      workspaceId: prospect.workspaceId, campaignId: prospect.campaignId, prospectId: prospect.id,
      accountId: prospect.accountId, type: "MARKED_NOT_INTERESTED", at: deps.now,
    });
  } else if (intent === "OUT_OF_OFFICE") {
    // Put the prospect back in the sequence a week later.
    await deps.db.prospect.update({
      where: { id: prospect.id },
      data: { stage: "MESSAGED", stageChangedAt: deps.now, nextActionAt: addScaled(deps.now, FINAL_WAIT_DAYS * DAY) },
    });
  }
}

/**
 * Lets the setter handle the latest prospect message on a conversation:
 * send (AUTO), draft (APPROVAL) or hand over to a human (OFF, escalations).
 */
export async function runSetter(deps: EngineDeps, conversationId: string) {
  const conversation = await deps.db.conversation.findUniqueOrThrow({
    where: { id: conversationId },
    include: {
      prospect: { include: { campaign: true, account: true, workspace: true } },
      messages: { orderBy: { sentAt: "asc" }, take: 50 },
    },
  });
  const { prospect } = conversation;
  const { campaign, workspace } = prospect;

  // A new prospect message makes any pending draft stale.
  await deps.db.draft.updateMany({
    where: { conversationId, status: "PENDING" },
    data: { status: "REJECTED", decidedAt: deps.now },
  });

  if (conversation.status === "HUMAN" || conversation.status === "NEEDS_HUMAN") return;
  if (conversation.status === "CLOSED") {
    await escalate(deps, conversation.id, prospect, "UNKNOWN", "Nouveau message sur une conversation close.");
    return;
  }

  const mode = planLimits(workspace.plan).setter ? campaign.setterMode : "OFF";
  if (mode === "OFF") {
    await deps.db.conversation.update({
      where: { id: conversationId },
      data: { status: "NEEDS_HUMAN", escalationReason: "Setter désactivé : à vous de répondre." },
    });
    return;
  }

  const decision = await deps.agents.setter.decide({
    history: conversation.messages.map((m) => ({ direction: m.direction, author: m.author, body: m.body })),
    vars: templateVars(prospect, prospect.account, campaign, workspace),
    offer: campaign.offer || workspace.offer,
    persona: campaign.persona || workspace.persona,
    prospectStage: prospect.stage,
  });

  await deps.db.conversation.update({ where: { id: conversationId }, data: { lastIntent: decision.intent } });
  await applyIntent(deps, prospect, decision.intent);

  if (decision.action === "escalate") {
    await escalate(deps, conversation.id, prospect, decision.intent, decision.reason, decision.agent);
    return;
  }
  if (decision.action === "wait") {
    await deps.db.conversation.update({ where: { id: conversationId }, data: { unread: false } });
    return;
  }

  const quota = await accountQuota(deps.db, prospect.account, deps.now);
  if (mode === "AUTO" && quota.remaining.messages > 0) {
    await sendOutbound(deps, {
      prospect,
      body: decision.message,
      author: "AI",
      activity: "AI_REPLY_SENT",
      data: { intent: decision.intent, by: decision.agent },
    });
    await deps.db.conversation.update({
      where: { id: conversationId },
      data: { unread: false, status: decision.closeAfter ? "CLOSED" : "AI_ACTIVE" },
    });
    return;
  }

  const rationale = mode === "AUTO"
    ? `${decision.rationale} (Quota de messages du jour atteint : validez pour envoyer.)`
    : decision.rationale;
  await deps.db.draft.create({
    data: { conversationId, body: decision.message, intent: decision.intent, rationale, author: decision.agent, createdAt: deps.now },
  });
  await logActivity(deps.db, {
    workspaceId: prospect.workspaceId, campaignId: prospect.campaignId, prospectId: prospect.id,
    accountId: prospect.accountId, type: "DRAFT_CREATED", data: { intent: decision.intent }, at: deps.now,
  });
}

async function escalate(deps: EngineDeps, conversationId: string, prospect: Prospect, intent: string, reason: string, by = "rules") {
  await deps.db.conversation.update({
    where: { id: conversationId },
    data: { status: "NEEDS_HUMAN", escalationReason: reason, unread: true },
  });
  await logActivity(deps.db, {
    workspaceId: prospect.workspaceId, campaignId: prospect.campaignId, prospectId: prospect.id,
    accountId: prospect.accountId, type: "ESCALATED", data: { intent, reason, by }, at: deps.now,
  });
}

/** Next wake-up after `sent` sequence messages (first message counts as 0 follow-ups sent). */
export function nextSequenceAction(followUpsJson: unknown, followUpsSent: number, maxFollowUps: number, now: Date): Date {
  const steps = parseFollowUps(followUpsJson).slice(0, maxFollowUps);
  const next = steps[followUpsSent];
  return addScaled(now, (next ? next.delayDays : FINAL_WAIT_DAYS) * DAY);
}
