/**
 * Demo data: a workspace whose campaigns have been running for three weeks.
 * History is produced by the real engine and simulator replayed over past time,
 * so every number in the app is consistent.
 *
 *   npm run db:seed            (does nothing if the demo user already exists)
 */
export {};

// Set before the engine reads it: replayed history uses real-time delays.
process.env.TIME_SCALE = "1";

// Rule-based agents: replaying three weeks with Claude would mean hundreds of paid calls.
const { ruleAgents } = await import("@/server/agents");
const { hashPassword } = await import("@/server/auth/password");
const { db } = await import("@/server/db");
const { DAY, HOUR } = await import("@/server/domain/time");
const { runTick } = await import("@/server/engine/tick");
const { SimulatorProvider } = await import("@/server/linkedin/simulator/provider");

const DEMO_EMAIL = "demo@vela.local";
const DEMO_PASSWORD = "demo1234";
const DAYS_OF_HISTORY = 21;
const STEP = 2 * HOUR;

async function main() {
  if (await db.user.findUnique({ where: { email: DEMO_EMAIL } })) {
    console.log(`Demo user ${DEMO_EMAIL} already exists: nothing to do.`);
    return;
  }

  const start = new Date(Date.now() - DAYS_OF_HISTORY * DAY);
  const user = await db.user.create({
    data: { email: DEMO_EMAIL, name: "Alex Martin", passwordHash: await hashPassword(DEMO_PASSWORD), createdAt: start },
  });
  const workspace = await db.workspace.create({
    data: {
      name: "Clarity Finance",
      offer:
        "Nous automatisons le reporting financier des PME en connectant leur comptabilité et leur banque à un tableau de bord prêt pour le comité de direction. Mise en place en deux semaines, sans changer d'outil comptable.",
      persona: "DAF, CFO et dirigeants de PME de 20 à 500 salariés, SaaS ou conseil, en France et en Belgique.",
      bookingUrl: "https://cal.example.com/alex/20min",
      createdAt: start,
      members: { create: { userId: user.id, role: "OWNER" } },
    },
  });
  const account = await db.linkedInAccount.create({
    data: {
      workspaceId: workspace.id,
      provider: "simulator",
      externalId: `sim-acc-demo-${workspace.id}`,
      fullName: "Alex Martin",
      headline: "Fondateur @ Clarity Finance · Le reporting financier des PME, automatisé",
      accountType: "PREMIUM",
      // Demo account sends around the clock so the worker always has something to do.
      sendingDays: [1, 2, 3, 4, 5, 6, 7],
      sendingStart: "00:00",
      sendingEnd: "00:00",
      createdAt: start,
    },
  });

  const common = {
    workspaceId: workspace.id,
    accountId: account.id,
    offer: workspace.offer,
    persona: workspace.persona,
    bookingUrl: "",
    keywords: [],
    postUrls: [],
    companySizes: ["11-50", "51-200", "201-500"],
    inviteNote: null,
    followUps: [
      { delayDays: 3, template: "{{firstName}}, je me permets de remonter mon message. {Une idée de la réponse|Qu'en pensez-vous} ?" },
      { delayDays: 5, template: "{Dernier message de ma part|Je ne veux pas insister} {{firstName}} : si le sujet devient d'actualité chez {{company}}, je reste disponible." },
    ],
  };

  await db.campaign.create({
    data: {
      ...common,
      name: "DAF de PME SaaS · France",
      status: "ACTIVE",
      launchedAt: start,
      createdAt: start,
      sources: ["SEARCH", "SIGNALS"],
      signals: ["NEW_ROLE", "HIRING", "FUNDRAISING"],
      titles: ["CFO", "Directeur Administratif et Financier", "Contrôleur de gestion"],
      industries: ["Logiciels (SaaS)", "Conseil", "Services financiers"],
      locations: ["Paris", "Lyon", "Bordeaux", "Lille", "Nantes"],
      exclusions: ["Recrutement", "Stagiaire"],
      minScore: 55,
      weeklyProspectTarget: 150,
      firstMessage:
        "Merci d'avoir accepté mon invitation, {{firstName}} !\n\n{Je travaille avec|J'accompagne} des DAF de PME sur un point précis : le reporting mensuel qui prend encore plusieurs jours. Comment ça se passe chez {{company}} ?",
      setterMode: "AUTO",
    },
  });

  await db.campaign.create({
    data: {
      ...common,
      name: "Dirigeants · signaux de croissance",
      status: "ACTIVE",
      launchedAt: new Date(start.getTime() + 7 * DAY),
      createdAt: new Date(start.getTime() + 7 * DAY),
      sources: ["SIGNALS", "PROFILE_VISITORS"],
      signals: ["FUNDRAISING", "HIRING"],
      titles: ["CEO", "Fondateur", "Directeur Général"],
      industries: [],
      locations: ["Paris", "Bruxelles", "Genève"],
      exclusions: ["Recrutement"],
      minScore: 50,
      weeklyProspectTarget: 80,
      firstMessage:
        "Bonjour {{firstName}}, merci d'avoir accepté mon invitation. {Une levée de fonds|Une phase de recrutement|Une période de forte croissance}, c'est souvent le moment où le reporting financier devient un sujet. C'est le cas chez {{company}} ?",
      setterMode: "APPROVAL",
    },
  });

  await db.campaign.create({
    data: {
      ...common,
      name: "Experts-comptables partenaires",
      status: "DRAFT",
      sources: ["SEARCH"],
      signals: [],
      titles: ["Expert-comptable"],
      industries: ["Expertise comptable"],
      locations: ["Lyon"],
      exclusions: [],
      minScore: 60,
      weeklyProspectTarget: 50,
      firstMessage: "Merci d'avoir accepté mon invitation, {{firstName}}. Vous accompagnez des PME sur leur reporting ?",
      setterMode: "APPROVAL",
    },
  });

  const deps = (now: Date) => ({ db, agents: ruleAgents(), providerFor: () => new SimulatorProvider(db, 1), now });
  // Campaign 2 starts a week later: keep it paused until then.
  const second = await db.campaign.findFirstOrThrow({ where: { workspaceId: workspace.id, name: { startsWith: "Dirigeants" } } });
  await db.campaign.update({ where: { id: second.id }, data: { status: "PAUSED" } });

  let ticks = 0;
  for (let t = start.getTime(); t < Date.now(); t += STEP) {
    if (t >= second.launchedAt!.getTime()) {
      await db.campaign.updateMany({ where: { id: second.id, status: "PAUSED" }, data: { status: "ACTIVE" } });
    }
    const results = await runTick(deps(new Date(t)), { workspaceId: workspace.id });
    for (const r of results) if (r.error) throw new Error(r.error);
    if (++ticks % 24 === 0) process.stdout.write(`  ${Math.round(((t - start.getTime()) / (Date.now() - start.getTime())) * 100)}%\n`);
  }

  const [prospects, meetings, conversations] = await Promise.all([
    db.prospect.count({ where: { workspaceId: workspace.id } }),
    db.meeting.count({ where: { workspaceId: workspace.id } }),
    db.conversation.count({ where: { workspaceId: workspace.id } }),
  ]);
  console.log(`Seeded ${prospects} prospects, ${conversations} conversations, ${meetings} meetings.`);
  console.log(`Log in with ${DEMO_EMAIL} / ${DEMO_PASSWORD}`);
}

try {
  await main();
} finally {
  await db.$disconnect();
}
