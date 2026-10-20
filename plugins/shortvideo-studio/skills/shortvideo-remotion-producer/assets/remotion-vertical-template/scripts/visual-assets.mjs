import {existsSync, statSync} from "node:fs";
import {join} from "node:path";

const hasText = (value) => typeof value === "string" && value.trim().length > 0;
const localPath = (value) => hasText(value) && !/^(?:[a-z]+:|\/)|(?:^|\/)\.{1,2}(?:\/|$)|\\/i.test(value);

// Optional metadata keeps existing code-only and pre-upgrade projects compatible.
// With projectRoot, additionally verify the declared files; visual quality is reviewed separately.
export const validateVisualAssets = (manifest, {projectRoot} = {}) => {
  const errors = [];
  const assets = manifest.visualAssets ?? [];
  if (!Array.isArray(assets)) return ["visualAssets must be an array"];
  const ids = new Set();
  const checkFile = (relative, label, publicRelative = false) => {
    if (!localPath(relative)) {errors.push(`${label} must be a local ${publicRelative ? "public" : "project"}-relative path`); return;}
    if (!projectRoot) return;
    const path = publicRelative ? join(projectRoot, "public", relative) : join(projectRoot, relative);
    if (!existsSync(path) || !statSync(path).isFile()) errors.push(`${label}: missing file ${relative}`);
  };
  for (const [i, asset] of assets.entries()) {
    const label = `visualAssets[${i}]`;
    if (!asset || typeof asset !== "object" || Array.isArray(asset)) {errors.push(`${label} must be an asset object`); continue;}
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(asset.id ?? "")) errors.push(`${label}.id must be lower-case hyphen-case`);
    if (ids.has(asset.id)) errors.push(`${label}: duplicate visual asset id ${asset.id}`);
    if (hasText(asset.id)) ids.add(asset.id);
    if (!["character", "product", "prop", "background", "other"].includes(asset.type)) errors.push(`${label}.type is invalid`);
    if (!["user", "existing", "official", "generated"].includes(asset.sourceType)) errors.push(`${label}.sourceType is invalid`);
    if (!hasText(asset.source)) errors.push(`${label}.source is required`);
    checkFile(asset.src, `${label}.src`, true);
    if (asset.sourceType === "generated" && !hasText(asset.promptPath)) errors.push(`${label}.promptPath is required for generated assets`);
    if (asset.promptPath !== undefined) checkFile(asset.promptPath, `${label}.promptPath`);
    if (asset.referencePaths !== undefined) {
      if (!Array.isArray(asset.referencePaths)) errors.push(`${label}.referencePaths must be an array`);
      else for (const [j, path] of asset.referencePaths.entries()) checkFile(path, `${label}.referencePaths[${j}]`);
    }
    for (const field of ["identityGroup", "variant"]) {
      if (asset[field] !== undefined && !hasText(asset[field])) errors.push(`${label}.${field} must be non-empty text`);
    }
  }
  for (const [i, clip] of (Array.isArray(manifest.clips) ? manifest.clips : []).entries()) {
    if (clip.assetIds === undefined) continue;
    if (!Array.isArray(clip.assetIds)) {errors.push(`clips[${i}].assetIds must be an array`); continue;}
    const used = new Set();
    for (const id of clip.assetIds) {
      if (!ids.has(id)) errors.push(`clips[${i}].assetIds references unknown visual asset ${String(id)}`);
      if (used.has(id)) errors.push(`clips[${i}].assetIds repeats ${String(id)}`);
      used.add(id);
    }
  }
  return errors;
};
