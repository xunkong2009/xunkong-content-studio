# Workflow Rubrics

## General Rule

Every output should help the next stage make fewer decisions, not more.

## TopicCard

Use this when returning topic candidates.

```markdown
## TopicCard N
- 事件本身:
- 值得深挖的商业/社会机制:
- 潜在反常识角度:
- 可验证证据密度:
- 建议文章方向:
```

Pass bar:

- Topic is current enough to matter or durable enough to justify a non-news feature.
- Topic contains a real mechanism, not just a reaction.
- Topic points toward a thesis the article could own.

## ResearchBrief

Use this when converting a topic into an evidence-backed brief.

```markdown
# ResearchBrief
## 研究问题
## 核心论点
### 论点 1
- 证据:
- 来源:
- 可信度:
- 推断说明:
### 论点 2
- 证据:
- 来源:
- 可信度:
- 推断说明:
## 仍待验证的问题
## 可直接进入文章的洞察
按需附作品或场景候选，简记材料、来源定位、核验状态、解释用途与适用边界；无合适材料可省略。
```

Pass bar:

- Each major claim has evidence.
- Facts and inference are clearly separated.
- Brief is selective and article-usable.

## OutlineSpec

Use this when turning a brief into a writing plan.

```markdown
# OutlineSpec
## Summary
- 文章主轴:
- 判断力度:
- 核心命题:
## 文章骨架
### 开篇
内容说明
### 小标题 1
内容说明
### 小标题 2
内容说明
### 小标题 3
内容说明
### 结尾
内容说明
## Evidence Cues
- 证据提醒:
## Acceptance
- 成稿标准:
## Assumptions
- 默认前提:
```

Pass bar:

- Another writer could draft from it immediately with no structural ambiguity.
- `Summary` stays brief and does not expand into a planning memo.
- `文章骨架` is the primary body of the outline.
- Each subtitle in `文章骨架` has a clear job.
- If a work or scene is selected, the relevant section identifies its explanatory job and connection back to the thesis; `Evidence Cues` retains source and verification limits. No required quote or scene count.
- The opening raises the real problem and the ending resolves upward rather than merely stopping.
- `Evidence Cues`, `Acceptance`, and `Assumptions` remain concise and useful.
- The outline contains no `Run Plan` section and no placeholder wording like `大概写什么`.

## ArticleDraft

Use this when drafting the article.

```markdown
# ArticleDraft
## 暂定标题
## 正文
```

Pass bar:

- Default length lands in the 3000-5000 Chinese character range unless the user requested otherwise.
- The body is paragraph-led, not bullet-led.
- The writing contains analysis, not just paraphrased research.
- Where useful, concrete choices and cultural associations make the argument recognizable. References have an explanatory or narrative purpose; first-person experiences are traceable. A strong factual article may use none.
- Default to bolding key judgment sentences or especially important takeaway lines in the final draft, but keep the emphasis sparse so the article does not look over-marked.
- Keep one working title only. Final title generation and visual packaging belong to `PackagingSet`.
- Preserve source charts or images only when they already exist in the research materials and materially support the argument.

## PolishReport

Use this when critiquing and rewriting a draft.

```markdown
# PolishReport
## 主要问题
### 问题 1
- 位置:
- 问题类型:
- 为什么削弱文章:
- 修改方向:
## FinalDraft
```

Pass bar:

- Critique is concrete.
- Rewriting actually fixes the identified problems.
- Final draft reads like one authorial pass.
- Preserve useful authorial details, colloquial turns and cultural connections while removing ornamental name-dropping or unsupported scenes. If style changed materially, briefly identify what was retained and why.
- If AI-style contrast phrases such as `不是……而是……` are too frequent, call that out explicitly as a separate problem type.
- Do not generate alternate-title sets or new visual concepts here. Those belong to `PackagingSet`.
- Preserve already verified source charts or images when they are integral to the article.

## PackagingSet

Use this when generating distribution assets.

```markdown
# PackagingSet
## 标题候选
1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
## 图像 Prompts
### Prompt 1
- 建议位置:
- 视觉任务:
- Prompt:
### Prompt 2
- 建议位置:
- 视觉任务:
- Prompt:
### Prompt 3
- 建议位置:
- 视觉任务:
- Prompt:
```

Pass bar:

- Ten titles are meaningfully differentiated.
- Prompts are visually actionable, not abstract summaries.
- Each prompt has a clear insertion point and editorial purpose.

## HTMLExport

Use this when exporting a finished article for WeChat backend copy-paste.

```markdown
# HTMLExport
## 标题
## 正文 HTML
## TypographySpec
- 外层容器：<section ...>
- 正文段落：<p ...>
- 正文字体：15 号
- 正文字体颜色：#545454
- 一级小标题：17 号，#3daad6
- 一级小标题标签：<h1 ...>
- 二级小标题：16 号，标题前带 ●
- 二级小标题标签：<h2 ...>
- 两端缩进：16
- 行间距：1.75
- 字间距：1
- 默认图片：<img ... />
```

Pass bar:

- `正文 HTML` contains directly copyable HTML with inline styles and no explanatory chatter mixed into the body.
- The body is wrapped in the required outer `<section>` with the full fixed inline style string.
- First-level subheads use the required `<h1>` style, and second-level subheads use the required `<h2>` style with a leading `●` only when they actually exist.
- Paragraphs use the required `<p style="margin-bottom: 15px;">`.
- Key judgment sentences and crucial takeaway lines preserve or receive `<strong>` or `<b>` emphasis in the exported HTML, but the emphasis should stay sparse and editorially selective.
- Source images are preserved in-place whenever the original article exposes usable image data.
- If source images are unavailable, at least one opening placeholder image is inserted, and additional placeholders are added only where the article clearly needs image slots.
- `TypographySpec` is fixed, complete, and matches the exported HTML rules.

## ReflectionNote

Use this after the article is complete.

```markdown
# ReflectionNote
- 本篇做得好的地方:
- 可以更好的地方:
- 新发现的写作套路:
- 应写入记忆库的内容:
```

Pass bar:

- Captures reusable lessons, not self-praise.
- Names at least one pattern worth keeping or avoiding.
