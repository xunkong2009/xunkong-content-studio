import {renderArgs} from "./render-profile.mjs";
import {mixClipAudio} from "./audio-render.mjs";
import {mkdirSync} from "node:fs";
import {join} from "node:path";
import {spawnSync} from "node:child_process";
import {assertManifest, ensureRemotionCli, loadManifest, projectRoot, removeFilesWithExtension, remotionCli} from "./project-lib.mjs";

const manifest = loadManifest();
assertManifest(manifest);
ensureRemotionCli();

const rendersDir = join(projectRoot, "renders");
mkdirSync(rendersDir, {recursive: true});
for (const extension of [".mp4", ".mov", ".webm", ".wav"]) removeFilesWithExtension(rendersDir, extension);

for (const clip of manifest.clips) {
  const output = join(rendersDir, clip.fileName);
  const result = spawnSync(
    remotionCli,
    ["render", "src/index.ts", clip.compositionId, output, ...renderArgs(clip), "--muted", "--concurrency=2"],
    {cwd: projectRoot, stdio: "inherit"},
  );
  if (result.status !== 0) process.exit(result.status ?? 1);
  mixClipAudio(manifest, clip, output);
}
