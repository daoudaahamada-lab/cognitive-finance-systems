import type { Locator, Page } from "playwright-core";
import { browserConfig } from "./config";

function wait(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/** A random pause, scaled by LINKEDIN_PACE (0 in tests). */
export async function pause(minMs: number, maxMs: number) {
  const pace = browserConfig.pace();
  if (pace === 0) return;
  await wait((minMs + Math.random() * (maxMs - minMs)) * pace);
}

/** Types like a person: per-key delays, Shift+Enter between lines (Enter may send). */
export async function typeHuman(page: Page, target: Locator, text: string) {
  await target.click();
  await pause(300, 900);
  const pace = browserConfig.pace();
  const lines = text.split("\n");
  for (const [i, line] of lines.entries()) {
    if (pace === 0) await page.keyboard.insertText(line);
    else await page.keyboard.type(line, { delay: (35 + Math.random() * 60) * pace });
    if (i < lines.length - 1) await page.keyboard.press("Shift+Enter");
  }
  await pause(500, 1500);
}

/** Scrolls a little, the way someone reading a profile would. */
export async function browse(page: Page) {
  if (browserConfig.pace() === 0) return;
  await page.mouse.wheel(0, 300 + Math.random() * 500);
  await pause(800, 2500);
  await page.mouse.wheel(0, -(200 + Math.random() * 300));
  await pause(400, 1200);
}
