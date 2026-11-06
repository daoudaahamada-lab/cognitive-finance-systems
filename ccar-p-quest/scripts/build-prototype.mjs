// Construit le prototype V2 (combat au lance-pierre contre L'Injecteur, étage 7).
// Sorties :
//   dist/prototype-injecteur.html           page autonome
//   dist/prototype-injecteur.artifact.html  même page sans squelette HTML, pour la publication en Artifact
// Usage : node scripts/build-prototype.mjs
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { validateLevel } from "./validate.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const level = JSON.parse(readFileSync(join(root, "content", "level-07.json"), "utf8"));
const errors = validateLevel(level, 7);
if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}

const app = readFileSync(join(root, "src", "prototype-injecteur.html"), "utf8");
const marker = "/*__LEVEL__*/null";
if (!app.includes(marker)) throw new Error("Marqueur de contenu introuvable dans src/prototype-injecteur.html");
const json = JSON.stringify(level)
  .replace(/</g, "\\u003c")
  .split(String.fromCharCode(0x2028)).join("\\u2028")
  .split(String.fromCharCode(0x2029)).join("\\u2029");
const page = app.replace(marker, () => json);

const standalone =
  '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  "</head>\n<body>\n" + page + "\n</body>\n</html>\n";

mkdirSync(join(root, "dist"), { recursive: true });
writeFileSync(join(root, "dist", "prototype-injecteur.html"), standalone);
writeFileSync(join(root, "dist", "prototype-injecteur.artifact.html"), page);
console.log(`Prototype OK : ${level.questions.length} questions, ${(standalone.length / 1024).toFixed(0)} Ko → dist/prototype-injecteur.html`);
