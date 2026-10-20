#!/usr/bin/env node
import {cpSync, existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync} from "node:fs";
import {dirname, join, resolve} from "node:path";
import {fileURLToPath} from "node:url";

const args = process.argv.slice(2);
const valueFor = (name) => {
  const index = args.indexOf(name);
  return index === -1 ? undefined : args[index + 1];
};

const output = valueFor("--output");
const topicKey = valueFor("--topic-key");
const projectTitle = valueFor("--title");
const orientationFlag = args.indexOf("--orientation");
const orientation = orientationFlag === -1 ? "portrait" : valueFor("--orientation");

if (!output || !topicKey || !projectTitle) {
  console.error("Usage: node create-project.mjs --output <dir> --topic-key <slug> --title <title> [--orientation portrait|landscape] [--theme cream-red|navy-gold] [--gallery]");
  process.exit(1);
}

if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(topicKey)) {
  console.error("--topic-key must use lower-case hyphen-case.");
  process.exit(1);
}

if (!["landscape", "portrait"].includes(orientation)) {
  console.error("--orientation must be landscape or portrait.");
  process.exit(1);
}

const theme = valueFor("--theme") ?? "navy-gold";
if (!["cream-red", "navy-gold"].includes(theme)) throw new Error("--theme must be cream-red or navy-gold");
const target = resolve(output);
if (existsSync(target) && readdirSync(target).length > 0) {
  console.error(`Refusing to overwrite non-empty directory: ${target}`);
  process.exit(1);
}

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const template = join(skillRoot, "assets", "remotion-vertical-template");
mkdirSync(target, {recursive: true});
cpSync(template, target, {recursive: true});

const packagePath = join(target, "package.json");
const packageJson = JSON.parse(readFileSync(packagePath, "utf8"));
packageJson.name = `${topicKey}-motion-clips`;
writeFileSync(packagePath, `${JSON.stringify(packageJson, null, 2)}\n`);

const packageLockPath = join(target, "package-lock.json");
if (existsSync(packageLockPath)) {
  const packageLock = JSON.parse(readFileSync(packageLockPath, "utf8"));
  packageLock.name = packageJson.name;
  if (packageLock.packages?.[""]) packageLock.packages[""].name = packageJson.name;
  writeFileSync(packageLockPath, `${JSON.stringify(packageLock, null, 2)}\n`);
}

const manifestPath = join(target, "project-manifest.json");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
manifest.projectTitle = projectTitle;
manifest.topicKey = topicKey;
manifest.video.width = orientation === "portrait" ? 1080 : 1920;
manifest.video.height = orientation === "portrait" ? 1920 : 1080;
manifest.theme = theme;
manifest.styleTokens = JSON.parse(readFileSync(join(target, "themes.json"), "utf8"))[theme];
manifest.scopeTerms = [projectTitle];
if (args.includes("--gallery")) {
  const gallery = JSON.parse(readFileSync(join(target, "template-gallery.json"), "utf8"));
  manifest.sourceScript = gallery.sourceScript;
  manifest.clips = gallery.clips;
}
writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

console.log(`Created Remotion project: ${target}`);
console.log(`Video: ${orientation} ${manifest.video.width}x${manifest.video.height} @ ${manifest.video.fps}fps`);
console.log("Next: update project-manifest.json, add clips to src/clip-registry.tsx, then run npm install.");
