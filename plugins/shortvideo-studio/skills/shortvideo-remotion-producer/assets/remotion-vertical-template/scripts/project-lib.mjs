import {validateVisualAssets} from "./visual-assets.mjs";
import {existsSync, readFileSync, readdirSync, statSync, unlinkSync} from "node:fs";
import {dirname, join, resolve} from "node:path";
import {fileURLToPath} from "node:url";

export const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
export const manifestPath = join(projectRoot, "project-manifest.json");
export const remotionCli = join(projectRoot, "node_modules", ".bin", "remotion");

export const loadManifest = () => JSON.parse(readFileSync(manifestPath, "utf8"));

const isHex = (value) => typeof value === "string" && (/^#[0-9a-f]{6}$/i.test(value) || value.startsWith("rgb"));
const requiredClipStrings = ["beatId", "compositionId", "fileName", "title", "scriptExcerpt", "narrativeJob", "motionType"];

export const validateManifest = (manifest) => {
  const errors = [];
  const version = manifest.schemaVersion ?? 1;
  if (![1, 2].includes(version)) errors.push("schemaVersion must be 1 or 2");
  if (!manifest.projectTitle?.trim()) errors.push("projectTitle is required");
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(manifest.topicKey ?? "")) errors.push("topicKey must be lower-case hyphen-case");
  if (!["draft", "confirmed", "user-provided"].includes(manifest.scriptStatus)) errors.push("scriptStatus must be draft, confirmed, or user-provided");
  if (!manifest.sourceScript?.trim()) errors.push("sourceScript is required");
  if (!Array.isArray(manifest.scopeTerms) || manifest.scopeTerms.length === 0 || manifest.scopeTerms.some((term) => !term?.trim())) errors.push("scopeTerms must contain at least one topic or brand term");
  if (!Array.isArray(manifest.forbiddenCarryoverTerms) || manifest.forbiddenCarryoverTerms.some((term) => !term?.trim())) errors.push("forbiddenCarryoverTerms must be an array of non-empty strings");
  if (!Array.isArray(manifest.referenceImages)) errors.push("referenceImages must be an array");

  const tokens = ["background", "paper", "ink", "accent", "accentSecondary", "line", "shadow"];
  for (const token of tokens) {
    if (!isHex(manifest.styleTokens?.[token])) errors.push(`styleTokens.${token} must be a CSS color`);
  }

  for (const field of ["width", "height", "fps"]) {
    if (!Number.isInteger(manifest.video?.[field]) || manifest.video[field] <= 0) errors.push(`video.${field} must be a positive integer`);
  }

  if (!Array.isArray(manifest.clips) || manifest.clips.length === 0) {
    errors.push("clips must contain at least one clip");
  } else {
    const seenBeatIds = new Set();
    const seenCompositionIds = new Set();
    const seenFileNames = new Set();

    for (const [index, clip] of manifest.clips.entries()) {
      const label = `clips[${index}]`;
      for (const field of requiredClipStrings) {
        if (!clip[field]?.trim()) errors.push(`${label}.${field} is required`);
      }
      if (!/^B\d{2,}$/.test(clip.beatId ?? "")) errors.push(`${label}.beatId must look like B01`);
      if (!/^[A-Z][A-Za-z0-9]*$/.test(clip.compositionId ?? "")) errors.push(`${label}.compositionId must be PascalCase`);
      if (!/^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.(mp4|mov|webm)$/.test(clip.fileName ?? "")) errors.push(`${label}.fileName must look like 01-topic-name.mp4/mov/webm`);
      const profile = clip.renderProfile ?? "h264";
      const ext = {"h264":".mp4", "prores-alpha":".mov", "vp9-alpha":".webm"}[profile];
      if (!ext || !clip.fileName?.endsWith(ext)) errors.push(`${label}: renderProfile and extension must agree`);
      if (clip.presentation !== undefined && !["fullscreen", "overlay"].includes(clip.presentation)) errors.push(`${label}.presentation invalid`);
      if (clip.templateId !== undefined && !["keyword","callout","opinion-cards","data-chart","logic-flow","comparison","timeline","evidence","brand-map","custom"].includes(clip.templateId)) errors.push(`${label}.templateId invalid`);
      const props = clip.templateProps ?? {};
      if (props.items !== undefined && (!Array.isArray(props.items) || props.items.some(item => !item || typeof item.label !== "string" || !item.label.trim()))) errors.push(`${label}.templateProps.items requires labels`);
      if (["callout","opinion-cards"].includes(clip.templateId) && props.items?.length > 3) errors.push(`${label}: reference card layout supports up to 3 items; split or use custom`);
      if (["timeline","logic-flow"].includes(clip.templateId) && props.items?.length > 4) errors.push(`${label}: reference timeline/flow supports up to 4 items; split or use custom`);
      if (props.items?.length > 6) errors.push(`${label}: too many items for base template; split or use custom`);
      if (clip.templateId === "comparison" && props.items?.length !== 2) errors.push(`${label}: comparison needs two items`);
      if (clip.templateId === "brand-map" && (!props.items?.length || props.items.length > 4)) errors.push(`${label}: brand-map supports 1-4 items; split complex maps`);
      if (clip.templateId === "data-chart" && (!props.items?.length || props.items.some(item => !Number.isFinite(item.value) || item.value < 0) || !Number.isFinite(props.value))) errors.push(`${label}: data-chart requires nonnegative item values and a finite headline value`);
      if (props.revealSeconds !== undefined && (!Array.isArray(props.revealSeconds) || props.revealSeconds.some((sec,i) => !Number.isFinite(sec) || sec < 0 || sec*manifest.video.fps >= clip.durationInFrames || (i>0 && sec<props.revealSeconds[i-1])))) errors.push(`${label}: invalid revealSeconds`);
      if (props.presentation !== undefined && props.presentation !== (clip.presentation ?? "fullscreen")) errors.push(`${label}: templateProps.presentation conflicts with clip.presentation`);
      if (clip.presentation === "overlay") {
        if (profile === "h264") errors.push(`${label}: overlay output must use an alpha profile`);
        const validRect = r => r && [r.x,r.y,r.width,r.height].every(Number.isFinite) && r.x>=0 && r.y>=0 && r.width>0 && r.height>0 && r.x+r.width<=manifest.video.width && r.y+r.height<=manifest.video.height;
        if (!validRect(props.overlayRegion) || !Array.isArray(props.faceRegions) || !props.faceRegions.length || props.faceRegions.some(r=>!validRect(r))) errors.push(`${label}: overlay requires canvas-valid overlayRegion and faceRegions measured from footage`);
        else if (props.faceRegions.some(r => props.overlayRegion.x < r.x+r.width && props.overlayRegion.x+props.overlayRegion.width > r.x && props.overlayRegion.y < r.y+r.height && props.overlayRegion.y+props.overlayRegion.height > r.y)) errors.push(`${label}: overlay overlaps face protection region`);
      }
      if (clip.timeline !== undefined) {
        const time = clip.timeline;
        if (!time.baseVideo || !/^[a-f0-9]{64}$/i.test(time.baseSha256??"") || !Number.isFinite(time.start) || !Number.isFinite(time.end) || time.start<0 || time.end<=time.start || Math.abs((time.end-time.start)*manifest.video.fps-clip.durationInFrames) > 1) errors.push(`${label}: timeline requires locked base path/hash and matching actual duration`);
      }
      if (!Number.isInteger(clip.durationInFrames) || clip.durationInFrames <= 0) errors.push(`${label}.durationInFrames must be positive`);
      if (!Array.isArray(clip.auditFrames) || clip.auditFrames.length < 4) errors.push(`${label}.auditFrames must contain at least four stable frames`);
      if (!Array.isArray(clip.transitionFrames) || clip.transitionFrames.length < 1) errors.push(`${label}.transitionFrames must contain at least one transition frame`);

      for (const [kind, frames] of [["auditFrames", clip.auditFrames], ["transitionFrames", clip.transitionFrames]]) {
        if (!Array.isArray(frames)) continue;
        for (const frame of frames) {
          if (!Number.isInteger(frame) || frame < 0 || frame >= clip.durationInFrames) errors.push(`${label}.${kind} contains invalid frame ${frame}`);
        }
      }

      if (clip.audio !== undefined) {
        const audio = clip.audio;
        if (!audio || !["silent", "sfx"].includes(audio.mode) || !Array.isArray(audio.events)) errors.push(`${label}.audio requires mode silent/sfx and events array`);
        else {
          if (audio.mode === "silent" && audio.events.length > 0) errors.push(`${label}.audio silent mode cannot contain events`);
          if (audio.mode === "sfx" && audio.events.length === 0) errors.push(`${label}.audio sfx mode requires events`);
          for (const [i, event] of audio.events.entries()) {
            const tag = `${label}.audio.events[${i}]`;
            if (!event || typeof event !== "object") {errors.push(`${tag} must be an object`); continue;}
            for (const field of ["src", "purpose", "source"]) if (typeof event[field] !== "string" || !event[field].trim()) errors.push(`${tag}.${field} is required`);
            if (typeof event.src === "string" && (/^(?:[a-z]+:|\/)|(?:^|\/)\.\.(?:\/|$)|\\/i.test(event.src))) errors.push(`${tag}.src must be a local public-relative asset path`);
            if (!Number.isInteger(event.from) || event.from < 0 || !Number.isInteger(event.durationInFrames) || event.durationInFrames <= 0 || event.from + event.durationInFrames > clip.durationInFrames) errors.push(`${tag} has invalid audio frame range`);
            if (!Number.isFinite(event.volume) || event.volume <= 0 || event.volume > 1) errors.push(`${tag}.volume must be greater than 0 and at most 1`);
          }
        }
      }

      if (clip.detailFrames !== undefined && (!Array.isArray(clip.detailFrames) || clip.detailFrames.some((f) => !Number.isInteger(f) || f < 0 || f >= clip.durationInFrames))) errors.push(`${label}.detailFrames contains invalid frames`);
      if (version === 2) {
        const design = clip.motionDesign;
        const hasText = (v) => typeof v === "string" && v.trim().length > 0;
        if (!design || typeof design !== "object" || Array.isArray(design)) errors.push(`${label}.motionDesign is required for schemaVersion 2`);
        else {
          for (const field of ["viewerQuestion", "visualModel", "layoutMode", "anchorText"]) {
            if (!hasText(design[field])) errors.push(`${label}.motionDesign.${field} is required`);
          }
          if (!["full-excerpt", "illustrative-insert"].includes(design.coverageMode)) errors.push(`${label}.motionDesign.coverageMode is invalid`);
          if (!["estimated", "narration"].includes(design.timingSource)) errors.push(`${label}.motionDesign.timingSource is invalid`);
          if (design.timingSource === "narration" && !hasText(design.timingEvidence)) errors.push(`${label}.motionDesign.timingEvidence is required for narration timing`);
          if (hasText(design.anchorText) && !clip.scriptExcerpt?.includes(design.anchorText)) errors.push(`${label}.motionDesign.anchorText must occur in scriptExcerpt`);
          if (design.coverageMode === "full-excerpt" && design.anchorText !== clip.scriptExcerpt) errors.push(`${label}.motionDesign.anchorText must equal scriptExcerpt for full-excerpt`);
          if (!Array.isArray(design.beats) || design.beats.length === 0) errors.push(`${label}.motionDesign.beats must contain at least one action`);
          else {
            let previousHoldEnd = -1;
            for (const [i, beat] of design.beats.entries()) {
              const tag = `${label}.motionDesign.beats[${i}]`;
              if (!beat || typeof beat !== "object" || Array.isArray(beat)) { errors.push(`${tag} must be an action object`); continue; }
              for (const field of ["triggerText", "action", "focus"]) if (!hasText(beat[field])) errors.push(`${tag}.${field} is required`);
              if (hasText(beat.triggerText) && !design.anchorText?.includes(beat.triggerText)) errors.push(`${tag}.triggerText must occur in anchorText`);
              const frames = [beat.startFrame, beat.endFrame, beat.holdEndFrame];
              if (frames.some((f) => !Number.isInteger(f) || f < 0 || f >= clip.durationInFrames) || !(beat.startFrame <= beat.endFrame && beat.endFrame <= beat.holdEndFrame)) errors.push(`${tag} has invalid action/hold frame range`);
              if (beat.startFrame <= previousHoldEnd) errors.push(`${tag} overlaps the previous primary action/reading hold`);
              previousHoldEnd = beat.holdEndFrame;
            }
          }
        }
      }

      if (seenBeatIds.has(clip.beatId)) errors.push(`Duplicate beatId: ${clip.beatId}`);
      if (seenCompositionIds.has(clip.compositionId)) errors.push(`Duplicate compositionId: ${clip.compositionId}`);
      if (seenFileNames.has(clip.fileName)) errors.push(`Duplicate fileName: ${clip.fileName}`);
      seenBeatIds.add(clip.beatId);
      seenCompositionIds.add(clip.compositionId);
      seenFileNames.add(clip.fileName);
    }
  }

  errors.push(...validateVisualAssets(manifest));
  return errors;
};

export const assertManifest = (manifest) => {
  const errors = validateManifest(manifest);
  if (errors.length > 0) {
    console.error("Manifest validation failed:");
    for (const error of errors) console.error(`- ${error}`);
    process.exit(1);
  }
};

export const ensureRemotionCli = () => {
  if (!existsSync(remotionCli)) {
    console.error("Remotion CLI not found. Run npm install first.");
    process.exit(1);
  }
};

export const removeFilesWithExtension = (directory, extension) => {
  if (!existsSync(directory)) return;
  for (const file of readdirSync(directory)) {
    const path = join(directory, file);
    if (file.endsWith(extension) && statSync(path).isFile()) unlinkSync(path);
  }
};
