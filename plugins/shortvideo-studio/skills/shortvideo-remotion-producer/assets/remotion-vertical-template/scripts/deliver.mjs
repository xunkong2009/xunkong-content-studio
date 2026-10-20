import {spawnSync} from "node:child_process";
import {projectRoot} from "./project-lib.mjs";

const visualApproved = process.argv.includes("--visual-approved");
const run = (name) => {
  const result = spawnSync("npm", ["run", name], {cwd: projectRoot, stdio: "inherit"});
  if (result.status !== 0) process.exit(result.status ?? 1);
};

run("preflight");
run("lint");
run("preview:motion");
run("preview:audit");

if (!visualApproved) {
  console.log("Motion previews and audit frames are ready. Watch preview/motion/index.html at normal speed, inspect preview/audit/index.html, fix all visual issues, then run npm run deliver -- --visual-approved.");
  process.exit(0);
}

run("render:all");
run("verify");
run("package");
