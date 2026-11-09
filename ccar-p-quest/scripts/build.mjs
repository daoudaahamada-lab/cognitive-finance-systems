// Construit le jeu V2 à partir de src/v2/ et des niveaux content/level-XX.json.
// Sorties :
//   dist/index.html     page autonome (à ouvrir dans un navigateur ou à héberger)
//   dist/artifact.html  même page sans squelette HTML, pour la publication en Artifact claude.ai
// Usage : node scripts/build.mjs [--allow-partial]
import { execSync } from "node:child_process";
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
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

const src = join(root, "src", "v2");
const jsFiles = readdirSync(join(src, "js")).filter((f) => f.endsWith(".js")).sort();
// --stable-bosses : prend les fichiers de boss du dernier commit (utile pendant qu'ils sont en cours de refonte).
const stable = process.argv.includes("--stable-bosses");
const readJs = (f) => (stable && /^4\d-boss-/.test(f)
  ? execSync(`git show HEAD:./src/v2/js/${f}`, { cwd: root, encoding: "utf8", maxBuffer: 1 << 24 })
  : readFileSync(join(src, "js", f), "utf8"));
const js = jsFiles.map((f) => `/* ---- ${f} ---- */\n` + readJs(f)).join("\n");
const css = readFileSync(join(src, "styles.css"), "utf8");
const shell = readFileSync(join(src, "shell.html"), "utf8");
for (const m of ["/*__CSS__*/", "/*__CONTENT__*/null", "/*__JS__*/"]) if (!shell.includes(m)) throw new Error("Marqueur manquant dans shell.html : " + m);

const json = JSON.stringify(levels)
  .replace(/</g, "\\u003c")
  .split(String.fromCharCode(0x2028)).join("\\u2028")
  .split(String.fromCharCode(0x2029)).join("\\u2029");
const page = shell.replace("/*__CSS__*/", () => css).replace("/*__CONTENT__*/null", () => json).replace("/*__JS__*/", () => js);

const standalone =
  '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  "</head>\n<body>\n" + page + "\n</body>\n</html>\n";

mkdirSync(join(root, "dist"), { recursive: true });
writeFileSync(join(root, "dist", "index.html"), standalone);
writeFileSync(join(root, "dist", "artifact.html"), page);
const total = levels.reduce((s, l) => s + l.questions.length, 0);
console.log(`Build OK : ${levels.length} niveau(x), ${total} questions, ${jsFiles.length} fichiers JS, ${(standalone.length / 1024).toFixed(0)} Ko → dist/index.html, dist/artifact.html`);
