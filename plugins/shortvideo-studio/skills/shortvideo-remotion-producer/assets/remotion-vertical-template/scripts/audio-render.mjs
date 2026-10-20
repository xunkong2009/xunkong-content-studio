import {existsSync, renameSync, unlinkSync} from "node:fs";
import {join, parse} from "node:path";
import {spawnSync} from "node:child_process";
import {projectRoot} from "./project-lib.mjs";

export const audioMode = (clip) => clip.audio?.mode ?? "silent";

export const mixClipAudio = (manifest, clip, output) => {
  if (audioMode(clip) === "silent") return;
  const binary = process.env.FFMPEG_BINARY || "ffmpeg";
  const events = clip.audio.events;
  const args = ["-y", "-v", "error", "-i", output];
  for (const event of events) {
    const source = join(projectRoot, "public", event.src);
    if (!existsSync(source)) throw new Error(`Missing sound asset: ${source}`);
    args.push("-i", source);
  }
  const filters = events.map((event, i) => {
    const seconds = event.durationInFrames / manifest.video.fps;
    const fade = Math.min(.02, seconds / 4);
    const delay = Math.round(event.from / manifest.video.fps * 1000);
    return `[${i + 1}:a]atrim=duration=${seconds},asetpts=PTS-STARTPTS,afade=t=in:d=${fade},afade=t=out:st=${seconds - fade}:d=${fade},volume=${event.volume},adelay=${delay}:all=1[s${i}]`;
  });
  const duration = clip.durationInFrames / manifest.video.fps;
  filters.push(`${events.map((_, i) => `[s${i}]`).join("")}amix=inputs=${events.length}:normalize=0:dropout_transition=0,apad,atrim=duration=${duration},alimiter=limit=0.89:level=false:latency=true[out]`);
  const parsed = parse(output);
  const temporary = join(parsed.dir, `${parsed.name}.sound-mix.tmp${parsed.ext}`);
  args.push("-filter_complex", filters.join(";"), "-map", "0:v:0", "-map", "[out]", "-c:v", "copy", "-c:a", parsed.ext === ".webm" ? "libopus" : "aac", "-b:a", "128k", "-ar", "48000", "-t", String(duration), "-movflags", "+faststart", temporary);
  const result = spawnSync(binary, args, {cwd: projectRoot, encoding: "utf8"});
  if (result.status !== 0) {
    if (existsSync(temporary)) unlinkSync(temporary);
    throw new Error(`Sound mix failed (${binary}): ${result.stderr || result.error?.message || result.status}`);
  }
  renameSync(temporary, output);
  const stem = join(parsed.dir, `${parsed.name}.sfx.wav`);
  const extract = spawnSync(binary, ["-y", "-v", "error", "-i", output, "-map", "0:a:0", "-c:a", "pcm_s16le", stem], {encoding: "utf8"});
  if (extract.status !== 0) throw new Error(`SFX stem extraction failed: ${extract.stderr}`);
};
