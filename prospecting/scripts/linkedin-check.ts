/**
 * Read-only diagnosis of a browser LinkedIn account: session, search, profile buttons,
 * connections and messages. Nothing is sent. Stop the worker first (it holds the browser profile).
 *
 *   npm run linkedin:check -- --account <account id> [--campaign <campaign id>]
 */
export {};

const { db } = await import("@/server/db");
const { localBrowserProvider } = await import("@/server/linkedin");
const { diagnosticQuery } = await import("@/server/services/accounts");

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
}

const accountId = arg("account");
const accounts = await db.linkedInAccount.findMany({ where: { provider: "browser" }, select: { id: true, fullName: true, status: true } });
if (!accountId) {
  console.log("Usage : npm run linkedin:check -- --account <id> [--campaign <id>]\nComptes navigateur :");
  for (const a of accounts) console.log(`  ${a.id}  ${a.fullName} (${a.status})`);
  process.exit(1);
}
const account = await db.linkedInAccount.findUnique({ where: { id: accountId } });
if (!account || account.provider !== "browser") throw new Error("Compte navigateur introuvable.");
const campaignId = arg("campaign");
const campaign = campaignId ? await db.campaign.findUnique({ where: { id: campaignId } }) : await db.campaign.findFirst({ where: { accountId } });

const provider = localBrowserProvider();
try {
  const report = await provider.diagnose({ externalId: account.externalId }, diagnosticQuery(campaign));
  for (const line of report) console.log(`${line.ok ? "✓" : "✗"} ${line.check.padEnd(18)} ${line.detail}`);
  const failed = report.filter((l) => !l.ok).length;
  console.log(failed ? `\n${failed} point(s) à vérifier : LinkedIn a peut-être changé son interface (voir src/server/linkedin/browser/selectors.ts).` : "\nTout est reconnu.");
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(/ProcessSingleton|SingletonLock|already in use/i.test(message) ? "Le profil navigateur est déjà ouvert : arrêtez le worker pendant le diagnostic." : `Échec : ${message}`);
  process.exitCode = 1;
} finally {
  await provider.sessions.closeAll();
  await db.$disconnect();
}
