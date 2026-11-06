// Construit le jeu à partir de src/app.html et des niveaux content/level-XX.json.
// Sorties :
//   dist/index.html     page autonome (à ouvrir dans un navigateur ou à héberger)
//   dist/artifact.html  même page sans squelette HTML, pour la publication en Artifact claude.ai
// Usage : node scripts/build.mjs [--allow-partial]
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { loadLevels } from "./validate.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const allowPartial = process.argv.includes("--allow-partial");

const { levels, errors } = loadLevels();
if (errors.length) {
  console.error(errors.join("\n"));
  if (!allowPartial) {
    console.error(`\n${errors.length} erreur(s) : build arrêté. Corrige le contenu ou relance avec --allow-partial.`);
    process.exit(1);
  }
}
if (!allowPartial && levels.length !== 10) {
  console.error(`${levels.length} niveau(x) trouvé(s), 10 attendus. Relance avec --allow-partial pour construire quand même.`);
  process.exit(1);
}

const app = readFileSync(join(root, "src", "app.html"), "utf8");
const marker = "/*__CONTENT__*/null";
if (!app.includes(marker)) throw new Error("Marqueur de contenu introuvable dans src/app.html");
const json = JSON.stringify(levels).replace(/</g, "\\u003c").split(String.fromCharCode(0x2028)).join("\\u2028").split(String.fromCharCode(0x2029)).join("\\u2029");
const page = app.replace(marker, () => json);

const standalone =
  '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  "</head>\n<body>\n" + page + "\n</body>\n</html>\n";

mkdirSync(join(root, "dist"), { recursive: true });
writeFileSync(join(root, "dist", "index.html"), standalone);
writeFileSync(join(root, "dist", "artifact.html"), page);
const total = levels.reduce((s, l) => s + l.questions.length, 0);
console.log(`Build OK : ${levels.length} niveau(x), ${total} questions, ${(standalone.length / 1024).toFixed(0)} Ko → dist/index.html, dist/artifact.html`);
