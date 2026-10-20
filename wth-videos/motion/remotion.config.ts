// Remotion CLI config (applies to `remotion render`, `remotion studio`, `remotion benchmark`).
// Docs: https://www.remotion.dev/docs/config
import {Config} from '@remotion/cli/config';

// Never let Remotion download Chrome Headless Shell from Google storage (blocked here):
// use the Playwright-provided headless shell that ships with the machine.
// Override with REMOTION_BROWSER_EXECUTABLE if the path changes.
const BROWSER =
  process.env.REMOTION_BROWSER_EXECUTABLE ??
  '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';

Config.setBrowserExecutable(BROWSER);
Config.setChromeMode('headless-shell');
// No GPU in the container: SwiftShader (CPU) WebGL/compositing. Plain DOM/CSS/<Img>
// does not need it, but it keeps any canvas/WebGL/filters deterministic.
Config.setChromiumOpenGlRenderer('swiftshader');
// Shared-memory capture needs Remotion's own patched headless shell
// ("Page.remotionCreateFramePool wasn't found" with the Playwright build). Skip the probe.
Config.setDisableSharedMemoryCapture(true);

// Output defaults (CLI flags still win).
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setPixelFormat('yuv420p');
Config.setCrf(18);
// Without this, JPEG frames give a full-range stream (ffprobe: yuvj420p, color_range=pc)
// that some players/apps show with washed-out or crushed blacks. bt709 = limited (tv) range
// yuv420p tagged BT.709, the safe choice for TikTok / Instagram / Facebook.
Config.setColorSpace('bt709');
Config.setOverwriteOutput(true);

// 4 vCPU / 15 GB RAM box: concurrency benchmarked 1..8 (see package.json render:test).
Config.setConcurrency(4);
// Large PNGs (1536x1024 RGBA, ~2 MB) + font loading: be generous with delayRender.
Config.setDelayRenderTimeoutInMilliseconds(60000);
