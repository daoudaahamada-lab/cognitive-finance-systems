// Remotion CLI config (applies to `remotion render`, `remotion studio`, `remotion benchmark`).
// Docs: https://www.remotion.dev/docs/config
import {Config} from '@remotion/cli/config';
import fs from 'node:fs';
import path from 'node:path';

// Never let Remotion download Chrome Headless Shell from Google storage (blocked here):
// use the Playwright-provided headless shell that ships with the machine. The default path lives in ONE place,
// browser.json (also read by scripts/stills.mjs and pipeline/motion.py); REMOTION_BROWSER_EXECUTABLE overrides it.
const BROWSER =
  process.env.REMOTION_BROWSER_EXECUTABLE ??
  JSON.parse(fs.readFileSync(path.join(process.cwd(), 'browser.json'), 'utf8')).executable;
if (!fs.existsSync(BROWSER)) {
  throw new Error(`Rendering browser not found: ${BROWSER}. Set REMOTION_BROWSER_EXECUTABLE (or fix motion/browser.json).`);
}

Config.setBrowserExecutable(BROWSER);
Config.setChromeMode('headless-shell');
// No GPU in the container: SwiftShader (CPU) WebGL/compositing. Plain DOM/CSS/<Img>
// does not need it, but it keeps any canvas/WebGL/filters deterministic.
Config.setChromiumOpenGlRenderer('swiftshader');
// Shared-memory capture needs Remotion's own patched headless shell
// ("Page.remotionCreateFramePool wasn't found" with the Playwright build). Skip the probe.
Config.setDisableSharedMemoryCapture(true);

// Output defaults (CLI flags still win).
// Lossless PNG frames: JPEG (even at q92) subsampled the red accent and the caption edges to 4:2:0 once
// before x264 did it again (caption band 35.9 dB -> 34.0 dB). PNG costs ~30-50 % more render time.
Config.setVideoImageFormat('png');
Config.setCodec('h264');
Config.setPixelFormat('yuv420p');
// CRF 15: holds stay clean (at CRF 18 the 250-frame GOP refresh made still frames shimmer by up to 13 levels).
Config.setCrf(15);
// bt709 = limited (tv) range yuv420p tagged BT.709, the safe choice for TikTok / Instagram / Facebook
// (without it, players may show washed-out or crushed blacks).
Config.setColorSpace('bt709');
Config.setOverwriteOutput(true);

// Keyframes on shot changes (pipeline/motion.py passes them in WTH_KEYFRAMES, seconds, comma-separated):
// the I-frame refresh then lands inside a handover burst, never in a still hold. With shots < 250 frames
// apart, x264's periodic keyframe (keyint 250, counted from the last IDR) never falls inside a hold either.
const KEYFRAMES = process.env.WTH_KEYFRAMES ?? '';
Config.overrideFfmpegCommand(({type, args}) => {
  if (process.env.WTH_DEBUG_FFMPEG) console.log(`[ffmpeg ${type}]`, JSON.stringify(args));
  if (!KEYFRAMES || !args.includes('libx264')) return args;
  const out = [...args];
  out.splice(out.length - 1, 0, '-force_key_frames', KEYFRAMES);
  return out;
});

// 4 vCPU / 15 GB RAM box: concurrency benchmarked 1..8 (see package.json render:test).
Config.setConcurrency(4);
// Large PNGs (1536x1024 RGBA, ~2 MB) + font loading: be generous with delayRender.
Config.setDelayRenderTimeoutInMilliseconds(60000);
