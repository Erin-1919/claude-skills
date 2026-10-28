// Render an animated HTML scene to MP4, frame by frame:
//   node render_scene.mjs <scene.html> <seconds> <out.mp4> [--fps 30] [--size 1920x1080] [--scale 2]
// The scene defines window.sceneReady (a Promise) and window.seek(t) (t in seconds). Every frame is seeked, screenshot,
// and piped to ffmpeg, so the motion is exact whatever the machine's speed. Layout size times scale is the output size
// (1920x1080 at scale 2 gives 3840x2160). Needs Playwright with Chrome (npm i -D playwright; npx playwright install chrome).
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { FFMPEG } from "./ffmpeg.mjs";

const opt = (name, def) => { const i = process.argv.indexOf(`--${name}`); return i < 0 ? def : process.argv[i + 1]; };

export async function renderScene(scene, seconds, out, { fps = 30, width = 1920, height = 1080, scale = 2 } = {}) {
  mkdirSync(dirname(resolve(out)), { recursive: true });
  const browser = await chromium.launch({ channel: "chrome", args: ["--allow-file-access-from-files"] });
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: scale });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.goto(pathToFileURL(resolve(scene)).href);
  await page.evaluate(() => window.sceneReady);
  await page.evaluate(() => document.fonts.ready);

  const ff = spawn(FFMPEG, ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", String(fps), out],
    { stdio: ["pipe", "inherit", "inherit"] });
  const done = new Promise((ok, fail) => ff.on("close", (c) => (c === 0 ? ok() : fail(new Error(`ffmpeg exit ${c}`)))));

  const frames = Math.round(seconds * fps);
  for (let i = 0; i < frames; i++) {
    await page.evaluate((t) => window.seek(t), i / fps);
    const jpg = await page.screenshot({ type: "jpeg", quality: 95 });
    if (!ff.stdin.write(jpg)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % (fps * 5) === 0) process.stdout.write(`\r${scene}: ${i}/${frames}`);
  }
  ff.stdin.end();
  await done;
  await browser.close();
  process.stdout.write(`\r${scene}: ${frames}/${frames} -> ${out}\n`);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [scene, seconds, out] = process.argv.slice(2);
  const [width, height] = opt("size", "1920x1080").split("x").map(Number);
  await renderScene(scene, Number(seconds), out, { fps: Number(opt("fps", 30)), width, height, scale: Number(opt("scale", 2)) });
}
