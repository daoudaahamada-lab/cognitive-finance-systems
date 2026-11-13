// Rendu image par image : Chromium (Playwright) -> JPEG -> ffmpeg (H.264), en parallèle par tronçons.
// Usage : node tools/render.js [--workers 4] [--from s] [--to s] [--out build/video_noaudio.mp4]
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => (v.startsWith('--') ? a.concat([[v.slice(2), arr[i + 1]]]) : a), []));
const ROOT = path.resolve(__dirname, '..');
const TL = JSON.parse(fs.readFileSync(path.join(ROOT, 'build/timeline.json'), 'utf8'));
const FPS = 25;
const WORKERS = parseInt(args.workers || '4', 10);
const T0 = parseFloat(args.from || '0');
const T1 = parseFloat(args.to || String(TL.duration + 0.5));
const OUT = path.resolve(ROOT, args.out || 'build/video_noaudio.mp4');
const CHUNKDIR = path.join(ROOT, 'build/chunks');
fs.mkdirSync(CHUNKDIR, { recursive: true });

const f0 = Math.round(T0 * FPS), f1 = Math.ceil(T1 * FPS);
const total = f1 - f0;
const per = Math.ceil(total / WORKERS);

async function worker(k) {
  const a = f0 + k * per, b = Math.min(f1, a + per);
  if (a >= b) return null;
  const out = path.join(CHUNKDIR, `chunk_${String(k).padStart(2, '0')}.mp4`);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  await page.goto('file://' + path.join(ROOT, 'web/index.html'));
  await page.evaluate(() => window.READY);
  const t0 = Date.now();
  for (let f = a; f < b; f++) {
    await page.evaluate(t => render(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - a) % 500 === 0) console.log(`[w${k}] ${f - a}/${b - a} images, ${((Date.now() - t0) / Math.max(1, f - a)).toFixed(0)} ms/image`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  if (errs.length) console.log(`[w${k}] erreurs page :`, errs);
  return out;
}

(async () => {
  console.log(`Rendu ${total} images (${(total / FPS).toFixed(1)} s) avec ${WORKERS} processus`);
  const t = Date.now();
  const chunks = (await Promise.all([...Array(WORKERS).keys()].map(worker))).filter(Boolean);
  const list = path.join(CHUNKDIR, 'list.txt');
  fs.writeFileSync(list, chunks.map(c => `file '${c}'`).join('\n'));
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', OUT]);
  console.log(`Terminé en ${((Date.now() - t) / 60000).toFixed(1)} min -> ${OUT}`);
})();
