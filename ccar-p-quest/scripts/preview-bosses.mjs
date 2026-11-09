// Page d'aperçu des boss : chaque boss dans 8 états, puis dans l'arène avec son décor.
// Usage :
//   node scripts/preview-bosses.mjs                    tous les boss → dist/dev/boss-preview.html
//   node scripts/preview-bosses.mjs 3 4                seulement les boss 3 et 4
//   node scripts/preview-bosses.mjs 3 4 --out mon.html nom du fichier produit dans dist/dev/
// Capture : node scripts/shot.cjs dist/dev/boss-preview.html capture.png [f=0.5]
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const jsDir = join(root, "src", "v2", "js");
const args = process.argv.slice(2);
const outIdx = args.indexOf("--out");
const outName = outIdx >= 0 ? args[outIdx + 1] : "boss-preview.html";
const only = args.filter((a, i) => /^\d+$/.test(a) && i !== outIdx + 1).map((n) => String(Number(n)).padStart(2, "0"));

const bossFiles = readdirSync(jsDir)
  .filter((f) => /^4\d-boss-\d\d\.js$/.test(f))
  .filter((f) => !only.length || only.includes(f.slice(8, 10)))
  .sort();
const files = ["00-core.js", "15-backdrop.js", ...bossFiles];
const js = files.map((f) => `/* ---- ${f} ---- */\n` + readFileSync(join(jsDir, f), "utf8")).join("\n");
const html = readFileSync(join(root, "src", "v2", "dev", "boss-preview.html"), "utf8").replace("/*__JS__*/", () => js);
mkdirSync(join(root, "dist", "dev"), { recursive: true });
writeFileSync(join(root, "dist", "dev", outName), html);
console.log(`Aperçu OK : ${bossFiles.length} boss → dist/dev/${outName}`);
