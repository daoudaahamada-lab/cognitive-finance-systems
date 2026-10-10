import type { ActivityType, Prisma } from "@prisma/client";
import type { Db } from "@/server/db";

export type ActivityInput = {
  workspaceId: string;
  type: ActivityType;
  campaignId?: string | null;
  prospectId?: string | null;
  accountId?: string | null;
  data?: Prisma.InputJsonValue;
  at: Date;
};

export function logActivity(db: Db | Prisma.TransactionClient, input: ActivityInput) {
  return db.activity.create({
    data: {
      workspaceId: input.workspaceId,
      type: input.type,
      campaignId: input.campaignId ?? null,
      prospectId: input.prospectId ?? null,
      accountId: input.accountId ?? null,
      data: input.data,
      createdAt: input.at,
    },
  });
}
