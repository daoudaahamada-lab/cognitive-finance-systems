import type { Campaign, LinkedInAccount, Prospect, Workspace } from "@prisma/client";
import type { SequenceStep, WriteInput } from "@/server/agents/writer";
import type { TemplateVars } from "@/server/domain/templates";
import { parseFollowUps } from "@/server/domain/followups";
import { isWithinSendingWindow } from "@/server/domain/schedule";
import { logActivity } from "./activity";
import { nextSequenceAction, sendOutbound } from "./conversation";
import type { EngineDeps } from "./deps";
import { accountQuota } from "./quota";
import { templateVars } from "./vars";

/** Per-tick caps spread actions over the day instead of bursting them. */
export const INVITES_PER_TICK = 3;
export const MESSAGES_PER_TICK = 5;

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
  const provider = deps.providerFor(account.provider);
  const notSnoozed = { OR: [{ snoozedUntil: null }, { snoozedUntil: { lte: now } }] };
  const activeCampaign = { campaign: { status: "ACTIVE" as const } };

  // 1. Invitations, best-scored first.
  let invites = 0;
  const toInvite = await db.prospect.findMany({
    where: { accountId: account.id, stage: "QUALIFIED", ...activeCampaign, ...notSnoozed },
    include: { campaign: true, workspace: true },
    orderBy: [{ score: "desc" }, { createdAt: "asc" }],
    take: Math.min(quota.remaining.invites, INVITES_PER_TICK),
  });
  for (const prospect of toInvite) {
    const { campaign, workspace } = prospect;
    const note = campaign.inviteNote
      ? await deps.agents.writer.write(writeInput(prospect, campaign.inviteNote, { kind: "invite_note" }, templateVars(prospect, account, campaign, workspace)))
      : null;
    await provider.sendInvitation({ externalId: account.externalId }, prospect.externalId, note, now);
    await db.prospect.update({
      where: { id: prospect.id },
      data: { stage: "INVITED", stageChangedAt: now, invitedAt: now },
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
  let messageBudget = Math.min(quota.remaining.messages, MESSAGES_PER_TICK);
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
          nextActionAt: nextSequenceAction(campaign.followUps, 0, now),
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
          nextActionAt: nextSequenceAction(campaign.followUps, index + 1, now),
        },
      });
    }
    messages++;
    messageBudget--;
  }

  return { invites, messages, unresponsive };
}
