---
name: shortvideo-image-storyboard
description: 口播短视频连续图文配图分镜工具：适用于把给定口播文案拆成竖版演示页式配图段落，生成 Markdown 分镜表、页面文字、图片提示词，并按需调用 imagegen 生成图文并茂的图片。支持白板图文讲义风和普通解析风；普通解析风默认做成浅色底、图文并茂、研究问题式的竖版 PPT 页面，并按用户指定比例适配；有参考图时按参考图风格执行，没有参考图且需要出图时默认先生成第一张确认，再继续批量生成。
---

## 分享版个人配置

用户当轮提供的材料和要求优先。需要语料库、主播照片或本地字体时，可读取当前项目的 `.xunkong-studio/config.json`（如存在）；相对文件路径以当前项目为基准。配置示例见插件根目录 `config.example.json`，不要改写安装目录。

未配置语料库时使用随包风格规则继续写作；未配置真人参考照片时可先交付提示词或无人像方案。需要复现某个真人且缺少参考时，向当前用户索取参考，不使用发布者的身份。配置文件中不存储 API Key、密码或账号 Cookie。

# 口播短视频配图分镜

## Overview

Use this skill to turn a spoken short-video script into a continuous visual slide storyboard. The goal is not decorative background images, but presentation-like short-video images that combine readable text, visual explanation, and narration support.

Load references only when needed:

- `references/storyboard-rules.md` for segmentation, visual-intent selection, reference-image priority, confirmation gates, and output format.
- `references/style-guides.md` before writing prompts or generating images.

## Plugin handoff

When called by `shortvideo-workbench` with a `VisualBeatPlan`, process only beats marked `generated-slide` and the generated-slide portion of `mixed` beats. Preserve every `beat_id` in the storyboard and generated filename. Do not re-segment the full script; use the supplied excerpt, visual job, on-image text, aspect ratio, and style, while retaining this skill's reference-image and first-image confirmation rules.

## Default Workflow

1. Read the user's script and identify topic, audience, emotional tone, content type, and whether current-fact verification is needed.
2. Determine the aspect ratio:
   - Default is `9:16`.
   - If the user specifies another ratio such as `1:1`, `4:5`, `16:9`, `3:4`, or any other clear ratio, use that ratio for storyboard composition, prompts, and generated images.
   - Keep one ratio for the whole batch unless the user explicitly asks for mixed ratios.
3. Determine visual style:
   - If the user provides reference images, use them as the highest-priority style/composition/person/color/layout guidance.
   - If the user provides horizontal PPT/reference images but requests or implies vertical short-video output, inherit the content density, visual reasoning, layout devices, and presentation feeling from the references, then redesign them for the requested vertical ratio.
   - If the user specifies `手绘`, `白板`, `讲义`, or asks for a hand-drawn page, use `白板图文讲义风`.
   - If the user specifies `普通`, `解析`, `写实`, or does not specify a style, use `普通解析风`: a light-background vertical PPT explainer page with rich but readable text, diagrams, photos/illustrations, comparison blocks, callouts, and a research/problem-solving feeling.
   - If a recurring presenter is needed, use the current user's provided reference and preserve that identity. Do not assume a default gender, face or clothing.
4. Segment the script semantically. For `白板图文讲义风`, aim for about 100 Chinese characters per page. For `普通解析风`, aim for one complete problem, mechanism, contrast, example, or conclusion per page, usually 80-140 Chinese characters depending on page density and the requested aspect ratio. Do not split mechanically if it breaks a complete idea.
5. For each segment, assign a visual intent: opening, concept explanation, emotional emphasis, contrast, conflict, analogy, transition, or conclusion.
6. For each image, write an on-image text plan:
   - One complete title or core argument.
   - For `白板图文讲义风`, one explanation text block that summarizes the key evidence or mechanism, plus one conclusion sticky note.
   - For `普通解析风`, a PPT-style text system: one large title, 2-4 short analysis blocks/callouts/labels, and one bottom or side takeaway sentence when needed.
   - Keep text readable on mobile; avoid full voiceover paragraphs.
7. Output a Markdown storyboard first. Include settings, segment table, on-image text, prompt for each image, and negative prompt.
8. If the user asks only for prompts, stop at the storyboard/prompt pack.
9. If the user asks to generate images, use the imagegen skill / built-in image tool:
   - With reference images: generate in sequence using the reference guidance, unless references conflict.
   - Without reference images and without prior style/batch approval: generate only image 1 first, show it to the user, and ask whether the style is acceptable before continuing. Existing style approval or explicit direct batch authorization continues without another gate.
   - After confirmation, continue generating the remaining images in order.

## Operating Rules

- Default language is Simplified Chinese unless the user asks otherwise.
- Default deliverable is Markdown plus image preview/status. Do not output JSON by default.
- Every visual must serve the narration. Avoid attractive but irrelevant images.
- Keep the whole batch visually consistent: aspect ratio, style, color language, character treatment, image density, and text policy.
- Use the current user's reference for recurring presenter identity. Without a reference, use a no-presenter explanation or a clearly generic character when appropriate; do not claim identity fidelity.
- Default hand-drawn images use `白板图文讲义风`: pure white background, complete title/core argument, diagram subject, explanation text block, and conclusion sticky note.
- Default ordinary images use `普通解析风`: light or warm off-white background, vertical PPT-like information design, rich visual explanation, and an analytical "studying a problem" feeling. Use charts, tables, comparison columns, photo/illustration cards, arrows, callout boxes, icons, and short evidence notes as needed. The page should feel like a designed slide, not a standalone stock image with a title pasted on top.
- On-image Chinese text must be exact and listed separately before the prompt. Prefer concise argument sentences, evidence summaries, and key numbers over subtitle-style transcription.
- Do not put the full voiceover inside generated images. A whiteboard lecture page may include short explanatory paragraphs, but not dense article text.
- If exact Chinese typography is critical or the image model produces bad text, regenerate once with simpler text; if still unstable, make a clean visual with reserved text boxes for post-production overlay.
- Abstract ideas must become visible situations. For example, do not prompt "流量焦虑"; depict a creator watching a falling dashboard or a crowded feed swallowing a small account.
- For long scripts, vary composition every 4-6 images so the sequence does not become a string of similar scenes. In `普通解析风`, rotate among comparison page, mechanism diagram, case table, process flow, image-card grid, data/number page, metaphor page, and conclusion page.
- If user-provided references conflict, ask for priority instead of blending them silently.
- If the topic depends on current news, company status, policy, pricing, legal, medical, or financial facts, verify before turning those facts into visuals.

## Output Contract

Use this structure unless the user requests another format:

```markdown
## 口播配图方案

基础设置：
- 风格：白板图文讲义风 / 普通解析风 / 参考图风格
- 画幅：9:16 或用户指定比例
- 切片密度：白板图文讲义风每 100 字左右一页；普通解析风按一个完整问题/机制/对比/案例/结论一页，通常 80-140 字
- 参考图使用方式：无 / 人物 / 构图 / 色彩 / 质感 / 版式
- 生成策略：只给 prompts / 先生成第 1 张确认 / 按参考图连续生成

### 图 01
对应文案：
...

画面任务：
...

页面文字：
- 标题/核心论点：...
- 解释文字块 / 分析卡片 / 标签：...
- 结论贴纸 / 底部金句：...

构图与主体：
...

Prompt：
...

Negative prompt：
...

生成状态：
未生成 / 已生成预览 / 等待确认
```

## Completion Checklist

- Script segments are semantic. Whiteboard lecture pages are roughly 100 Chinese characters each; ordinary analysis pages each carry one complete analytical beat and are usually 80-140 Chinese characters depending on density and ratio.
- Style choice is clear and consistent.
- Aspect ratio follows the user's explicit instruction or defaults to `9:16`.
- Reference-image roles are named when references are provided.
- Each whiteboard lecture page has a complete title/core argument, diagram subject, explanation text block, and conclusion sticky note.
- Each ordinary analysis page is a light-background vertical PPT explainer page with visible information architecture, not merely a realistic scene.
- Each prompt is executable by an image model and contains a concrete scene.
- Without references or prior style/batch authorization, stop after the first preview for style confirmation. Existing approval or explicit direct-production instructions continue without another gate.
- Prompt-only requests do not call image generation tools.

## 已确认口播项目中的配图

沿用工作台已有beat_id、实际口播范围与确认风格，使用image生成连续图文分镜，不重新拆整篇脚本。整批保持图形、材质与文字层级一致，配图与真实视频、说明动画各司其职。考虑后期普通字幕的实际位置，为必要字幕留空；不要在同一区域同时放完整页面结论与口播字幕。既有配图保留，新版另存。Remotion只需要主体图片时走其hybrid-assets流程，不启动整套配图流程。
