// Captures de contrôle : node tools/preview.js out_dir t1 t2 ... (t en secondes ou ancre "beatId+off")
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [outDir, ...times] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto('file://' + path.resolve(__dirname, '../web/index.html'));
  await page.evaluate(() => window.READY);
  for (const te of times) {
    const t = await page.evaluate(x => (isNaN(+x) ? T(x) : +x), te);
    await page.evaluate(x => render(x), t);
    const name = `${outDir}/f_${t.toFixed(2).padStart(7, '0')}_${te.replace(/[^\w.+-]/g, '_')}.jpg`;
    await page.screenshot({ path: name, type: 'jpeg', quality: 80 });
    console.log(name);
  }
  if (errs.length) console.log('ERREURS:', errs.join('\n'));
  await browser.close();
})();
