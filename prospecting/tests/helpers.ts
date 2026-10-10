import type { AccountType, Prisma, SetterMode } from "@prisma/client";
import { ruleAgents } from "@/server/agents";
import { db } from "@/server/db";
import type { EngineDeps } from "@/server/engine/deps";
import { SimulatorProvider } from "@/server/linkedin/simulator/provider";
import { assertTestDatabase } from "./global-setup";

export { db };

export async function resetDb() {
  assertTestDatabase(process.env.DATABASE_URL ?? "");
  const tables = await db.$queryRaw<{ tablename: string }[]>`
    SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename <> '_prisma_migrations'`;
  if (tables.length === 0) return;
  await db.$executeRawUnsafe(`TRUNCATE ${tables.map((t) => `"${t.tablename}"`).join(", ")} CASCADE`);
}

export function deps(now: Date): EngineDeps {
  return { db, agents: ruleAgents(), providerFor: () => new SimulatorProvider(db, 1), now };
}

export async function createWorkspace(options: { accountType?: AccountType; allWeek?: boolean } = {}) {
  const workspace = await db.workspace.create({
    data: {
      name: "Test",
      offer: "Nous automatisons le reporting financier des PME. Le tout en 2 semaines.",
      bookingUrl: "https://cal.example.com/demo",
    },
  });
  const account = await db.linkedInAccount.create({
    data: {
      workspaceId: workspace.id,
      provider: "simulator",
      externalId: `sim-acc-${workspace.id}`,
      fullName: "Alex Martin",
      accountType: options.accountType ?? "FREE",
      ...(options.allWeek === false
        ? {}
        : { sendingDays: [1, 2, 3, 4, 5, 6, 7], sendingStart: "00:00", sendingEnd: "00:00" }),
    },
  });
  return { workspace, account };
}

export async function createCampaign(
  workspaceId: string,
  accountId: string,
  overrides: Partial<Prisma.CampaignUncheckedCreateInput> & { setterMode?: SetterMode } = {},
) {
  return db.campaign.create({
    data: {
      workspaceId,
      accountId,
      name: "CFO PME",
      status: "ACTIVE",
      sources: ["SEARCH", "SIGNALS"],
      titles: ["CFO", "Directeur Administratif et Financier"],
      industries: ["Logiciels (SaaS)", "Conseil"],
      locations: ["Paris", "Lyon"],
      companySizes: [],
      keywords: [],
      signals: [],
      postUrls: [],
      exclusions: ["Recrutement"],
      minScore: 50,
      weeklyProspectTarget: 150,
      offer: "Nous automatisons le reporting financier des PME.",
      inviteNote: "Bonjour {{firstName}}, ravi d'échanger avec vous.",
      firstMessage: "{Bonjour|Hello} {{firstName}}, merci pour la connexion ! Comment gérez-vous le reporting chez {{company}} ?",
      followUps: [
        { delayDays: 3, template: "{{firstName}}, je me permets de relancer." },
        { delayDays: 4, template: "Dernière relance {{firstName}} !" },
      ],
      setterMode: "AUTO",
      bookingUrl: "https://cal.example.com/demo",
      ...overrides,
    },
  });
}
