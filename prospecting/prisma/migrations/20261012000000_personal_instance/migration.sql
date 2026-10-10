-- AlterTable
ALTER TABLE "Workspace" DROP COLUMN "plan",
DROP COLUMN "trialEndsAt";

-- DropEnum
DROP TYPE "Plan";

