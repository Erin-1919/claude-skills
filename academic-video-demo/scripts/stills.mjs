// Contact sheets for review, in seconds instead of a full render.
//   node stills.mjs scene <scene.html> <out.png> t1 t2 ...   seeks an HTML scene (layout 1920x1080) to each time
//   node stills.mjs video <file.mp4>   <out.png> t1 t2 ...   grabs frames from a rendered video
// Tiles the shots two per row at 960 px each and writes one PNG; open it and read every shot before rendering.
// Look for: overlaps, clipped or tiny text, elements visible before their cue, hard edges, captions that collide.
import { chromium } from "playwright";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { FFMPEG } from "./ffmpeg.mjs";

const [mode, src, out, ...times] = process.argv.slice(2);
if (!["scene", "video"].includes(mode) || !times.length) {
  console.error("usage: node stills.mjs scene|video <src> <out.png> t1 t2 ...");
  process.exit(1);
}
const tmp = mkdtempSync(join(tmpdir(), "stills-"));
const shots = times.map((t, i) => join(tmp, `s${i}.png`));

if (mode === "scene") {
  const b = await chromium.launch({ channel: "chrome", args: ["--allow-file-access-from-files"] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on("pageerror", (e) => console.error("pageerror:", e.message));
  await p.goto(pathToFileURL(resolve(src)).href);
  await p.evaluate(() => window.sceneReady);
  for (const [i, t] of times.entries()) { await p.evaluate((t) => window.seek(t), Number(t)); await p.screenshot({ path: shots[i] }); }
  await b.close();
} else {
  for (const [i, t] of times.entries()) {
    const r = spawnSync(FFMPEG, ["-y", "-loglevel", "error", "-ss", t, "-i", src, "-frames:v", "1", "-vf", "scale=1920:-2", shots[i]]);
    if (r.status !== 0) throw new Error(r.stderr.toString());
  }
}

// two per row; an odd count gets a black last tile
const n = shots.length, cols = Math.min(2, n), rows = Math.ceil(n / cols);
const inputs = shots.flatMap((s) => ["-i", s]);
let fc = shots.map((_, i) => `[${i}:v]scale=960:540,setsar=1[t${i}]`).join(";");
const tiles = shots.map((_, i) => `[t${i}]`);
if (n % cols) { fc += `;color=black:s=960x540:d=1[pad]`; tiles.push("[pad]"); }
const layout = tiles.map((_, i) => `${(i % cols) * 960}_${Math.floor(i / cols) * 540}`).join("|");
fc += tiles.length > 1 ? `;${tiles.join("")}xstack=inputs=${tiles.length}:layout=${layout}:fill=black[o]` : `;${tiles[0]}null[o]`;
const r = spawnSync(FFMPEG, ["-y", "-loglevel", "error", ...inputs, "-filter_complex", fc, "-map", "[o]", "-frames:v", "1", out]);
rmSync(tmp, { recursive: true, force: true });
if (r.status !== 0) throw new Error(r.stderr.toString());
console.log(`${out}: ${n} shots, ${rows} rows`);
