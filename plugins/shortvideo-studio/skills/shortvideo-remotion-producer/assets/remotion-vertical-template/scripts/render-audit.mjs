import {mkdirSync, writeFileSync} from "node:fs";
import {join} from "node:path";
import {spawnSync} from "node:child_process";
import {assertManifest, ensureRemotionCli, loadManifest, projectRoot, removeFilesWithExtension, remotionCli} from "./project-lib.mjs";

const manifest = loadManifest();
assertManifest(manifest);
ensureRemotionCli();

const auditDir = join(projectRoot, "preview", "audit");
mkdirSync(auditDir, {recursive: true});
removeFilesWithExtension(auditDir, ".png");

const items = [];
for (const clip of manifest.clips) {
  const frames = [
    ...clip.auditFrames.map((frame) => ({frame, kind: "stable"})),
    ...clip.transitionFrames.map((frame) => ({frame, kind: "transition"})),
    ...(clip.detailFrames ?? [clip.auditFrames.at(-1)]).map((frame) => ({frame, kind: "detail"})),
  ];
  const unique = [...new Map(frames.map((item) => [`${item.frame}-${item.kind}`, item])).values()];

  for (const item of unique) {
    const fileName = `${clip.beatId}-${clip.compositionId}-${item.kind}-f${item.frame}.png`;
    const output = join(auditDir, fileName);
    const result = spawnSync(
      remotionCli,
      ["still", "src/index.ts", clip.compositionId, output, `--frame=${item.frame}`, `--scale=${item.kind === "detail" ? 1 : 0.25}`],
      {cwd: projectRoot, stdio: "inherit"},
    );
    if (result.status !== 0) process.exit(result.status ?? 1);
    items.push({...item, beatId: clip.beatId, compositionId: clip.compositionId, title: clip.title, fileName});
  }
}

const escapeHtml = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
const cards = items.map((item) => `
  <article>
    <a href="${escapeHtml(item.fileName)}"><img src="${escapeHtml(item.fileName)}" alt="${escapeHtml(item.beatId)} ${escapeHtml(item.title)} frame ${item.frame}"></a>
    <div><strong>${escapeHtml(item.beatId)} · ${escapeHtml(item.title)}</strong><br>${item.kind} · frame ${item.frame}</div>
  </article>`).join("");

const html = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(manifest.projectTitle)} 审片</title>
<style>body{margin:0;padding:28px;background:#1b1b1b;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}h1{font-size:28px}.note{color:#bbb;margin-bottom:24px}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}article{background:#2a2a2a;border-radius:12px;overflow:hidden}img{display:block;width:100%;height:auto}article div{padding:12px 14px;line-height:1.5;font-size:14px}@media(max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}</style></head>
<body><h1>${escapeHtml(manifest.projectTitle)} · Remotion 关键帧审片</h1><div class="note"><a href="../motion/index.html">先看正常速度连续预览</a>。关键帧共 ${items.length} 张；detail 为全尺寸，点击查看。检查断行、孤字、遮挡、越界、裁切和重影。</div><div class="grid">${cards}</div></body></html>`;
writeFileSync(join(auditDir, "index.html"), html);
console.log(`Audit page: ${join(auditDir, "index.html")}`);
