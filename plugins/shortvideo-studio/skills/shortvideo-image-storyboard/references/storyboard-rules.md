# Storyboard Rules

## Input Reading

Before segmenting, identify:

- Topic: what the script is about.
- Audience: who should understand or care.
- Content type: business analysis, product explanation, knowledge explainer, emotional viewpoint, news commentary, or other.
- Tone: calm, sharp, anxious, optimistic, critical, playful, serious.
- Visual constraints: aspect ratio, references, brand, person, platform, forbidden elements.
- Text constraints: whether the user wants big title text, data labels, no text, or post-production text boxes.

If the script relies on unstable facts, verify them before using them as visual claims.

## Segmentation

- For `白板图文讲义风`, target about 100 Chinese characters per page.
- For `普通解析风`, target one complete analytical beat per image: one problem, mechanism, contrast, case, data point, or conclusion. This is usually 80-140 Chinese characters, but a dense vertical page can carry slightly more if the text remains readable.
- Prefer semantic units over exact length.
- Keep a complete claim, example, or contrast in one segment when possible.
- If a sentence is longer than the target but contains one indivisible idea, keep it together.
- If two short sentences form one logical beat, merge them.
- For dense scripts, slightly increase image count rather than forcing overloaded prompts. For `普通解析风`, preserve the "researching a problem" feel by making each page answer one clear question.

Good segment types:

- Hook or problem setup.
- One mechanism or cause.
- One contrast between old and new.
- One concrete example.
- One emotional turn.
- One conclusion or judgment.

## Visual Intent

Assign exactly one primary intent per image:

- `开场建立`: introduce the topic and mood.
- `概念解释`: make an abstract idea visible.
- `证据承接`: visualize a data point, report, product, or public signal without inventing unsupported detail.
- `冲突呈现`: show tension between two forces.
- `对比转折`: compare past vs present, expectation vs reality, old model vs new model.
- `情绪强化`: make the audience feel pressure, confusion, trust collapse, excitement, or relief.
- `类比隐喻`: use a metaphor when direct depiction is weak.
- `节奏转场`: reset visual rhythm between dense points.
- `结论收束`: give the final judgment a memorable visual.

## On-image Text

These images are for spoken short-video support, so the default is a presentation-like image with both text and visuals.

Default text structure for `白板图文讲义风`:

- `标题/核心论点`: a complete page headline or argument. It may be a question, judgment, or step title.
- `解释文字块`: one concise explanatory paragraph or 2-3 short lines that summarize the evidence, mechanism, or contrast.
- `图解主体`: the central drawing, diagram, table, scene, flow, comparison, or metaphor.
- `结论贴纸`: one sticky-note style takeaway that states what the audience should remember.

Default text structure for `普通解析风`:

- `主标题`: a clear question, judgment, or section title.
- `视觉主体`: the central PPT visual: comparison, matrix, flow, data shape, case table, photo cards, icon cards, or metaphor diagram.
- `分析卡片/标签`: 2-4 short blocks that explain the evidence, mechanism, contrast, or example.
- `底部金句/结论`: optional but preferred when the page needs a memorable takeaway.

Rules:

- The image should never contain the full voiceover.
- `白板图文讲义风` must include title/core argument, diagram subject, explanation text block, and conclusion sticky note.
- Do not use more than 5 text blocks unless the user explicitly asks for dense PPT pages.
- Use exact text in the prompt. Put quoted text in the storyboard before the prompt.
- Prefer readable page text: a strong title, a compact explanation, and one memorable conclusion.
- If exact Chinese rendering fails, simplify the text and regenerate once. If still unstable, create a clean visual layout with reserved text boxes for later editing.
- For legal, medical, financial, and current-fact claims, verify before making them prominent on image.

## Reference Image Priority

References outrank default style rules when the user says to follow them.

If the references are horizontal but the requested output is vertical, inherit their analysis method and design language rather than their canvas shape. Useful things to inherit include:

- Content richness: a title plus several evidence blocks, labels, examples, or a concluding line.
- Presentation devices: comparison columns, before/after pairs, tables, funnels, scales, flowcharts, circular mechanisms, callout boxes, photo cards, icons, arrows, and highlighted keywords.
- Visual tone: shallow light background, restrained business colors, black/dark-gray Chinese type, red or green accent marks, clean slide spacing, and a problem-research feeling.

Redesign these into the requested ratio, especially `9:16`, `3:4`, or `4:5`. Use vertical stacking, top-title/middle-visual/bottom-takeaway structure, or two/three stacked modules instead of squeezing a 16:9 layout into a narrow frame.

## Presenter Reference

Use the current user's uploaded or configured reference images. Do not refer to the publisher's cloud files or reuse a publisher identity anchor. Preserve an established identity and clothing unless the current user requests a change. Without a reference, a no-presenter concept or a clearly generic character is acceptable; reproducing a specific person requires that user's reference.

For each reference image, label the intended role before prompting:

- `人物参考`: identity, age, styling, pose, expression.
- `构图参考`: framing, camera angle, layout, subject scale.
- `色彩参考`: palette, contrast, lighting mood.
- `质感参考`: hand-drawn, cinematic, editorial, paper texture, realistic, 3D, etc.
- `版式参考`: text area, hierarchy, graphic layout.

If multiple references conflict, ask the user which one has priority. Do not average conflicting identity, layout, or style signals.

## Aspect Ratio Rules

- Default ratio is `9:16`.
- If the user gives any other ratio, use that ratio everywhere in the storyboard and generated images.
- For `9:16`, favor strong vertical composition, clear central subject, and enough negative space for captions if needed.
- For `9:16`, keep title and key labels inside the upper or middle safe area, away from platform UI overlays and lower subtitles.
- For `9:16` ordinary analysis pages, prefer vertical PPT modules: top title, middle diagram/photo-card/comparison area, bottom takeaway or conclusion strip. Keep side-by-side comparisons to two columns at most, and use stacked cards when text would become small.
- For `16:9`, favor horizontal scene logic, side-by-side comparison, or wider environment.
- For `1:1`, keep the subject readable from the center outward.
- For `4:5` or `3:4`, balance vertical short-video readability with more editorial spacing.

## Image Generation Gate

When the user asks to generate images:

- If references are provided and their role is clear, generate the sequence in order.
- If no references and no prior style/batch authorization are provided, generate only image 1 first and ask whether to continue with the same style. Reuse existing approval; explicit direct batch authorization does not require another confirmation.
- If the user asked only for prompts, do not generate images.
- If the first image is rejected, revise the style guide and regenerate image 1 before continuing.

Use the imagegen skill / built-in image tool for actual images. This skill should not introduce a new image-generation script.

## Markdown Output

Default fields per image:

- `图号`
- `对应文案`
- `画面任务`
- `页面文字`
- `构图与主体`
- `画面细节`
- `Prompt`
- `Negative prompt`
- `生成状态`

Keep prompt text specific and scene-based. Include the exact on-image text and its layout. Avoid vague style stacking.
