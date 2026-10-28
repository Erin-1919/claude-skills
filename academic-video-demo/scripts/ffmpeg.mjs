// Resolve ffmpeg and ffprobe: PATH first, then the WinGet package folder (a fresh WinGet install is not on PATH
// until a new shell starts). Import { FFMPEG, FFPROBE } from the other scripts.
import { execFileSync } from "node:child_process";
import { existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

function resolve(name) {
  try { execFileSync(name, ["-version"], { stdio: "ignore" }); return name; } catch {}
  const pkgs = process.env.LOCALAPPDATA && join(process.env.LOCALAPPDATA, "Microsoft", "WinGet", "Packages");
  if (pkgs && existsSync(pkgs)) {
    for (const d of readdirSync(pkgs).filter((d) => d.startsWith("Gyan.FFmpeg"))) {
      for (const sub of readdirSync(join(pkgs, d))) {
        const exe = join(pkgs, d, sub, "bin", `${name}.exe`);
        if (existsSync(exe)) return exe;
      }
    }
  }
  throw new Error(`${name} not found: install it (Windows: winget install Gyan.FFmpeg) and retry`);
}

export const FFMPEG = resolve("ffmpeg");
export const FFPROBE = resolve("ffprobe");
export const duration = (file) => Number(execFileSync(FFPROBE, ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file]).toString());
