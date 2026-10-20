# Cover Prompting

## Purpose

Use this guide when the user wants the confirmed short-video script, title set, or hook turned into prompts for Douyin-style cover images. The goal is to produce a few strong thumbnail concepts that are immediately usable for image generation and later text layout.

## When To Use

- The script or title direction is already stable enough to support a clear cover angle
- The user asks for `封面图 prompt`, `抖音封面`, `缩略图 prompt`, `封面图提示词`, or similar packaging help
- The user wants cover prompts after the script is done, or explicitly wants the skill to include that stage

## Default Assumptions

- Use `3:4` portrait ratio unless the user specifies another ratio
- Use realistic live-action unless the topic clearly needs collage, illustration, or graphic design language
- Return 4-6 prompts total unless the user requests another quantity
- Default to Chinese prompts when delivering cover-image prompts, unless the user explicitly asks for English or bilingual prompts
- Use the current user's uploaded or project-configured host reference. Without a reference, deliver prompts or a no-presenter concept; request a reference before reproducing a specific person.
- When writing cover prompts or generating cover images, explicitly say the host must match the same person from the current user's provided reference photos; do not describe or generate a generic host in place of the reference identity
- Include two styles by default:
  - Style A: host portrait plus background information or scene elements are composited and designed together, but remain separate layers without direct interaction
  - Style B: host directly holds, uses, points to, or is embedded in the product or scene, creating a visible interaction
- Reserve the upper 20-35% of the image for large white headline copy

## Workflow

1. Confirm the script or title direction is stable enough to support one clear cover angle.
2. Extract the most thumb-stopping frame from the script:
   - product risk
   - business reversal
   - category conflict
   - brand tension
   - surprising judgment
3. Decide whether the cover should emphasize:
   - host authority
   - product object
   - storefront / scene
   - data or information board
   - mixed composition
4. Lock one clean cover system in `封面总设定`:
   - ratio
   - host framing
   - current user's host reference source
   - text zone
   - visual density
   - palette
5. Write prompts in two buckets:
   - Style A composition prompts
   - Style B interaction prompts
6. Provide a short white headline suggestion for each prompt. Default to separate copy guidance instead of depending on precise Chinese text generation inside the image.

## Prompt Rules

- One prompt should equal one cover concept.
- Keep the host visually dominant enough to read on a phone screen.
- Mention the upper text-safe zone explicitly.
- Use short, concrete background elements: storefront sign, product close-up, category shelf, menu board, chart card, headline panel, price tag, or crowd blur.
- If using brand or celebrity references, prefer descriptive framing unless the user explicitly wants direct likeness recreation.
- Keep design language intentional: depth, contrast, layering, and headline space matter more than scenic detail.
- Favor chest-up or waist-up host framing for readability.
- Every prompt must anchor the host to `使用本次用户指定的主播参考照片，保持同一人身份与约定造型`. When the host is already established, do not repeat detailed appearance or introduce a wardrobe change.
- Every prompt must include a negative host constraint: `不要换人，不要擅自改变参考人物的身份、造型或服装`.

## Style Notes

### Style A: Composite / Designed Layout

- The host and the background information are visually combined through layout, layering, scale contrast, headline placement, and depth of field.
- The host does not need to touch the product or physically merge with the scene.
- Good for analytical, business, and media topics where background information carries meaning.

### Style B: Interaction / In-Scene

- The host should visibly hold, wear, use, inspect, compare, point to, or stand inside the key scene.
- The interaction should communicate the topic before the viewer reads the headline.
- Good for product, retail, food, and consumer topics where action improves clickability.

## Failure Modes

- Treating the cover like a video still with no design hierarchy
- Letting the headline area become busy or low-contrast
- Writing prompts so generic that the image looks like stock portrait photography
- Making the host too small to read at thumbnail size
- Asking the image model to render long Chinese copy perfectly when clean text space would work better

## 固定主播、固定标题的四方向请求

用户说“主播是既定主播”时，提示词以约定参考图保持同一人，侧重构图与概念，不重复冗长外貌描述，也不擅自换装。用户固定标题时各方案逐字一致，允许换行，不另拟标题或添加副标题；提示词数量按用户请求。

四方案应有不同视觉机制或人物动作，不能仅换背景颜色。默认3:4、前景主播足够大、顶部约三分之一干净大白字区，可用黑描边与少量强调笔触；不要把视频动效的金黄重点规则强制套在封面标题上。只要提示词不提前出图。
