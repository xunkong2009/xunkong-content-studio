# Style Guides

## Shared Prompt Rules

Every prompt should include:

- Aspect ratio.
- Intended short-video use.
- Exact on-image text and text layout.
- Concrete scene and subject.
- Composition and camera/framing.
- Mood and color/lighting direction.
- Style source: default style or reference-image style.
- Text policy: presentation-like layout with short readable Chinese text by default.

Avoid:

- Generic "high quality, masterpiece" filler.
- Unsupported factual claims in the image.
- Long Chinese text, full voiceover sentences, or subtitle paragraphs inside the image.
- Overcrowded scenes with too many symbols.
- Sudden style changes across a batch.
- Tiny unreadable text, fake interface text, or extra random Chinese characters.

## Text Layout Defaults

Default images should look like short-video presentation pages: a strong visual plus readable explanatory text.

- For `白板图文讲义风`, use a complete title/core argument, a central diagram, one explanation text block, and one conclusion sticky note.
- For `普通解析风`, use a vertical PPT-style information page: one main title, one clear visual thesis, 2-4 short analysis blocks or labels, and an optional bottom takeaway. The page should feel like it is studying a problem, not simply decorating a sentence.
- For data pages, one large number can be the visual center, but the page still needs an explanation block and takeaway when using `白板图文讲义风`.
- Keep text high contrast, large, and readable on a phone.
- Leave breathing room around text. Do not place text over busy details.
- Ask the image model to render only the listed text; no extra words.

Prompt text block:

```text
页面文字：标题/核心论点「<title_or_argument>」；解释文字块「<explanation>」；结论贴纸「<takeaway>」。只渲染这些文字，不要添加其他中文、英文或假文字。
文字布局：顶部大标题，中部图解主体，侧边或中下部解释文字块，底部或角落黄色结论贴纸；字体粗、清晰、高对比，适合手机竖屏阅读。
```

## Presenter Reference

Use the current user's uploaded or project-configured presenter reference when recurring identity matters. Preserve the reference identity and user-specified styling; do not default to a particular gender, face, age or clothing. Label identity, layout, color and texture references separately. Without an identity reference, use a no-presenter explanation or a clearly generic character; do not claim the image depicts the user.

## 白板图文讲义风

Use for spoken short-video hand-drawn lecture pages, business case analysis, knowledge explainers, and mechanism breakdowns.

Visual language:

- Pure white background.
- Hand-drawn whiteboard lecture page, editorial explainer, light infographic, or hand-drawn presentation slide.
- Clear black or dark-gray linework with restrained accent colors.
- No grid-paper background by default.
- Simple characters, objects, arrows, panels, sticky notes, charts, and metaphorical props.
- Composition should be readable on a phone screen.
- Text should feel like bold marker-style Chinese presentation lettering: large title, readable explanation, clear takeaway sticky note.
- Each page should be understandable on its own without hearing the full voiceover.

Prompt pattern:

```text
画幅：<ratio>。为口播短视频生成一张图文并茂的白板图文讲义风演示页，纯白底。页面文字：标题/核心论点「<title_or_argument>」；解释文字块「<explanation>」；结论贴纸「<takeaway>」。只渲染这些文字，不要添加其他中文、英文或假文字。画面表现：<segment meaning>。图解主体：<main diagram subject>。构图：顶部大标题，中部图解主体，侧边或中下部解释文字块，底部或角落黄色结论贴纸；文字与图像分区清楚。视觉语言：手绘线稿、白板讲义、轻信息图、克制配色、红色下划线/箭头/圈注、少量黄色贴纸、清晰手机端阅读。情绪：<tone>。
```

Good uses:

- Explaining a mechanism with arrows or simple flow.
- Turning anxiety, trust, growth, decline, and competition into visual metaphors.
- Summarizing a business argument so one page reveals the core point, evidence, and takeaway.
- Showing a person facing dashboards, choices, screens, or symbolic objects only when a person is necessary.

## 普通解析风

Use by default when no style is specified. It should feel like a clear visual analysis slide, not random stock photography.

Visual language:

- Light or warm off-white background by default; avoid heavy dark backgrounds unless the user asks.
- Vertical PPT-like explainer page, commercial analysis slide, editorial infographic, or clean conceptual presentation page.
- Rich but readable information design: title, diagram/photo/illustration, callout cards, arrows, labels, comparison blocks, tables, timelines, funnels, matrices, or bottom conclusion strips.
- Concrete people, products, screens, stores, desks, city scenes, factory scenes, social-media interfaces, photos, icons, or illustrations when relevant, but always organized as a slide.
- Strong but not chaotic composition. The viewer should understand the logic in 3 seconds and see the supporting details after that.
- Restrained business colors on a light base: dark gray/black type, muted blue/green/terra-cotta accents, occasional red circles/arrows/underlines for emphasis.
- Use bold readable Chinese title typography, medium-weight body text, data callouts, label cards, and clear hierarchy. Avoid fake interface text unless the user provides exact text.
- Adapt the layout to the requested ratio. For vertical ratios, use stacked modules, big central visual, or two-column comparison only when the text remains readable.

Think before composing:

- What problem is this page answering?
- Which structure best explains it: comparison, mechanism, table, flow, funnel, scale, cycle, matrix, image-card grid, quote, or metaphor?
- Which parts must be text, and which parts should be visual?
- What is the one conclusion the audience should remember?

Common vertical page patterns:

- `问题开场页`: top large question, central symbolic image or photo, 2-3 small evidence tags, bottom sharp takeaway.
- `左右/上下对比页`: old vs new, before vs after, expectation vs reality, desire vs comfort, cost vs benefit.
- `机制流程页`: 3-5 step flow with arrows, each step has a short label and one sentence.
- `案例表格页`: compact table or grid, red/green circles, sticky-note conclusion.
- `图文卡片页`: 3-4 photo/illustration cards with icon, title, and one-line explanation.
- `数据/杠杆页`: one chart/funnel/scale/large number plus explanatory callouts.
- `隐喻解释页`: balance scale, funnel, engine, shield, harbor, maze, conveyor belt, magnifier, or loop diagram with clear labels.
- `结论收束页`: one strong visual metaphor plus a bottom conclusion strip.

Prompt pattern:

```text
画幅：<ratio>。为口播短视频生成一张浅色底、图文并茂的普通解析风竖版 PPT 演示页。页面文字：主标题「<title>」；分析卡片/标签「<label1>」「<label2>」「<label3>」；底部金句/结论「<takeaway>」。只渲染这些文字，不要添加其他中文、英文或假文字。画面表现：<segment meaning>。本页要研究的问题：<question>。版式类型：<comparison/mechanism/table/flow/photo-card/data/metaphor/conclusion>。视觉主体：<main visual subject>。构图：<ratio-aware layout>，文字区与主视觉区层级清楚，顶部大标题，中部图文解释区，底部结论条或留白。风格：浅色背景、清晰商业解析图、竖版 PPT 信息设计、真实照片/编辑插画/图标与图表结合、克制配色、手机端可读的粗标题和清楚正文。情绪：<tone>。
```

Good uses:

- Business commentary scenes.
- Product or brand analysis.
- Platform, consumption, technology, workplace, or market topics.
- Before/after or expectation/reality comparisons.
- Explaining a problem with a case table, mechanism diagram, funnel, scale, matrix, or photo-card grid.
- Turning horizontal reference-slide logic into vertical short-video PPT pages.

## Reference-Driven Style

When references are provided:

- Start the prompt by naming what to inherit from the reference.
- Preserve only the roles the user needs: person, composition, color, texture, or layout.
- Do not claim exact identity preservation unless a person reference is explicitly intended for that.
- If the reference contains text-heavy layout, inherit layout style but replace text with the exact storyboard text.
- If the reference is horizontal and the output ratio is vertical, inherit its content method, density, color, graphic devices, and reasoning style, then rebuild the layout for vertical composition.

Prompt addition:

```text
参考图使用：继承参考图的<role list>，但画面内容改为<segment meaning>。保持同一批图片在构图密度、色彩、质感和人物处理上的一致性。
```

## Negative Prompt Defaults

Use or adapt:

```text
避免杂乱背景、低清晰度、过度符号堆叠、无关人物、随机品牌标识、未指定文字、错误中文文字、乱码、小到不可读的文字、大段文字、水印、夸张表情、塑料质感、风格突变、与口播内容无关的装饰元素、把普通解析风做成单张 stock photo、把 16:9 横版版式硬挤进竖屏、深色压抑背景、男性人物换脸、去掉眼镜、变成西装商务男、变老。
```
