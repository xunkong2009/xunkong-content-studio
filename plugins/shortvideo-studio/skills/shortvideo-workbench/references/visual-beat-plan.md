# VisualBeatPlan 统一交接规范

`VisualBeatPlan` 是整个插件唯一的脚本切片结果。先生成计划，再把不同节拍分配给图文分镜、Remotion 动效、真实素材搜索下载或 AI 视频提示词流程。

## 项目字段

```yaml
project_title: 主题名
script_status: draft | confirmed | user_provided
estimated_duration_seconds: 180
aspect_ratio: 9:16
visual_style: 普通解析风
delivery_mode: links-only | review-first | search-and-download | prompts-only | generate | motion-render
```

## 节拍字段

每个节拍必须包含以下字段：

| 字段 | 含义 |
|---|---|
| `beat_id` | 稳定编号，如 `B01` |
| `script_excerpt` | 对应口播原文，不随意改写 |
| `narration_seconds` | 预计口播秒数 |
| `narrative_job` | hook、证据、人物、机制、案例、转折或结论 |
| `visual_mode` | 见下方枚举 |
| `visual_job` | 画面需要让观众看懂什么 |
| `source_preferences` | 来源优先级或明确平台 |
| `search_queries` | 中英文搜索词，可为空 |
| `named_entity_required` | 必须准确出现的人、组织、产品或地点，可为空 |
| `on_image_text` | 图文页要显示的标题、数字或短标签，可为空 |
| `suggested_duration_seconds` | 建议插入时长；按作用与实际口播决定，动效注明整段覆盖还是局部插片 |
| `asset_status` | planned、shortlisted、downloaded、generated、rendered、host-only 或 blocked |
| `rights_note` | 素材授权、署名或用途提醒，可为空但不能伪造 |

## visual_mode 枚举

- `host-only`：主播持续出镜，不加外部素材。
- `network-footage`：YouTube、微博、B站等网络视频中的人物、机构、事件或产品画面。
- `stock-footage`：Pexels、Pixabay、Mixkit 等素材网站中的通用 B-roll。
- `generated-slide`：图文并茂的解析页、数据页、机制图或结论页。
- `remotion-motion`：根据观看问题设计主体变化与注意力调度，按需复用或生成主要人物/产品等图片，由代码编排并准确呈现文字、数字和关系，制作独立动效 MP4。主体图片沿用该节拍编号，不另拆整篇脚本。
- `ai-generated-clip`：需要文本生成视频的概念镜头。
- `mixed`：两个方案同时保留；需注明主用与备用，或明确叠加方式。

## Markdown 交付模板

```markdown
## VisualBeatPlan

项目：...
脚本状态：confirmed
预计时长：180 秒
画幅：9:16
交付模式：search-and-download

| Beat | 对应口播 | 秒数 | 叙事任务 | 视觉模式 | 画面任务 | 搜索词/页面文字 | 状态 |
|---|---|---:|---|---|---|---|---|
| B01 | ... | 6 | hook | network-footage | 建立学校与 AI 的关联 | 清华姚班 AI | planned |
| B02 | ... | 8 | 数据证据 | generated-slide | 展示核心人数与成果 | 1200 / 750 / 60 | planned |
```

## 交接规则

1. 图文分镜 Skill 只处理 `generated-slide` 和需要图文页的 `mixed` 节拍。
2. 素材搜索下载 Skill 只处理 `network-footage`、`stock-footage` 和需要真实素材的 `mixed` 节拍。
3. Remotion 动效 Skill 只处理 `remotion-motion` 和明确分配给 Remotion 的 `mixed` 节拍，并把 `beat_id` 写入项目清单、审片文件和输出文件名。
4. 动效 Skill 可在分配到的 remotion-motion 节拍内调用 imagegen 准备必要主体图，按动效 Skill 的 `references/hybrid-assets.md` 登记来源、姿态和提示词；素材准备不改 visual_mode，也不另触发 generated-slide 的整页样图确认。
5. 商业短视频写作器只为 `ai-generated-clip` 节拍输出视频生成 prompts，并按用户请求处理封面。
6. 资产文件名或清单项以节拍编号开头，例如 `B07-斯坦福校园.mp4`。
7. 某条素材失败时保留原节拍编号，更新状态并给替代方案，不重新编号后续节拍。

8. 本地口播剪辑沿用节拍编号，并按 `editing-handoff.md` 将节拍和本地资产映射到粗剪基准的实际时间轴。估计口播秒数不作为最终剪辑入出点；交接保留未使用节拍及其原因。

## 动效扩展（可选，兼容原字段）

remotion-motion 节拍新增 template_id（九类ID或 custom）、presentation（fullscreen/overlay）、theme（cream-red/navy-gold）、trigger_phrases、asset_needs。estimated 秒数仅规划；粗剪后回填 base_video、base_sha256、start/end（秒）、trigger_times。overlay 另记 face_regions 和字幕区域，允许肩手覆盖，不要求主播挪位置。字段及参数对照 Remotion 的 references/nine-templates.md；不另拆稿。

## 文字与声音的共同规划

需要动效/字幕时，为相关节拍记录`text_role`（explanation/keyword）、`caption_policy`（suppress/reposition/keep）、`caption_position`（需要时）、`caption_windows`和`sound_events`。每个事件保留触发台词、实际frame/seconds、动作含义与声源；关键词不固定数量。原有字段和旧计划继续兼容，不为补字段重编号。

图文配图与说明动效可以有独立底色；主播上的重点文字优先透明无底框，金黄重点+白字黑边，避免把整段重点文字一律做全屏。仅有脚本先填触发短语，粗剪后回填帧点，不提前宣称同步。
