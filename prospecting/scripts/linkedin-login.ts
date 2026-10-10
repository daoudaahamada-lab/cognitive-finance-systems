/**
 * Opens a visible Chromium on the account's profile so you can log into LinkedIn yourself
 * (password, 2FA, security check). The session is kept for the worker afterwards.
 * Needs a screen: run it on your own machine. Stop the worker first.
 *
 *   npm run linkedin:login -- --account <account id>
 */
export {};

process.env.LINKEDIN_HEADLESS = "false";
process.env.VELA_ROLE = "worker";

const { db } = await import("@/server/db");
const { localBrowserProvider } = await import("@/server/linkedin");
const { browserConfig } = await import("@/server/linkedin/browser/config");

const i = process.argv.indexOf("--account");
const accountId = i >= 0 ? process.argv[i + 1] : undefined;
const account = accountId ? await db.linkedInAccount.findUnique({ where: { id: accountId } }) : null;
if (!account || account.provider !== "browser") {
  console.log("Usage : npm run linkedin:login -- --account <id d'un compte navigateur>");
  process.exit(1);
}

const provider = localBrowserProvider();
try {
  await provider.sessions.withPage(account.externalId, async (page) => {
    await page.goto(`${browserConfig.baseUrl()}/login`);
    console.log("Connectez-vous dans la fenêtre Chromium (10 minutes maximum)…");
    await page.waitForURL((url) => url.pathname.startsWith("/feed"), { timeout: 10 * 60_000 });
  });
  const me = await provider.checkSession({ externalId: account.externalId });
  await db.linkedInAccount.update({ where: { id: account.id }, data: { fullName: me.name || account.fullName, headline: me.headline || account.headline, status: "ACTIVE", statusReason: null } });
  console.log(`Session enregistrée pour ${me.name} (/in/${me.slug}). Vous pouvez relancer le worker.`);
} finally {
  await provider.sessions.closeAll();
  await db.$disconnect();
}
