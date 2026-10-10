-- AlterEnum
ALTER TYPE "ActivityType" ADD VALUE 'ACTION_FAILED';

-- AlterTable
ALTER TABLE "Campaign" ADD COLUMN     "searchUrl" TEXT NOT NULL DEFAULT '';

-- AlterTable
ALTER TABLE "LinkedInAccount" ADD COLUMN     "invitesPausedUntil" TIMESTAMP(3),
ADD COLUMN     "statusReason" TEXT;

