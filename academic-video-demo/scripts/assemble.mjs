// Join rendered parts into the final video:   node assemble.mjs <spec.json>
// spec: { "out": "final.mp4", "fade": 0.6, "size": "3840x2160", "fps": 30, "parts": [["intro.mp4"], ["demo_tour.mp4", "demo_chats.mp4"], ["close.mp4"]] }
// Files inside one part are segments of one continuous recording and join with a hard cut; parts join with a crossfade.
// Durations come from ffprobe, so a part that grows or shrinks needs no change here. Paths resolve against the spec's folder.
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { FFMPEG, duration } from "./ffmpeg.mjs";

const specPath = resolve(process.argv[2]);
const spec = JSON.parse(readFileSync(specPath, "utf8"));
const at = (p) => resolve(dirname(specPath), p);
const FADE = spec.fade ?? 0.6, FPS = spec.fps ?? 30, [W, H] = (spec.size ?? "3840x2160").split("x");
const groups = spec.parts.map((g) => g.map(at));
const files = groups.flat();

let fc = files.map((_, i) => `[${i}:v]scale=${W}:${H}:flags=lanczos,fps=${FPS},setsar=1,format=yuv420p[s${i}]`).join(";");
let k = 0;
const lens = groups.map((g, j) => {
  fc += `;${g.map(() => `[s${k++}]`).join("")}concat=n=${g.length}:v=1:a=0[p${j}]`;
  return g.reduce((t, f) => t + duration(f), 0);
});
let prev = "p0", acc = lens[0];
for (let i = 1; i < lens.length; i++) {
  const lab = `x${i}`;
  fc += `;[${prev}][p${i}]xfade=transition=fade:duration=${FADE}:offset=${(acc - FADE).toFixed(3)}[${lab}]`;
  acc += lens[i] - FADE; prev = lab;
}
const out = at(spec.out);
const r = spawnSync(FFMPEG, ["-y", "-loglevel", "error", ...files.flatMap((p) => ["-i", p]), "-filter_complex", fc, "-map", `[${prev}]`,
  "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", out], { stdio: "inherit" });
if (r.status !== 0) throw new Error(`ffmpeg exited ${r.status}`);
console.log(`${out}: ${duration(out).toFixed(1)} s`);
let t = 0;
for (const [i, len] of lens.entries()) { console.log(`  part ${i + 1} starts at ${t.toFixed(1)} s`); t += len - FADE; }
