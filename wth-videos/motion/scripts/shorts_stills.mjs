// Review tool: PNG stills of the "Short" composition, one bundle for several shorts.
//   node scripts/shorts_stills.mjs <out_dir> <f1,f2,...> <props1.json> [<props2.json> ...]
// Writes <out_dir>/<id>_f0123.png (id = props.id). Used by `python3 -m pipeline.shorts --stills "0 60 ..."`.
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [outDir, frameList, ...propsFiles] = process.argv.slice(2);
if (!outDir || !frameList || propsFiles.length === 0) {
  console.error('usage: node scripts/shorts_stills.mjs <out_dir> <f1,f2,...> <props.json> [...]');
  process.exit(2);
}
const browserExecutable =
  process.env.REMOTION_BROWSER_EXECUTABLE ?? JSON.parse(fs.readFileSync(path.join(root, 'browser.json'), 'utf8')).executable;
if (!fs.existsSync(browserExecutable)) {
  console.error(`Rendering browser not found: ${browserExecutable}. Set REMOTION_BROWSER_EXECUTABLE (or fix motion/browser.json).`);
  process.exit(3);
}
const frames = frameList.split(',').map(Number);
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public')});
const chromiumOptions = {gl: 'swiftshader'};
for (const p of propsFiles) {
  const inputProps = JSON.parse(fs.readFileSync(p, 'utf8'));
  const composition = await selectComposition({serveUrl, id: 'Short', inputProps, browserExecutable, chromiumOptions, chromeMode: 'headless-shell'});
  for (const f of frames) {
    const output = path.join(outDir, `${inputProps.id}_f${String(f).padStart(4, '0')}.png`);
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
}
