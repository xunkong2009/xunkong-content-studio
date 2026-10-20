import {profileFor} from "./render-profile.mjs";
import {audioMode} from "./audio-render.mjs";
import {spawnSync} from "node:child_process";
import {createRequire} from "node:module";
import {existsSync, readdirSync, statSync, writeFileSync} from "node:fs";
import {join} from "node:path";
import {assertManifest, loadManifest, projectRoot} from "./project-lib.mjs";

const require = createRequire(import.meta.url);
const ffprobe = require("ffprobe-static").path;
const manifest = loadManifest();
assertManifest(manifest);

const rendersDir = join(projectRoot, "renders");
const actual = existsSync(rendersDir) ? readdirSync(rendersDir).filter((file) => /\.(mp4|mov|webm)$/.test(file)).sort() : [];
const expected = manifest.clips.map((clip) => clip.fileName).sort();
if (JSON.stringify(actual) !== JSON.stringify(expected)) {
  console.error(`Rendered video set does not match manifest. Expected ${expected.join(", ")}; found ${actual.join(", ")}`);
  process.exit(1);
}

const parseRate = (rate) => {
  const [numerator, denominator] = rate.split("/").map(Number);
  return numerator / denominator;
};

const reports = [];
for (const clip of manifest.clips) {
  const file = join(rendersDir, clip.fileName);
  if (statSync(file).size < 1024) {
    console.error(`${clip.fileName} is unexpectedly small`);
    process.exit(1);
  }

  const result = spawnSync(
    ffprobe,
    ["-v", "error", "-show_entries", "stream=codec_type,codec_name,pix_fmt,width,height,r_frame_rate:stream_tags:format=duration,size", "-of", "json", file],
    {encoding: "utf8"},
  );
  if (result.status !== 0) {
    console.error(`ffprobe failed for ${clip.fileName}`);
    process.exit(result.status ?? 1);
  }

  const data = JSON.parse(result.stdout);
  const stream = data.streams?.find((item) => item.codec_type === "video");
  const duration = Number(data.format?.duration);
  const expectedDuration = clip.durationInFrames / manifest.video.fps;
  const failures = [];
  const audio = data.streams?.filter((item) => item.codec_type === "audio") ?? [];
  const expectsAudio = audioMode(clip) === "sfx";
  if (!expectsAudio && audio.length) failures.push("unexpected audio stream in silent motion clip");
  if (expectsAudio && (audio.length !== 1 || audio[0].codec_name !== (profileFor(clip) === "vp9-alpha" ? "opus" : "aac"))) failures.push("sfx clip requires AAC or WebM Opus matching profile");
  const profile = profileFor(clip);
  const expectedCodec = profile === "prores-alpha" ? "prores" : profile === "vp9-alpha" ? "vp9" : "h264";
  if (stream?.codec_name !== expectedCodec) failures.push(`codec=${stream?.codec_name}`);
  if (profile === "prores-alpha" && !stream?.pix_fmt?.startsWith("yuva")) failures.push("ProRes alpha missing");
  if (profile === "vp9-alpha" && String(stream?.tags?.alpha_mode ?? stream?.tags?.ALPHA_MODE ?? "0") !== "1" && !stream?.pix_fmt?.startsWith("yuva")) failures.push("VP9 alpha metadata missing");
  if (expectsAudio && !existsSync(file.replace(/\.(mp4|mov|webm)$/, ".sfx.wav"))) failures.push("Missing separate SFX stem");
  if (stream?.width !== manifest.video.width || stream?.height !== manifest.video.height) failures.push(`size=${stream?.width}x${stream?.height}`);
  if (Math.abs(parseRate(stream?.r_frame_rate ?? "0/1") - manifest.video.fps) > 0.01) failures.push(`fps=${stream?.r_frame_rate}`);
  if (!Number.isFinite(duration) || Math.abs(duration - expectedDuration) > 0.2) failures.push(`duration=${duration}`);
  if (failures.length > 0) {
    console.error(`${clip.fileName} failed verification: ${failures.join(", ")}`);
    process.exit(1);
  }

  reports.push({fileName: clip.fileName, codec: stream.codec_name, width: stream.width, height: stream.height, fps: manifest.video.fps, duration, audio: expectsAudio, audioMode: audioMode(clip)});
  console.log(`${clip.fileName}: ${stream.codec_name} ${stream.width}x${stream.height} ${manifest.video.fps}fps ${duration.toFixed(2)}s ${audioMode(clip)}`);
}

writeFileSync(join(rendersDir, "media-verification.json"), JSON.stringify({passed: true, clips: reports}, null, 2) + "\n");
