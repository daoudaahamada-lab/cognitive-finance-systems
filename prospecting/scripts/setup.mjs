// One-time installation on your own computer: dependencies, settings, database, browser for LinkedIn.
//   npm run setup
import { copyFileSync, existsSync } from "node:fs";
import { ensureDatabase, fail, run, setting } from "./lib.mjs";

const major = Number(process.versions.node.split(".")[0]);
if (major < 22) fail(`Node.js 22 ou plus récent est nécessaire (vous avez ${process.versions.node}) : https://nodejs.org`);

const step = (n, text) => console.log(`\n[${n}/5] ${text}`);

step(1, "Installation des dépendances (quelques minutes)…");
if (!run("npm", ["install"])) fail("L'installation des dépendances a échoué (voir le message ci-dessus).");

step(2, "Fichier de réglages .env");
if (existsSync(".env")) console.log("Déjà présent : conservé tel quel.");
else {
  copyFileSync(".env.example", ".env");
  console.log("Créé à partir de .env.example.");
}

step(3, "Base de données");
await ensureDatabase();
console.log("Base de données prête.");

step(4, "Création des tables");
let migrated = false;
for (let attempt = 0; attempt < 10 && !migrated; attempt++) {
  migrated = run("npx", ["prisma", "migrate", "deploy"]);
  // A freshly started database can refuse connections for a few seconds.
  if (!migrated) await new Promise((resolve) => setTimeout(resolve, 3000));
}
if (!migrated) fail("Les tables n'ont pas pu être créées (voir le message ci-dessus).");

step(5, "Navigateur utilisé pour LinkedIn (Chromium)");
const chromium = setting("LINKEDIN_CHROMIUM_PATH");
if (chromium && existsSync(chromium)) console.log(`Navigateur déjà configuré : ${chromium}`);
else if (!run("npx", ["playwright-core", "install", "chromium"])) fail("Le téléchargement de Chromium a échoué (voir le message ci-dessus).");

console.log("\n✓ Installation terminée. Pour lancer Vela : npm run local\n");
