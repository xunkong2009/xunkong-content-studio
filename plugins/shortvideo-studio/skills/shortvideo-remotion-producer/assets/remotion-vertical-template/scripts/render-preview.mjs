import {writePreviewPage} from "./preview-page.mjs";
import {previewName} from "./render-profile.mjs";
import {mixClipAudio} from "./audio-render.mjs";
import {mkdirSync, writeFileSync} from "node:fs";
import {join} from "node:path";
import {spawnSync} from "node:child_process";
import {assertManifest, ensureRemotionCli, loadManifest, projectRoot, removeFilesWithExtension, remotionCli} from "./project-lib.mjs";

const manifest = loadManifest();
assertManifest(manifest);
ensureRemotionCli();
const directory = join(projectRoot, "preview", "motion");
mkdirSync(directory, {recursive: true});
removeFilesWithExtension(directory, ".mp4");
const escape = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const cards = [];
for (const clip of manifest.clips) {
  // Use half size only when both resulting H.264 dimensions are even.
  const scale = manifest.video.width % 4 === 0 && manifest.video.height % 4 === 0 ? 0.5 : 1;
  const result = spawnSync(remotionCli, ["render", "src/index.ts", clip.compositionId, join(directory, previewName(clip)), "--codec=h264", "--muted", "--crf=28", "--pixel-format=yuv420p", `--scale=${scale}`, "--concurrency=2"], {cwd: projectRoot, stdio: "inherit"});
  if (result.status !== 0) process.exit(result.status ?? 1);
  mixClipAudio(manifest, clip, join(directory, previewName(clip)));
  const design = clip.motionDesign;
  const alphaNote = clip.presentation === "overlay" ? "透明浮层的MP4仅供动作预览，需另查最终alpha并与实际主播叠加审片。" : "全屏插片";
  const beats = (design?.beats ?? []).map((beat) => `<li>${(beat.startFrame / manifest.video.fps).toFixed(1)}s · ${escape(beat.triggerText)} → ${escape(beat.action)}</li>`).join("");
  cards.push(`<article><h2>${escape(clip.beatId)} · ${escape(clip.title)}</h2><video controls preload="metadata" playsinline src="${escape(previewName(clip))}"></video><p>${escape(design?.viewerQuestion ?? clip.narrativeJob)}</p><p>${escape(alphaNote)}</p><p>声音：${clip.audio?.mode === "sfx" ? "短动作音效，需实际试听" : "无声"}</p><p>口播锚点：${escape(design?.anchorText ?? clip.scriptExcerpt)}</p><p>${design?.timingSource === "narration" ? "按已有口播时间轴设计，仍需实际核对同步" : "估算节奏，未按真人录音同步"}</p><ol>${beats}</ol></article>`);
}
writeFileSync(join(directory, "index.html"), `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(manifest.projectTitle)} · 连续预览</title><style>body{margin:0;padding:28px;background:#f6f1e8;color:#122333;font-family:system-ui,"PingFang SC",sans-serif}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px}article{padding:24px;background:#fff;border-radius:16px}video{width:100%;max-height:70vh;background:#ddd}p,li{line-height:1.6}h2{font-size:22px}</style><h1>${escape(manifest.projectTitle)}</h1><p>先以正常速度播放，检查变化是否清楚、文字停留和首尾接口，再<a href="../audit/index.html">查看关键帧及全尺寸细节</a>。预览成功不代表视觉审查通过。</p><main>${cards.join("")}</main></html>`);
writePreviewPage(manifest, directory);
console.log(`Motion preview: ${join(directory, "index.html")}`);
