# 九类基础动效

默认竖屏 1080×1920，明确要求横屏才使用 1920×1080，布局重新安排；主题默认 navy-gold（网页深蓝金），保留 cream-red（米白黑红）。固定机位正常录制，模板适应现有主播，不要求录制时让位或配合动画。

## 按内容选择

| templateId / Composition | 用途与动作 | 验收重点 |
|---|---|---|
| keyword / KeywordTemplate | 铺垫→重点词放大、高亮 | 只强调当前关键词，跟随真实重音，不提前泄露 |
| callout / CalloutTemplate | 主播旁信息卡依次出现 | 保留主播位置，可遮肩手，入场全程避脸 |
| opinion-cards / OpinionCardsTemplate | 观点逐张累积、最后回顾 | 标题短、数量与可读时长匹配 |
| data-chart / DataChartTemplate | 计数→柱形增长→比较 | 同量纲与基线，数值、年份、单位可核查 |
| logic-flow / LogicFlowTemplate | 节点→箭头→下一层 | 因果/流程/并列关系准确，不强画因果 |
| comparison / ComparisonTemplate | 两列进入、共同比较 | 恰好两列，用同一组指标 |
| timeline / TimelineTemplate | 时间线和事件依次揭示 | 年份、顺序、阶段准确；复杂历史拆段 |
| evidence / EvidenceTemplate | 原始截图进入、重点框选 | 保留来源、日期与上下文，不用虚构卡片充当证据 |
| brand-map / BrandMapTemplate | 中心→连接→品牌展开 | 1–4个分支，超出时分组/定制；关系类型标清 |

模板是可用起点，不要求每条视频用齐九类。物体迁移、拆解、成本累积等继续使用 custom；只需要静态页或真实素材时走原路线。gallery 含虚构示例，正式项目替换原文与材料。

## 工程用法

```bash
node scripts/create-project.mjs --output <new-dir> --topic-key <slug> --title <title>
node scripts/create-project.mjs --output <new-gallery-dir> --topic-key nine-demo --title 九类模板 --gallery --theme navy-gold
```

默认竖屏、深蓝金；横屏加 `--orientation landscape`。manifest 中 theme 与七个 styleTokens 对应，颜色可按项目修改。旧 schemaVersion 1/2、ExampleClip 和自定义组件兼容，不强制升级旧成片。

clip 新增可选字段：

- templateId：上表 ID 或 custom；Composition 需对应 registry。
- presentation：fullscreen / overlay。位于 clip 顶层，不在 templateProps 中重复填写。
- renderProfile：h264（.mp4）/ prores-alpha（.mov）/ vp9-alpha（.webm）。overlay 使用透明档。
- templateProps：title、intro、keyword；items[{label,detail?,value?,year?,relation?,logoSrc?}]；value/unit；center；note/source；evidenceSrc/evidenceTitle/evidenceQuote；highlightRect；revealSeconds。
- revealSeconds 为每个主对象的入场秒数，按粗剪词句填写并与 motionDesign.beats 对齐；默认值只供样例。复杂退出、连续迁移或聚焦可直接扩展组件，不为适配模板修改人声。
- evidenceSrc 和 logoSrc 指 public 相对路径（或已授权 URL）。报告图片按 contain 展示；highlightRect 的 x/y/width/height 为证据卡容器百分比，需根据最终显示的截图位置测量，不能照搬原图百分比而忽略留白。当前基础组件支持框选；局部放大按同一素材和关键帧另编排。
- timeline：baseVideo、baseSha256、start/end（真实粗剪秒数）。存在时必须与 durationInFrames 匹配，motionDesign.timingSource=narration 并提供 timingEvidence。无录音样片使用 estimated，不伪造 hash 或标注同步。

### 透明浮层

templateProps.overlayRegion 为输出画布像素矩形 {x,y,width,height}，faceRegions 为取自实际底片、包含头部运动余量的保护矩形数组。浮层内容、影子和入场路径都应在允许区内；卡片可覆盖肩膀和手，不遮脸。尽量复用固定机位区域，逐片检查头部活动；没有底片只可标为待叠加验证。

模板不会移动主播。默认 overlay 不显示全屏标题、脚注或背景。全画布透明素材交给编辑器时，placement 为整幅画布；content_regions 填实际浮层包围区域（含运动/阴影余量），face_regions 用同一输出坐标。局部透明素材可直接给 placement，无需提前改变主播构图。

透明 MOV 用 ProRes 4444，WebM 用 VP9 alpha；MP4连续预览仅检查动作，不能证明透明正确。最终须抽查 alpha，并与真实底片合成检查。

## 共用时间表

统一 beat_id → 基准粗剪路径/SHA256 → start/end → trigger_times → 模板/呈现方式/主题 → 实际成片/音效 stem → 审片状态。工作台先规划，粗剪后补时标，Remotion 回填，剪辑消费，不各自重拆脚本。

音效片同时输出 .sfx.wav。全屏和浮层视频内声音均默认不直接使用，仅明确的 stem 通过编辑器 sfx 混入；人声源、入出点与增益保持，新增混音不要求与旧音轨同哈希。正常速度观看与试听仍为最终验收依据。

## 原网页视觉基准（v2）

九类分别复用原网页的静态视觉语言，动画改为逐帧计算，不将九类退化为同一张通用方框。

- 舞台：深蓝层次渐变、低对比网格、局部光晕及边缘暗部；标题/主体按原舞台比例排布，不把内容缩成页面中央小附件。
- 浮层：半透明浅蓝白卡、细亮边、外投影、细小图标与信息标签；主体固定，允许遮肩手，不遮脸。
- 观点卡：白/青/金三种材质渐变，错位缩进、厚度阴影、编号和语义图标，落位有轻微回弹。
- 图表：大号金数字、青与金渐变柱体、固定基线与年份，柱体从底部生长；长度与数值准确。
- 逻辑：带图标的蓝色渐变节点、逐段箭头，末节点金色实底。
- 对比：深蓝/金两块有材质的卡片、圆形搜索/目标图标、中央VS章，左右先后进入。
- 时间轴：延伸的金线、套环节点、分级年份与事件，最后节点强调。
- 证据：纸张、页眉、分隔线和段落结构；进入时轻微旋转/失焦后落稳，重点框选及标注；真实项目用原始截图，不能把演示材料当证据。
- 品牌：金色圆形中心、柔和外环与投影、曲线连接、蓝色渐变分支卡与行业图标；关系标签不可省略。

showPresenter 仅用于演示固定机位示意人物，正式项目默认关闭，叠加实际主播时不生成或移动主播。items 可配置 icon（content/algorithm/revenue/target/search/clock/chart/users/company/star/sports/digital/home）、tag 与已有真实 logoSrc。

leadText、kicker、conclusion 是可选文案；revealSeconds 按模板动作序列给秒数，示例值对齐原网页节奏。keyword 依次为小标签/铺垫/否定/划线/重点/补充，data-chart 为计数/各柱，comparison 为左右卡/VS/结果，evidence 为报告/框选/聚焦/标注，brand-map 为中心/各分支。不得把不同模板的时间数组机械复用。

米白黑红保留独立材质：米白纸张、米灰层次、红色重点与深色文字；不以整体滤镜硬套深蓝金。

当前参考版浮层/观点卡最多3项，时间轴/逻辑最多4项；超出时分组或定制，不缩小全部文字硬塞。核心图标为代码SVG，不依赖外部图标服务。两套材质分别编排，改品牌配色时同时检查渐变、前后景对比和 styleTokens。
