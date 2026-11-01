// Review tool: render selected frames of the Explainer composition as PNG stills with a single bundle.
//   node scripts/stills.mjs <props.json> <out_dir> <frame> [<frame> ...]
// Used by `python3 -m pipeline.motion Vxx --stills F1 F2 ...` to check framings and overlays without a full render.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [propsPath, outDir, ...frames] = process.argv.slice(2);
if (!propsPath || !outDir || frames.length === 0) {
  console.error('usage: node scripts/stills.mjs <props.json> <out_dir> <frame> [<frame> ...]');
  process.exit(2);
}
// Default path in ONE place: ../browser.json (REMOTION_BROWSER_EXECUTABLE overrides it).
const browserExecutable =
  process.env.REMOTION_BROWSER_EXECUTABLE ??
  JSON.parse(fs.readFileSync(path.join(root, 'browser.json'), 'utf8')).executable;
if (!fs.existsSync(browserExecutable)) {
  console.error(`Rendering browser not found: ${browserExecutable}. Set REMOTION_BROWSER_EXECUTABLE (or fix motion/browser.json).`);
  process.exit(3);
}
const inputProps = JSON.parse(fs.readFileSync(propsPath, 'utf8'));
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public')});
const chromiumOptions = {gl: 'swiftshader'};
const composition = await selectComposition({
  serveUrl,
  id: 'Explainer',
  inputProps,
  browserExecutable,
  chromiumOptions,
  chromeMode: 'headless-shell',
});
for (const f of frames.map(Number)) {
  const output = path.join(outDir, `f${String(f).padStart(4, '0')}.png`);
  await renderStill({
    serveUrl,
    composition,
    frame: f,
    output,
    inputProps,
    imageFormat: 'png',
    browserExecutable,
    chromiumOptions,
    chromeMode: 'headless-shell',
    overwrite: true,
    timeoutInMilliseconds: 60000,
  });
  console.log(output);
}
