import {spawnSync} from "node:child_process";
import {existsSync, unlinkSync} from "node:fs";
import {join} from "node:path";
import {assertManifest, loadManifest, projectRoot} from "./project-lib.mjs";

const manifest = loadManifest();
assertManifest(manifest);
const rendersDir = join(projectRoot, "renders");
const files = manifest.clips.flatMap((clip) => [join(rendersDir, clip.fileName), ...(clip.audio?.mode === "sfx" ? [join(rendersDir, clip.fileName.replace(/\.(mp4|mov|webm)$/, ".sfx.wav"))] : [])]);
for (const file of files) {
  if (!existsSync(file)) {
    console.error(`Missing rendered file: ${file}`);
    process.exit(1);
  }
}

const archive = join(rendersDir, `${manifest.topicKey}-motion-clips.zip`);
if (existsSync(archive)) unlinkSync(archive);
const result = spawnSync("zip", ["-j", "-q", archive, ...files], {cwd: projectRoot, stdio: "inherit"});
if (result.status !== 0) {
  console.error("ZIP packaging failed. Ensure the system zip command is installed.");
  process.exit(result.status ?? 1);
}
console.log(`Package: ${archive}`);

const projectArchive = join(projectRoot, `${manifest.topicKey}-editable-project.zip`);
if (existsSync(projectArchive)) unlinkSync(projectArchive);
const projectFiles = ["asset-prompts", "visual-asset-plan.md", "package.json", "package-lock.json", "project-manifest.json", "themes.json", "template-gallery.json", "src", "scripts", "tsconfig.json", "eslint.config.mjs", "remotion.config.ts", "preview", "renders", "public"].filter((path) => existsSync(join(projectRoot, path)));
const projectZip = spawnSync("zip", ["-r", "-q", projectArchive, ...projectFiles], {cwd: projectRoot, stdio: "inherit"});
if (projectZip.status !== 0) process.exit(projectZip.status ?? 1);
console.log(`Editable project: ${projectArchive}`);
