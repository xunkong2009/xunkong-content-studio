# Workflow Rubrics

## General Rule

Every stage should reduce decisions for the next stage. Keep the outputs short, speakable, and directly writable.

## VideoTopicCard

Use this when evaluating a user-supplied direction or returning topic candidates.

```markdown
## VideoTopicCard N
- 话题/现象:
- 为什么值得讲:
- 核心判断:
- 适合的开头钩子:
- 是否需要补证:
```

Pass bar:

- The topic is strong enough to support a short spoken argument, not just a headline recap.
- `为什么值得讲` names the tension, mechanism, or contradiction that makes the topic worth airtime.
- `核心判断` is concrete enough to guide both outline and script.
- `适合的开头钩子` sounds like something that can be spoken naturally in the first 1-3 lines.
- `是否需要补证` clearly distinguishes between safe-to-state facts and parts that still need verification.

## VideoOutlineSpec

Use this when converting a chosen topic into a short-video structure.

```markdown
# VideoOutlineSpec
## 一句话主轴
## 目标时长
## 结构骨架
### 开头钩子
内容说明
### 第一段
内容说明
### 第二段
内容说明
### 第三段
内容说明
### 收尾判断
内容说明
## 每段任务
- 开头钩子:
- 第一段:
- 第二段:
- 第三段:
- 收尾判断:
## 节奏提醒
- 提醒:
## 禁写项
- 避免:
```

Pass bar:

- The outline is built for a 120-240 second spoken script unless another duration was requested.
- `一句话主轴` is strong enough to keep the whole script aligned.
- `结构骨架` reads like a speakable progression rather than a long article outline.
- Each section has one clear job and pushes the argument forward.
- `节奏提醒` helps control speed, density, and hook timing without becoming a production memo.
- `禁写项` actively prevents drift into公众号腔, bullet腔, or generic motivation speech.

## VideoScriptPack

Use this when generating titles and the final script.

```markdown
# VideoScriptPack
## 标题候选
1.
2.
3.
4.
5.
## 封面/开场句
- 封面文案:
- 开场句:
## 口播脚本
## 分段卡点
- 0-15秒:
- 15-45秒:
- 45-90秒:
- 90秒后:
## 需保守表述处
- 如有:
```

Pass bar:

- The five titles are meaningfully different in framing, not micro-variants.
- `封面/开场句` is tight and high-pull without sounding like trashy clickbait.
- `封面/开场句` should preferably enter through conflict, reversal, collapse, or exposed contradiction rather than slow background setup.
- `口播脚本` sounds natural when read aloud and keeps a clear line of thought.
- `口播脚本` defaults to readable paragraph blocks rather than overly fragmented line-by-line formatting, unless the user asks for a cue-sheet style.
- Reason blocks should usually land as `sharp claim + concrete proof/example + plain-language interpretation`, especially for business and brand topics.
- `分段卡点` is light, useful, and timing-oriented; it should not turn into shot-by-shot storyboarding.
- `需保守表述处` flags uncertain or current-sensitive claims when needed, and can say `无` when none apply.

## CoverPromptPack

Use this when the script, title set, or hook is confirmed enough to support Douyin-style cover image prompts.

```markdown
# CoverPromptPack
## 封面总设定
- 比例:
- 风格:
- 主播设定:
- 标题摆放:
- 文案策略:
- 统一要求:
## Style A: 组合排版
### Prompt 1
- 适用标题:
- 顶部白字文案:
- 画面逻辑:
- Prompt:
- 负向约束:
### Prompt 2
- 适用标题:
- 顶部白字文案:
- 画面逻辑:
- Prompt:
- 负向约束:
## Style B: 互动入景
### Prompt 3
- 适用标题:
- 顶部白字文案:
- 画面逻辑:
- Prompt:
- 负向约束:
### Prompt 4
- 适用标题:
- 顶部白字文案:
- 画面逻辑:
- Prompt:
- 负向约束:
```

Pass bar:

- The pack is generated only after the script, hook, or title direction is stable enough to support a clear cover concept, unless the user explicitly wants exploratory covers.
- `封面总设定` locks `3:4` portrait logic by default, the host framing, the top text-safe zone, and the overall visual density.
- The output includes at least one workable Style A prompt and one workable Style B prompt unless the user requested only one style.
- `顶部白字文案` is short, readable, and aligned with the cover concept.
- `Prompt` includes host framing, scene elements, composition logic, lighting or mood, and a clear upper area for white copy.
- `负向约束` removes common failures such as cluttered backgrounds, tiny host scale, distorted hands, unreadable headline area, or accidental UI overlays.

## VideoPromptPack

Use this when the script is confirmed and the user wants prompts for Jimeng-like video-generation models.

```markdown
# VideoPromptPack
## 视觉总设定
- 画幅:
- 风格:
- 主体设定:
- 连贯性要求:
## Prompt 1
- 对应脚本段:
- 建议时长:
- Prompt:
- 负向约束:
## Prompt 2
- 对应脚本段:
- 建议时长:
- Prompt:
- 负向约束:
## Prompt 3
- 对应脚本段:
- 建议时长:
- Prompt:
- 负向约束:
```

Pass bar:

- Prompts are generated only after a script exists and is treated as confirmed unless the user explicitly wants exploratory prompts.
- `视觉总设定` locks aspect ratio, realism/stylization, main character logic, and continuity so clips do not look like unrelated fragments.
- Each prompt maps to one script beat or one visual idea and remains executable by a general video model.
- `Prompt` includes subject, action, scene, camera language, lighting or mood, and style cues.
- `负向约束` removes common model failure modes such as wrong text, extra limbs, chaotic crowds, UI clutter, or style drift when relevant.
- The pack is short enough to use directly, usually 4-8 prompts instead of dozens of micro-shots.

## Failure Modes

- Treating a hot topic as automatically worth covering.
- Writing a long article outline and relabeling it as a short-video structure.
- Producing a script that reads nicely on paper but is awkward to say out loud.
- Using overcooked rhetorical contrast such as repeated `不是……而是……` to simulate force.
- Returning titles that differ only by one or two words.
- Giving cover-image prompts before the title or hook direction is stable enough to support one clear cover.
- Mixing composite layout and interaction-in-scene logic without making either one legible.
- Giving video prompts before the script logic is stable.
- Writing one giant visual prompt that contains the whole script instead of splitting it into shot-sized units.
