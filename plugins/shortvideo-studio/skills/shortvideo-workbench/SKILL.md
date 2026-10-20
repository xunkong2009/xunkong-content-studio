---
name: shortvideo-workbench
description: Orchestrate a complete or partial Chinese talking-head short-video workflow across script writing, generated image storyboards, Remotion motion graphics, footage search, and local editing. Use when several production stages must be coordinated.
---

## 分享版个人配置

用户当轮提供的材料和要求优先。需要语料库、主播照片或本地字体时，可读取当前项目的 `.xunkong-studio/config.json`（如存在）；相对文件路径以当前项目为基准。配置示例见插件根目录 `config.example.json`，不要改写安装目录。

未配置语料库时使用随包风格规则继续写作；未配置真人参考照片时可先交付提示词或无人像方案。需要复现某个真人且缺少参考时，向当前用户索取参考，不使用发布者的身份。配置文件中不存储 API Key、密码或账号 Cookie。

# 短视频全流程工作台

把选题、口播脚本、图文配图、Remotion 动效、真实视频素材和本地口播剪辑串成一个项目。优先复用同一份视觉节拍计划，避免专业 Skill 分别拆稿、重复工作或出现段落错位。

## 先选择工作模式

- 用户要参考博主动效、评价现有动效或优化相关 Skill：交给 `../shortvideo-remotion-producer/SKILL.md` 的参考研究与镜头打磨流程，抽样对比真实画面、记录时间点并交付改进或规则更新；不启动未请求的选段、批量生成或渲染。

- 用户只要写选题、标题、口播脚本、封面提示词或一般 AI 视频提示词：读取并执行 `../deep-biz-shortvideo-writer/SKILL.md`。
- 用户只要图文配图分镜或生成配图：读取并执行 `../shortvideo-image-storyboard/SKILL.md`。
- 用户只要 Remotion、动效视频、动态图表、多段横屏或竖屏 MP4、人物/产品动效或遮挡审片：读取并执行 `../shortvideo-remotion-producer/SKILL.md`。
- 用户只要搜索素材链接、筛选素材或下载视频：读取并执行 `../video-material-finder-downloader/SKILL.md`。
- 用户要剪录制好的口播、剪气口、去重录、插素材、加字幕或局部修正：读取并执行 `../talking-head-video-editor/SKILL.md`，只推进请求的剪辑阶段。
- 用户要两个或以上阶段，或明确说“全流程”：执行本 Skill 的完整流程。

只加载当前阶段需要的专业 Skill。专业 Skill 的事实核验、样图确认、下载边界、版权标注、剪口听审、音轨锁定和工具检查规则仍然有效，本 Skill 不覆盖这些限制。

## 完整流程

1. **简报与脚本。** 沿用已确认脚本与事实。默认 9:16、1080×1920；用户要求横屏才用 16:9、1920×1080。默认网页深蓝金 navy-gold，保留米白黑红 cream-red；主题与画幅、模板分别选。
2. **统一画面规划。** 阅读 references/visual-beat-plan.md，只拆一次 VisualBeatPlan，保留 B01 等编号。逐段选择主播、真实素材、静态配图或九类动效；动效记录 template_id、presentation、触发短语和素材需求，不要求用齐九类。此时可准备报告、Logo、图片和风格样例，正式片长不按估时锁死。
3. **录制与粗剪。** 用户固定机位、同一角度正常录制；不要求移位、让出一侧、换角度或配合动画手势。提供原片后交剪辑 Skill 去重录与气口、审听剪口，确定粗剪及 SHA256。默认确认粗剪后继续；已授权全流程则连续执行，实际听审状态单独记录。
4. **真实时间标定。** 阅读 references/editing-handoff.md，在确定的粗剪上标注每个节拍、触发短语和动作时间。省略节拍标未使用，新增节拍追加编号。没有录音时可做估算样片，标待对齐，不宣称已同步。
5. **制作与素材准备。** 按既有视觉模式路由专业 Skill；正式 Remotion 根据实际时间表制作。浮层适配已有主播画面，可覆盖肩手但避开脸部和字幕；脸部区域可沿片段复用并检查运动余量。只要单阶段时不强制原片或重走全流程。
6. **合成精剪。** Remotion 回填实际文件、渲染规格、声音stem和审片状态。说明图解按规划fullscreen；主播上的关键词默认无底框透明overlay，重点金黄、非重点白字黑边，左侧纵向展开或胸前横向呈现，保护头部。全屏保留口播，浮层保留主播；动画不合拍先改动效。素材原声排除，动作与重点文字音效独立混入一次；素材间不得夹闪现主播。
7. **按需字幕与包装。** 明确需要时才加普通字幕或封面；动作和重点文字音效按已授权制作范围主动设计，不自动加音乐。字幕与重点文字共用同一实际时间轴，重复时优先隐藏普通字幕，补充句错位避让；主播字幕放胸前偏下，图解按留白另排。合成或局部返工前读取 `../talking-head-video-editor/references/final-composite.md`。
8. **检查与交付。** 检查剪口、触发同步、脸部避让、字幕、数据终值、音效、素材与主播接口。保持原先确认门和直接制作授权规则，不重复确认；连续授权不等于已实际试听。交付索引、阶段文件及真实检查状态。

## 参考语料来源

脚本参考使用当前用户配置的 IMA 或明确提供的本地语料。读取或刷新时交给 `../deep-biz-shortvideo-writer/references/sample-ingest.md` 与 `../deep-biz-shortvideo-writer/references/ima-corpus.md`。未配置时沿用内置风格规则，不要求访问发布者的私人资料。

## 路由原则

- 有明确人物、学校、企业、产品、事件或历史现场时，优先 `network-footage`，并优先原始发布者或官方账号。
- `network-footage` 由素材下载 Skill 根据脚本节拍继续路由到国内社交平台、海外社交平台、官方媒体中心或历史开放档案；只使用免费来源，排除付费新闻、UGC、素材和订阅库，也不要求每个平台都搜索一遍。
- 需要通用实验室、办公室、编程、城市、工厂等氛围镜头时，优先 `stock-footage`。
- 需要静态解释抽象机制、数据关系、对比或总结时，优先 `generated-slide`。
- 需要关键词强调、观点分步呈现、数据变化、逻辑、对比、历史、证据或品牌关系时可选九类 `remotion-motion`；商品角色、规模累积、机制因果和行为循环继续使用定制动效。按表达任务决定，普通叙述可保留主播，不为每句套模板。
- `remotion-motion` 内部生成主体图片不等于 `ai-generated-clip`：前者由代码编排静态/分层资产，后者才是生成式视频；不因需要一张人物图而启动网络视频下载或整页分镜流程。
- 一般 B-roll 仅在真实素材难以获得、概念本身不存在可拍画面且用户接受生成视频时使用 `ai-generated-clip`。
- 不为每句话强塞 B-roll。观点转折、情绪表达和关键判断可以保留 `host-only`。
- 已有 `VisualBeatPlan` 时，任何专业 Skill 都不得重新切分整篇脚本；只能处理分配给自己的节拍。

## 项目目录

需要落地文件时，默认使用：

```text
<workspace>/output/shortvideo/<topic>-<YYYYMMDD-HHMMSS>/
├── project-index.md
├── script/
├── visual-beat-plan.md
├── storyboard/
├── motion/
├── materials/
├── cover/
└── editing/                 # 剪辑状态、计划、时间映射、审听包、各版本视频和字幕
```

不要求导入 ChatCut 或创建本地常驻应用。素材可以只交付可点击来源链接，也可以按用户授权下载为当前工作区内的可点击文件。需要免费账号登录或联系原作者免费授权的素材，保留精确页面和状态；需要付款的来源直接跳过。

## 最终交付

最终回复先说明已经完成哪些阶段，再提供项目索引或关键文件链接。对未执行的阶段写明“未请求”或“等待确认”，不要假装已生成或已下载。Remotion 成片必须同时提供连续播放预览、关键帧审片、独立 MP4、压缩包和媒体校验结果。网络素材旁必须保留原始来源、时间段、字幕/水印提示和简短版权说明。

剪辑交付提供当前阶段视频、计划与检查报告；字幕阶段另交 SRT。项目索引记录基准路径、SHA256、用户确认摘要、实际听审状态和待复核位置。未听审的粗剪标为“待试听粗剪”；不得以程序检查通过代替实际听审。
