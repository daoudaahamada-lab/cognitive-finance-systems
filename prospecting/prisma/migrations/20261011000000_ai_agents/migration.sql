-- AlterTable
ALTER TABLE "Campaign" ADD COLUMN     "aiPersonalization" BOOLEAN NOT NULL DEFAULT true;

-- AlterTable
ALTER TABLE "Draft" ADD COLUMN     "author" TEXT NOT NULL DEFAULT 'rules';

-- AlterTable
ALTER TABLE "Prospect" ADD COLUMN     "scoreSummary" TEXT,
ADD COLUMN     "scoredBy" TEXT;

