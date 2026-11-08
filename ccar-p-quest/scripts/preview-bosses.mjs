// Page d'aperçu des boss V2 : chaque boss dans six états, avec ses zones de touche.
// Usage : node scripts/preview-bosses.mjs   → dist/dev/boss-preview.html
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const jsDir = join(root, "src", "v2", "js");
const files = ["00-core.js", ...readdirSync(jsDir).filter((f) => /^4\d-boss-.*\.js$/.test(f)).sort()];
const js = files.map((f) => `/* ---- ${f} ---- */\n` + readFileSync(join(jsDir, f), "utf8")).join("\n");
const html = readFileSync(join(root, "src", "v2", "dev", "boss-preview.html"), "utf8").replace("/*__JS__*/", () => js);
mkdirSync(join(root, "dist", "dev"), { recursive: true });
writeFileSync(join(root, "dist", "dev", "boss-preview.html"), html);
console.log(`Aperçu OK : ${files.length - 1} fichier(s) de boss → dist/dev/boss-preview.html`);
