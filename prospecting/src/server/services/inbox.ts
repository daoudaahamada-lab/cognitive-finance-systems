import type { Prisma } from "@prisma/client";
import { db } from "@/server/db";
import { logActivity } from "@/server/engine/activity";
import { runSetter, sendOutbound } from "@/server/engine/conversation";
import { engineDeps } from "@/server/engine/deps";
import { accountQuota } from "@/server/engine/quota";
import { ProviderActionError, ProviderAuthError, ProviderLimitError } from "@/server/linkedin/types";
import { UserError } from "./errors";

export const INBOX_TABS = ["todo", "drafts", "ai", "all"] as const;
export type InboxTab = (typeof INBOX_TABS)[number];

function tabWhere(workspaceId: string, tab: InboxTab): Prisma.ConversationWhereInput {
  const base = { workspaceId, messages: { some: {} } };
  switch (tab) {
    case "todo":
      return {
        ...base,
        OR: [
          { status: "NEEDS_HUMAN" },
          { drafts: { some: { status: "PENDING" } } },
          { status: "HUMAN", unread: true },
        ],
      };
    case "drafts":
      return { ...base, drafts: { some: { status: "PENDING" } } };
    case "ai":
      return { ...base, status: "AI_ACTIVE" };
    case "all":
      return base;
  }
}

export async function inboxCounts(workspaceId: string) {
  const entries = await Promise.all(INBOX_TABS.map(async (tab) => [tab, await db.conversation.count({ where: tabWhere(workspaceId, tab) })] as const));
  return Object.fromEntries(entries) as Record<InboxTab, number>;
}

export async function listConversations(workspaceId: string, tab: InboxTab, q?: string) {
  const search = q?.trim();
  return db.conversation.findMany({
    where: {
      ...tabWhere(workspaceId, tab),
      ...(search
        ? {
            prospect: {
              OR: [
                { firstName: { contains: search, mode: "insensitive" } },
                { lastName: { contains: search, mode: "insensitive" } },
                { company: { contains: search, mode: "insensitive" } },
              ],
            },
          }
        : {}),
    },
    include: {
      prospect: { select: { firstName: true, lastName: true, company: true, title: true, stage: true } },
      messages: { orderBy: { sentAt: "desc" }, take: 1 },
      drafts: { where: { status: "PENDING" }, select: { id: true } },
    },
    orderBy: { lastMessageAt: { sort: "desc", nulls: "last" } },
    take: 100,
  });
}

export async function getThread(workspaceId: string, conversationId: string) {
  return db.conversation.findFirst({
    where: { id: conversationId, workspaceId },
    include: {
      prospect: { include: { campaign: { select: { id: true, name: true, setterMode: true } }, meetings: { orderBy: { startsAt: "desc" }, take: 1 } } },
      account: { select: { fullName: true } },
      messages: { orderBy: { sentAt: "asc" } },
      drafts: { where: { status: "PENDING" }, orderBy: { createdAt: "desc" }, take: 1 },
    },
  });
}

async function ownedConversation(workspaceId: string, conversationId: string) {
  const conversation = await db.conversation.findFirst({
    where: { id: conversationId, workspaceId },
    include: { prospect: { include: { account: true } } },
  });
  if (!conversation) throw new UserError("Conversation introuvable.");
  return conversation;
}

async function assertMessageQuota(account: Parameters<typeof accountQuota>[1], now: Date) {
  const quota = await accountQuota(db, account, now);
  if (quota.remaining.messages <= 0) {
    throw new UserError(`Quota de messages atteint pour ce compte (${quota.limits.dailyMessages} sur 24 h). Réessayez plus tard.`);
  }
}

const normalize = (body: string) => body.replace(/\r\n?/g, "\n").trim();

/** Runs a LinkedIn send, turning provider errors into messages the user can act on. */
async function sending<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (error instanceof ProviderAuthError) throw new UserError(`Session LinkedIn invalide : ${error.message}`);
    if (error instanceof ProviderActionError || error instanceof ProviderLimitError) throw new UserError(`LinkedIn : ${error.message}`);
    throw error;
  }
}

export async function sendHumanReply(workspaceId: string, conversationId: string, body: string, handBack: boolean) {
  const text = normalize(body);
  if (!text) throw new UserError("Le message est vide.");
  if (text.length > 8000) throw new UserError("Message trop long (8000 caractères maximum).");
  const conversation = await ownedConversation(workspaceId, conversationId);
  if (conversation.prospect.account.status === "DISCONNECTED") throw new UserError("Le compte LinkedIn est déconnecté.");
  const deps = engineDeps();
  await assertMessageQuota(conversation.prospect.account, deps.now);
  await sending(() => sendOutbound(deps, { prospect: conversation.prospect, body: text, author: "HUMAN", activity: "HUMAN_REPLY_SENT" }));
  await db.draft.updateMany({ where: { conversationId, status: "PENDING" }, data: { status: "REJECTED", decidedAt: deps.now } });
  await db.conversation.update({
    where: { id: conversationId },
    data: { unread: false, status: handBack ? "AI_ACTIVE" : "HUMAN", escalationReason: null },
  });
}

export async function approveDraft(workspaceId: string, draftId: string, editedBody?: string) {
  const draft = await db.draft.findFirst({ where: { id: draftId, status: "PENDING", conversation: { workspaceId } } });
  if (!draft) throw new UserError("Ce brouillon n'est plus disponible.");
  const conversation = await ownedConversation(workspaceId, draft.conversationId);
  const body = normalize(editedBody ?? draft.body);
  if (!body) throw new UserError("Le message est vide.");
  const deps = engineDeps();
  await assertMessageQuota(conversation.prospect.account, deps.now);
  // Claim the draft first so a double click cannot send it twice.
  const claimed = await db.draft.updateMany({ where: { id: draftId, status: "PENDING" }, data: { status: "SENT", decidedAt: deps.now, body } });
  if (claimed.count === 0) throw new UserError("Ce brouillon a déjà été traité.");
  try {
    await sending(() =>
      sendOutbound(deps, {
        prospect: conversation.prospect,
        body,
        author: "AI",
        activity: "AI_REPLY_SENT",
        data: { intent: draft.intent, approved: true, edited: body !== draft.body },
      }),
    );
  } catch (error) {
    // Not sent: put the draft back so it can be retried.
    await db.draft.update({ where: { id: draftId }, data: { status: "PENDING", decidedAt: null, body: draft.body } });
    throw error;
  }
  await db.conversation.update({
    where: { id: conversation.id },
    data: { unread: false, status: draft.intent === "NOT_INTERESTED" ? "CLOSED" : "AI_ACTIVE" },
  });
}

export async function rejectDraft(workspaceId: string, draftId: string) {
  const draft = await db.draft.findFirst({ where: { id: draftId, status: "PENDING", conversation: { workspaceId } }, include: { conversation: { include: { prospect: true } } } });
  if (!draft) throw new UserError("Ce brouillon n'est plus disponible.");
  const now = new Date();
  await db.draft.update({ where: { id: draftId }, data: { status: "REJECTED", decidedAt: now } });
  await db.conversation.update({
    where: { id: draft.conversationId },
    data: { status: "NEEDS_HUMAN", escalationReason: "Brouillon refusé : à vous de répondre.", unread: true },
  });
  const p = draft.conversation.prospect;
  await logActivity(db, { workspaceId, campaignId: p.campaignId, prospectId: p.id, accountId: p.accountId, type: "DRAFT_REJECTED", at: now });
}

export async function takeOver(workspaceId: string, conversationId: string) {
  await ownedConversation(workspaceId, conversationId);
  await db.conversation.update({ where: { id: conversationId }, data: { status: "HUMAN", escalationReason: null } });
}

/** Gives the thread back to the setter; if the prospect is waiting for an answer, the setter answers now. */
export async function handBackToAi(workspaceId: string, conversationId: string) {
  await ownedConversation(workspaceId, conversationId);
  await db.conversation.update({ where: { id: conversationId }, data: { status: "AI_ACTIVE", escalationReason: null, unread: false } });
  const last = await db.message.findFirst({ where: { conversationId }, orderBy: { sentAt: "desc" } });
  if (last?.direction === "INBOUND") await runSetter(engineDeps(), conversationId);
}

export async function markHandled(workspaceId: string, conversationId: string) {
  const conversation = await ownedConversation(workspaceId, conversationId);
  await db.conversation.update({
    where: { id: conversationId },
    data: { unread: false, escalationReason: null, status: conversation.status === "NEEDS_HUMAN" ? "HUMAN" : conversation.status },
  });
}

export async function logMeeting(workspaceId: string, prospectId: string, startsAt: Date) {
  if (Number.isNaN(startsAt.getTime())) throw new UserError("Date de rendez-vous invalide.");
  const prospect = await db.prospect.findFirst({ where: { id: prospectId, workspaceId } });
  if (!prospect) throw new UserError("Prospect introuvable.");
  const now = new Date();
  await db.meeting.create({
    data: { workspaceId, prospectId, campaignId: prospect.campaignId, startsAt, origin: "manual" },
  });
  await db.prospect.update({ where: { id: prospectId }, data: { stage: "MEETING_BOOKED", stageChangedAt: now, nextActionAt: null } });
  await db.conversation.updateMany({ where: { prospectId }, data: { status: "CLOSED", unread: false, escalationReason: null } });
  await logActivity(db, {
    workspaceId, campaignId: prospect.campaignId, prospectId, accountId: prospect.accountId,
    type: "MEETING_BOOKED", data: { startsAt: startsAt.toISOString(), manual: true }, at: now,
  });
}
