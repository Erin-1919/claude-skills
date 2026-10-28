// Record a live web app off screen on a virtual clock, frame by frame, to MP4. A starting point: add the app's own
// steps (tabs, loading data, camera moves, chats) as methods or functions that call frame()/wait().
//
//   const s = await start({ url: "http://127.0.0.1:8000/", overlay: "overlay.js", ready: () => window.myApp?.ready });
//   await s.segment("tour", "frames/demo_tour.mp4");   // nothing before the first segment is recorded
//   await s.caption("What this shot shows"); await s.wait(3);
//   if (!s.wants("chats")) { await s.stop(); process.exit(0); }
//   await s.segment("chats", "frames/demo_chats.mp4");
//   ...; await s.stop();
//
// Run with --seg <name> to re-render one segment: the others run the clock without capture, so the page reaches the
// same state and the files join seamlessly (assemble.mjs, one part). Run with --stills <dir> to save a still per still().
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { FFMPEG } from "./ffmpeg.mjs";

const FPS = 30;
const realSleep = (s) => new Promise((r) => setTimeout(r, s * 1000));
const ease = (k) => (k < 0.5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2);
const arg = (name) => { const i = process.argv.indexOf(`--${name}`); return i < 0 ? null : process.argv[i + 1]; };

// width x height is the CSS layout (pick the size the app looks good at, e.g. 1440x810 for a laptop layout);
// scale makes the output 3840 wide (1440 * 8/3, 1920 * 2).
// ready: page function that is true once the app has loaded. settled: page function that is true once the current
// frame's data has arrived (default: no fetches in flight, counted by overlay.js). redraw: page function run before each
// capture, for canvases that need a nudge (see references/live-app-recording.md).
export async function start({ url, overlay, width = 1440, height = 810, scale = 3840 / 1440, ready = () => true,
  settled = () => (window.__inflight ?? 0) === 0, redraw = null } = {}) {
  const browser = await chromium.launch({ channel: "chrome", headless: true, args: ["--hide-scrollbars"] });
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: scale });
  if (overlay) await ctx.addInitScript({ path: resolve(overlay) });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  // paused, the page clock moves only when frame() moves it: timers, requestAnimationFrame, and CSS-free JS animation
  // all step exactly one frame at a time
  await page.clock.install({ time: new Date("2030-01-01T12:00:00Z") });
  await page.clock.pauseAt(new Date("2030-01-01T12:00:01Z"));
  await page.goto(url);
  const s = new Session(page, browser, { width, height, settled, redraw });
  await s.until(ready, null, 60);
  return s;
}

export class Session {
  constructor(page, browser, opts) {
    Object.assign(this, { page, browser, ...opts, mouse: { x: opts.width / 2, y: opts.height / 2 }, n: 0, frames: 0, rec: false, ff: null });
    this.stills = arg("stills");
    if (this.stills) mkdirSync(this.stills, { recursive: true });
  }

  wants(name) { const seg = arg("seg"); return !seg || seg === name; }

  // Close the open segment's file, if any, and start the named one: recorded into outFile when wanted.
  async segment(name, outFile) {
    await this.#close();
    console.error(`segment ${name} starts at clock frame ${this.n}`);
    if (!this.wants(name)) return;
    mkdirSync(dirname(resolve(outFile)), { recursive: true });
    this.ff = spawn(FFMPEG, ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
      "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", outFile], { stdio: ["pipe", "inherit", "inherit"] });
    this.rec = true;
  }

  async #close() {
    if (this.ff) { this.ff.stdin.end(); await new Promise((r) => this.ff.on("close", r)); this.ff = null; }
    this.rec = false;
  }

  // Advance the page clock by one frame; when recording, wait until the frame's data has arrived, then capture.
  // Waiting costs real time only, never video time, so slow servers and model calls leave no gaps.
  async frame() {
    const ms = Math.round((this.n + 1) * 1000 / FPS) - Math.round(this.n * 1000 / FPS);
    this.n++;
    await this.page.clock.runFor(ms);
    if (!this.rec) return;
    for (let i = 0; i < 600 && !(await this.page.evaluate(this.settled)); i++) await realSleep(0.03);
    if (this.redraw) await this.page.evaluate(this.redraw);
    const jpg = await this.page.screenshot({ type: "jpeg", quality: 94 });
    if (!this.ff.stdin.write(jpg)) await new Promise((r) => this.ff.stdin.once("drain", r));
    if (++this.frames % 300 === 0) console.error(`  ${this.frames / FPS} s rendered`);
  }

  async wait(secs) { for (let i = Math.round(secs * FPS); i > 0; i--) await this.frame(); }

  // Run the clock until fn(arg) holds in the page. Without capture the wait leaves no trace in the video.
  async until(fn, a = null, timeout = 60, { capture = false } = {}) {
    const t0 = Date.now();
    while (!(await this.page.evaluate(fn, a))) {
      if (Date.now() - t0 > timeout * 1000) throw new Error(`until timed out: ${fn}`);
      if (capture) await this.frame();
      else { const rec = this.rec; this.rec = false; await this.frame(); this.rec = rec; await realSleep(0.03); }
    }
  }

  async still(name) {
    if (this.stills && this.rec) await this.page.screenshot({ path: join(this.stills, `${name}.jpg`), type: "jpeg", quality: 85, scale: "css" });
  }

  // overlay.js: captions and panel highlights
  async caption(text, pos) { await this.page.evaluate(([t, p]) => window.__overlay.caption(t, p), [text, pos]); }
  async highlight(sel) { await this.page.evaluate((s) => window.__overlay.highlight(s), sel); }

  // a visible, eased mouse path, one step per frame; overlay.js draws the cursor and the click ripple
  async moveTo(x, y, secs = 0.6) {
    const { x: x0, y: y0 } = this.mouse, n = Math.max(4, Math.round(secs * FPS));
    for (let i = 1; i <= n; i++) {
      const e = ease(i / n);
      await this.page.mouse.move(x0 + (x - x0) * e, y0 + (y - y0) * e);
      await this.frame();
    }
    this.mouse = { x, y };
  }
  async clickAt(x, y, secs = 0.6) { await this.moveTo(x, y, secs); await this.wait(0.1); await this.page.mouse.click(x, y); await this.frame(); }
  async clickEl(selector, secs = 0.6) {
    const loc = this.page.locator(selector).first();
    await loc.scrollIntoViewIfNeeded();
    const b = await loc.boundingBox();
    if (!b) throw new Error(`no element ${selector}`);
    await this.clickAt(b.x + b.width / 2, b.y + b.height / 2, secs);
  }

  async stop() {
    console.error(`stopped at clock frame ${this.n}`);
    await this.#close();
    await this.browser.close();
    return `${this.frames} frames, ${(this.frames / FPS).toFixed(1)} s`;
  }
}
