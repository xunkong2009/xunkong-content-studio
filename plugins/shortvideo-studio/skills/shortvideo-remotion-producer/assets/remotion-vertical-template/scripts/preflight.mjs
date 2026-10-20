import {validateVisualAssets} from "./visual-assets.mjs";
import {existsSync, readFileSync} from "node:fs";
import {isAbsolute, join, resolve} from "node:path";
import {assertManifest, loadManifest, projectRoot} from "./project-lib.mjs";

const manifest = loadManifest();
assertManifest(manifest);
const assetErrors = validateVisualAssets(manifest, {projectRoot});
if (assetErrors.length) {
  for (const error of assetErrors) console.error(error);
  process.exit(1);
}

const registry = readFileSync(join(projectRoot, "src", "clip-registry.tsx"), "utf8");
const missing = manifest.clips.filter((clip) => !new RegExp(`\\b${clip.compositionId}\\b`).test(registry));
if (missing.length > 0) {
  console.error(`Missing registry entries: ${missing.map((clip) => clip.compositionId).join(", ")}`);
  process.exit(1);
}

const sourcePath = isAbsolute(manifest.sourceScript) ? manifest.sourceScript : resolve(projectRoot, manifest.sourceScript);
const sourceText = existsSync(sourcePath) ? readFileSync(sourcePath, "utf8") : manifest.sourceScript;
if ((manifest.schemaVersion ?? 1) === 2) {
  for (const clip of manifest.clips) {
    if (!sourceText.includes(clip.scriptExcerpt)) {
      console.error(`${clip.beatId}: scriptExcerpt must occur unchanged in sourceScript`);
      process.exit(1);
    }
  }
}
const corpus = [manifest.projectTitle, manifest.topicKey, sourceText, ...manifest.clips.flatMap((clip) => [clip.title, clip.scriptExcerpt, clip.compositionId, clip.fileName])].join("\n").toLowerCase();
const missingScopeTerms = manifest.scopeTerms.filter((term) => !corpus.includes(term.toLowerCase()));
const forbiddenTerms = manifest.forbiddenCarryoverTerms.filter((term) => corpus.includes(term.toLowerCase()));
if (missingScopeTerms.length > 0 || forbiddenTerms.length > 0) {
  if (missingScopeTerms.length > 0) console.error(`Scope terms missing from project content: ${missingScopeTerms.join(", ")}`);
  if (forbiddenTerms.length > 0) console.error(`Forbidden carryover terms found: ${forbiddenTerms.join(", ")}`);
  process.exit(1);
}

for (const clip of manifest.clips) {
  for (const event of clip.audio?.events ?? []) {
    if (!existsSync(join(projectRoot, "public", event.src))) {
      console.error(`${clip.beatId}: missing sound asset public/${event.src}`);
      process.exit(1);
    }
  }
}
const seconds = manifest.clips.map((clip) => `${clip.beatId}:${(clip.durationInFrames / manifest.video.fps).toFixed(1)}s`);
console.log(`Preflight passed: ${manifest.projectTitle}`);
console.log(`Topic: ${manifest.topicKey}`);
console.log(`Clips: ${seconds.join(", ")}`);
console.log(`Video: ${manifest.video.width}x${manifest.video.height} @ ${manifest.video.fps}fps`);
