-- AlterTable
ALTER TABLE "LinkedInAccount" ADD COLUMN     "lastDiagnosedAt" TIMESTAMP(3),
ADD COLUMN     "lastDiagnosisOk" BOOLEAN,
ADD COLUMN     "lastError" TEXT,
ADD COLUMN     "lastErrorAt" TIMESTAMP(3);
