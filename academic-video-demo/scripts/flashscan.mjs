// Find transient bright frames (white flashes: a canvas cleared for one frame, a page that repaints white):
//   node flashscan.mjs <video.mp4> [--fps 30]
// A frame counts when more than 1 % of a 96x54 grey thumbnail is over 60 levels brighter than both neighbours.
// Expect 0; for each hit, look at the frames around the printed time.
import { spawnSync } from "node:child_process";
import { FFMPEG } from "./ffmpeg.mjs";

const file = process.argv[2];
const i = process.argv.indexOf("--fps"), fps = i < 0 ? 30 : Number(process.argv[i + 1]);
const W = 96, H = 54, N = W * H;
const buf = spawnSync(FFMPEG, ["-loglevel", "error", "-i", file, "-vf", `scale=${W}:${H},format=gray`, "-f", "rawvideo", "-"], { maxBuffer: 1 << 30 }).stdout;
const n = buf.length / N;
let hits = 0;
for (let f = 1; f < n - 1; f++) {
  let c = 0;
  for (let j = 0; j < N; j++) {
    const v = buf[f * N + j];
    if (v - buf[(f - 1) * N + j] > 60 && v - buf[(f + 1) * N + j] > 60) c++;
  }
  if (c > N * 0.01) { hits++; console.log(`flash at ${(f / fps).toFixed(2)} s (frame ${f}): ${c} cells`); }
}
console.log(`${hits} transient bright frames of ${n}`);
