import type { Campaign, LinkedInAccount, Prospect, Workspace } from "@prisma/client";
import type { SequenceStep, WriteInput } from "@/server/agents/writer";
import type { TemplateVars } from "@/server/domain/templates";
import { parseFollowUps } from "@/server/domain/followups";
import { isWithinSendingWindow } from "@/server/domain/schedule";
import { DAY, HOUR, addScaled } from "@/server/domain/time";
import { PROSPECT_ERROR_CODES, ProviderActionError, ProviderLimitError, type LinkedInProvider, type ProfileUpdate } from "@/server/linkedin/types";
import { logActivity } from "./activity";
import { nextSequenceAction, sendOutbound } from "./conversation";
import type { EngineDeps } from "./deps";
import { FIRST_MESSAGE_DELAY } from "./events";
import { paceBudget, waitScale } from "./pace";
import { accountQuota } from "./quota";
import { templateVars } from "./vars";

/** Per-tick caps spread actions over the day instead of bursting them. */
export const INVITES_PER_TICK = 3;
export const MESSAGES_PER_TICK = 5;
/** A sequence message that keeps failing is retried this many times, then the prospect is left alone. */
export const MAX_MESSAGE_ATTEMPTS = 3;
const MESSAGE_RETRY_DELAY = 6 * HOUR;

/** Keeps only non-empty strings from a provider's profile refresh. */
function profileUpdate(update: ProfileUpdate | void): ProfileUpdate {
  if (!update) return {};
  return Object.fromEntries(Object.entries(update).filter(([, v]) => typeof v === "string" && v.trim() !== "")) as ProfileUpdate;
}

/** Prospects known only by their URL (list import) get their profile read before anything is written to them. */
async function withFreshProfile<P extends Prospect>(deps: EngineDeps, provider: LinkedInProvider, account: LinkedInAccount, prospect: P): Promise<P> {
  if (!provider.enrichProfile || prospect.title || prospect.headline) return prospect;
  const fresh = profileUpdate(await provider.enrichProfile({ externalId: account.externalId }, prospect.externalId));
  if (Object.keys(fresh).length === 0) return prospect;
  await deps.db.prospect.update({ where: { id: prospect.id }, data: fresh });
  return { ...prospect, ...fresh };
}

function writeInput(
  prospect: Prospect & { campaign: Campaign; workspace: Workspace },
  template: string,
  step: SequenceStep,
  vars: TemplateVars,
): WriteInput {
  return {
    template,
    step,
    vars,
    prospectId: prospect.id,
    profile: prospect,
    offer: prospect.campaign.offer || prospect.workspace.offer,
    personalize: prospect.campaign.aiPersonalization,
  };
}

export type OutreachResult = { invites: number; messages: number; unresponsive: number; skipped?: "outside_window" };

export async function runOutreach(deps: EngineDeps, account: LinkedInAccount): Promise<OutreachResult> {
  const { db, now } = deps;
  if (!isWithinSendingWindow(account, now)) return { invites: 0, messages: 0, unresponsive: 0, skipped: "outside_window" };

  const quota = await accountQuota(db, account, now);
  const pace = await paceBudget(db, account, quota.limits, now);
  const provider = deps.providerFor(account.provider);
  const notSnoozed = { OR: [{ snoozedUntil: null }, { snoozedUntil: { lte: now } }] };
  const activeCampaign = { campaign: { status: "ACTIVE" as const } };

  // 1. Invitations, best-scored first (unless LinkedIn recently warned about the limit).
  let invites = 0;
  const invitesPaused = account.invitesPausedUntil !== null && account.invitesPausedUntil > now;
  const toInvite = await db.prospect.findMany({
    where: { accountId: account.id, stage: "QUALIFIED", ...activeCampaign, ...notSnoozed },
    include: { campaign: true, workspace: true },
    orderBy: [{ score: "desc" }, { createdAt: "asc" }],
    take: invitesPaused ? 0 : Math.min(quota.remaining.invites, INVITES_PER_TICK, pace.invites),
  });
  for (const queued of toInvite) {
    const { campaign, workspace } = queued;
    let prospect = queued;
    let note: string | null = null;
    let update: ProfileUpdate | void;
    try {
      prospect = await withFreshProfile(deps, provider, account, queued);
      note = campaign.inviteNote
        ? await deps.agents.writer.write(writeInput(prospect, campaign.inviteNote, { kind: "invite_note" }, templateVars(prospect, account, campaign, workspace)))
        : null;
      update = await provider.sendInvitation({ externalId: account.externalId }, prospect.externalId, note, now);
    } catch (error) {
      if (error instanceof ProviderLimitError) {
        await db.linkedInAccount.update({ where: { id: account.id }, data: { invitesPausedUntil: new Date(now.getTime() + DAY) } });
        await logActivity(db, {
          workspaceId: prospect.workspaceId, campaignId: campaign.id, prospectId: prospect.id, accountId: account.id,
          type: "ACTION_FAILED", data: { action: "invite", code: "LIMIT", message: error.message }, at: now,
        });
        break;
      }
      if (error instanceof ProviderActionError) {
        const verdict = await handleInviteError(deps, account, prospect, error);
        if (verdict === "stop") break;
        continue;
      }
      throw error;
    }
    await db.prospect.update({
      where: { id: prospect.id },
      data: { stage: "INVITED", stageChangedAt: now, invitedAt: now, ...profileUpdate(update) },
    });
    await logActivity(db, {
      workspaceId: prospect.workspaceId, campaignId: campaign.id, prospectId: prospect.id, accountId: account.id,
      type: "INVITE_SENT", data: note ? { note } : undefined, at: now,
    });
    invites++;
  }

  // 2. Sequence messages that are due (first message, follow-ups) and give-ups.
  let messages = 0;
  let unresponsive = 0;
  let messageBudget = Math.min(quota.remaining.messages, MESSAGES_PER_TICK, pace.messages);
  const due = await db.prospect.findMany({
    where: {
      accountId: account.id,
      stage: { in: ["CONNECTED", "MESSAGED"] },
      nextActionAt: { lte: now },
      ...activeCampaign,
      ...notSnoozed,
    },
    include: { campaign: true, workspace: true, account: true },
    orderBy: { nextActionAt: "asc" },
    take: 50,
  });
  for (const prospect of due) {
    const { campaign, workspace } = prospect;
    const steps = parseFollowUps(campaign.followUps);

    if (prospect.stage === "MESSAGED" && prospect.followUpsSent >= steps.length) {
      await db.prospect.update({
        where: { id: prospect.id },
        data: { stage: "UNRESPONSIVE", stageChangedAt: now, nextActionAt: null },
      });
      await logActivity(db, {
        workspaceId: prospect.workspaceId, campaignId: campaign.id, prospectId: prospect.id, accountId: account.id,
        type: "MARKED_UNRESPONSIVE", at: now,
      });
      unresponsive++;
      continue;
    }
    if (messageBudget <= 0) continue;

    const vars = templateVars(prospect, account, campaign, workspace);
    try {
      await sendSequenceStep(deps, prospect, steps, vars);
    } catch (error) {
      if (!(error instanceof ProviderActionError)) throw error;
      const verdict = await handleMessageError(deps, prospect, error);
      if (verdict === "stop") break;
      continue;
    }
    messages++;
    messageBudget--;
  }

  return { invites, messages, unresponsive };
}

type DueProspect = Prospect & { campaign: Campaign; workspace: Workspace; account: LinkedInAccount };

/** Sends the first message or the next follow-up. */
async function sendSequenceStep(deps: EngineDeps, prospect: DueProspect, steps: ReturnType<typeof parseFollowUps>, vars: TemplateVars) {
  const { db, now } = deps;
  const { campaign } = prospect;
  if (prospect.stage === "CONNECTED") {
    const body = await deps.agents.writer.write(writeInput(prospect, campaign.firstMessage, { kind: "first_message" }, vars));
    await sendOutbound(deps, { prospect, body, author: "SEQUENCE", activity: "MESSAGE_SENT" });
    await db.prospect.update({
      where: { id: prospect.id },
      data: {
        stage: "MESSAGED",
        stageChangedAt: now,
        firstMessagedAt: now,
        followUpsSent: 0,
        nextActionAt: nextSequenceAction(campaign.followUps, 0, now, waitScale(prospect.account)),
      },
    });
  } else {
    const index = prospect.followUpsSent;
    const step = steps[index]!;
    const body = await deps.agents.writer.write(writeInput(prospect, step.template, { kind: "follow_up", index }, vars));
    await sendOutbound(deps, { prospect, body, author: "SEQUENCE", activity: "FOLLOW_UP_SENT", data: { step: index + 1 } });
    await db.prospect.update({
      where: { id: prospect.id },
      data: {
        followUpsSent: index + 1,
        nextActionAt: nextSequenceAction(campaign.followUps, index + 1, now, waitScale(prospect.account)),
      },
    });
  }
}

/**
 * What a refused invitation tells us. Prospect-specific problems close the prospect;
 * anything else (unexpected page, worker down) leaves it queued and stops this tick's invitations.
 */
async function handleInviteError(deps: EngineDeps, account: LinkedInAccount, prospect: Prospect, error: ProviderActionError): Promise<"next" | "stop"> {
  const { db, now } = deps;
  const base = { workspaceId: prospect.workspaceId, campaignId: prospect.campaignId, prospectId: prospect.id, accountId: prospect.accountId, at: now };
  const failure = { ...base, type: "ACTION_FAILED" as const, data: { action: "invite", code: error.code, message: error.message } };
  if (error.code === "ALREADY_CONNECTED") {
    // Already in the network: skip straight to the first message.
    await db.prospect.update({
      where: { id: prospect.id },
      data: { stage: "CONNECTED", stageChangedAt: now, connectedAt: now, nextActionAt: addScaled(now, FIRST_MESSAGE_DELAY, waitScale(account)) },
    });
    return "next";
  }
  if (error.code === "ALREADY_PENDING") {
    await db.prospect.update({ where: { id: prospect.id }, data: { stage: "INVITED", stageChangedAt: now, invitedAt: now } });
    return "next";
  }
  await logActivity(db, failure);
  if (!PROSPECT_ERROR_CODES.includes(error.code)) return "stop";
  await db.prospect.update({
    where: { id: prospect.id },
    data: { stage: "DISQUALIFIED", stageChangedAt: now, disqualifiedReason: `LinkedIn : ${error.message}`, nextActionAt: null },
  });
  return "next";
}

/**
 * A sequence message failed: retry later. Prospect-specific failures give up after a few
 * attempts; systemic ones (worker down, unexpected page) stop this tick's messages.
 */
async function handleMessageError(deps: EngineDeps, prospect: Prospect, error: ProviderActionError): Promise<"next" | "stop"> {
  const { db, now } = deps;
  await logActivity(db, {
    workspaceId: prospect.workspaceId, campaignId: prospect.campaignId, prospectId: prospect.id, accountId: prospect.accountId,
    type: "ACTION_FAILED", data: { action: "message", code: error.code, message: error.message }, at: now,
  });
  if (!PROSPECT_ERROR_CODES.includes(error.code)) {
    await db.prospect.update({ where: { id: prospect.id }, data: { nextActionAt: new Date(now.getTime() + MESSAGE_RETRY_DELAY) } });
    return "stop";
  }
  const failures = await db.activity.count({ where: { prospectId: prospect.id, type: "ACTION_FAILED", data: { path: ["action"], equals: "message" } } });
  await db.prospect.update({
    where: { id: prospect.id },
    data:
      failures >= MAX_MESSAGE_ATTEMPTS
        ? { stage: "UNRESPONSIVE", stageChangedAt: now, nextActionAt: null }
        : { nextActionAt: new Date(now.getTime() + MESSAGE_RETRY_DELAY) },
  });
  return "next";
}
