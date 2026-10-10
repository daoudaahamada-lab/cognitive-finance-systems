import type { Prisma, ProspectStage } from "@prisma/client";
import { db } from "@/server/db";
import { DAY } from "@/server/domain/time";
import { logActivity } from "@/server/engine/activity";
import { UserError } from "./errors";

export const PAGE_SIZE = 50;

export type ProspectFilters = {
  stage?: ProspectStage;
  campaignId?: string;
  q?: string;
  minScore?: number;
  sort?: "recent" | "score";
  page?: number;
};

export function prospectWhere(workspaceId: string, f: ProspectFilters): Prisma.ProspectWhereInput {
  const q = f.q?.trim();
  return {
    workspaceId,
    ...(f.stage ? { stage: f.stage } : {}),
    ...(f.campaignId ? { campaignId: f.campaignId } : {}),
    ...(f.minScore ? { score: { gte: f.minScore } } : {}),
    ...(q
      ? {
          OR: [
            { firstName: { contains: q, mode: "insensitive" } },
            { lastName: { contains: q, mode: "insensitive" } },
            { company: { contains: q, mode: "insensitive" } },
            { title: { contains: q, mode: "insensitive" } },
          ],
        }
      : {}),
  };
}

export async function listProspects(workspaceId: string, f: ProspectFilters) {
  const where = prospectWhere(workspaceId, f);
  const page = Math.max(1, f.page ?? 1);
  const [total, rows] = await Promise.all([
    db.prospect.count({ where }),
    db.prospect.findMany({
      where,
      include: { campaign: { select: { name: true } } },
      orderBy: f.sort === "score" ? [{ score: { sort: "desc", nulls: "last" } }, { createdAt: "desc" }] : [{ stageChangedAt: "desc" }],
      skip: (page - 1) * PAGE_SIZE,
      take: PAGE_SIZE,
    }),
  ]);
  return { total, rows, page, pages: Math.max(1, Math.ceil(total / PAGE_SIZE)) };
}

export const BOARD_STAGES: ProspectStage[] = ["QUALIFIED", "INVITED", "CONNECTED", "MESSAGED", "REPLIED", "MEETING_BOOKED"];

export async function prospectBoard(workspaceId: string, f: ProspectFilters) {
  const base = prospectWhere(workspaceId, { ...f, stage: undefined });
  return Promise.all(
    BOARD_STAGES.map(async (stage) => {
      const where = { ...base, stage };
      const [count, items] = await Promise.all([
        db.prospect.count({ where }),
        db.prospect.findMany({ where, orderBy: { stageChangedAt: "desc" }, take: 25 }),
      ]);
      return { stage, count, items };
    }),
  );
}

export async function getProspect(workspaceId: string, prospectId: string) {
  return db.prospect.findFirst({
    where: { id: prospectId, workspaceId },
    include: {
      campaign: { select: { id: true, name: true, minScore: true } },
      account: { select: { fullName: true } },
      conversation: { select: { id: true, status: true } },
      meetings: { orderBy: { startsAt: "desc" } },
      activities: { orderBy: [{ createdAt: "desc" }, { id: "desc" }], take: 100 },
    },
  });
}

async function ownedProspect(workspaceId: string, prospectId: string) {
  const prospect = await db.prospect.findFirst({ where: { id: prospectId, workspaceId } });
  if (!prospect) throw new UserError("Prospect introuvable.");
  return prospect;
}

export type ManualStageAction = "exclude" | "requalify" | "not_interested";

export async function applyManualStage(workspaceId: string, prospectId: string, action: ManualStageAction) {
  const prospect = await ownedProspect(workspaceId, prospectId);
  const now = new Date();
  if (action === "exclude") {
    if (!["NEW", "QUALIFIED", "INVITED"].includes(prospect.stage)) {
      throw new UserError("Seul un prospect pas encore en conversation peut être exclu.");
    }
    await db.prospect.update({
      where: { id: prospectId },
      data: { stage: "DISQUALIFIED", stageChangedAt: now, disqualifiedReason: "Exclu manuellement", nextActionAt: null },
    });
  } else if (action === "requalify") {
    if (prospect.stage !== "DISQUALIFIED") throw new UserError("Ce prospect n'est pas disqualifié.");
    await db.prospect.update({
      where: { id: prospectId },
      data: { stage: "QUALIFIED", stageChangedAt: now, disqualifiedReason: null },
    });
  } else {
    await db.prospect.update({
      where: { id: prospectId },
      data: { stage: "NOT_INTERESTED", stageChangedAt: now, nextActionAt: null },
    });
    await db.conversation.updateMany({ where: { prospectId }, data: { status: "CLOSED", unread: false } });
    await logActivity(db, {
      workspaceId, campaignId: prospect.campaignId, prospectId, accountId: prospect.accountId,
      type: "MARKED_NOT_INTERESTED", data: { manual: true }, at: now,
    });
  }
}

export async function snoozeProspect(workspaceId: string, prospectId: string, days: number) {
  await ownedProspect(workspaceId, prospectId);
  const snoozedUntil = days > 0 ? new Date(Date.now() + days * DAY) : null;
  await db.prospect.update({ where: { id: prospectId }, data: { snoozedUntil } });
}

export async function saveNotes(workspaceId: string, prospectId: string, notes: string) {
  await ownedProspect(workspaceId, prospectId);
  await db.prospect.update({ where: { id: prospectId }, data: { notes: notes.slice(0, 5000) } });
}
