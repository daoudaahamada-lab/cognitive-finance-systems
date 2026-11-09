// Capture d'écran d'une page locale avec Chromium (outil de développement).
// Usage : node scripts/shot.cjs <page.html> <sortie.png> [ancre] [largeur] [attente en ms]
//   node scripts/shot.cjs dist/dev/boss-preview.html /tmp/boss.png          animation en cours
//   node scripts/shot.cjs dist/dev/boss-preview.html /tmp/boss.png f=0.5    boucles figées à 50 %
// Les erreurs JavaScript de la page sont affichées ; « no errors » sinon.
const path = require("path");
const { chromium } = require("playwright");
(async () => {
  const [file, out, hash, width, wait] = process.argv.slice(2);
  if (!file || !out) { console.error("Usage : node scripts/shot.cjs <page.html> <sortie.png> [ancre] [largeur] [attente ms]"); process.exit(1); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: Number(width) || 1950, height: 900 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push("console: " + m.text()); });
  await page.goto("file://" + path.resolve(file) + (hash ? "#" + hash : ""));
  await page.waitForTimeout(Number(wait) || 1500);
  await page.screenshot({ path: out, fullPage: true });
  console.log(errors.length ? errors.slice(0, 12).join("\n") : "no errors");
  await browser.close();
})();
