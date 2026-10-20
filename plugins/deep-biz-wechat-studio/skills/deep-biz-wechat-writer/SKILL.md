---
name: deep-biz-wechat-writer
description: 商业公众号全流程写作工具：适用于商业分析、营销策略、品牌变化、科技趋势与社会现象类文章，覆盖选题、调研、大纲、写作、审校、标题包装、IMA 语料调用与公众号 HTML 导出。用户要求整篇文章、推进完整流程或从任一阶段继续时使用。
---

## 分享版个人配置

用户当轮提供的材料和要求优先。需要语料库、主播照片或本地字体时，可读取当前项目的 `.xunkong-studio/config.json`（如存在）；相对文件路径以当前项目为基准。配置示例见插件根目录 `config.example.json`，不要改写安装目录。

未配置语料库时使用随包风格规则继续写作；未配置真人参考照片时可先交付提示词或无人像方案。需要复现某个真人且缺少参考时，向当前用户索取参考，不使用发布者的身份。配置文件中不存储 API Key、密码或账号 Cookie。

# 商业公众号全流程写作器

## 概述

把一篇深度商业与营销分析公众号文章，从选题一路跑到终稿、包装与公众号 HTML 导出。所有阶段都应被当作同一个编辑系统的一部分：语气要一致，事实与推断要分开，最后写出来的东西要像一个有经验的操盘手，而不是一个会总结材料的通用模型。

## 工作流

1. 先读 `references/style-layer.md`，把其中的语气、论证节奏、禁用表达与包装偏好应用到所有阶段。进入大纲、正文或审校时，再读 `references/author-voice.md`，落实作品联想、生活场景与作者在场的写法
2. IMA 为可选参考语料来源，读取当前用户项目配置中的文章和约稿目录；路径与读取规则见 `references/ima-corpus.md`。未配置或不可用时继续使用已沉淀的 style layer，不阻断普通写作，也不声称完成本次语料刷新
3. 如果用户明确要求刷新 IMA 语料、校准个人风格或读取既有笔记，再走 `references/sample-ingest.md`。用户给了文章链接、上传文件或本地样本目录路径时，也按该文件的对应分支处理
4. 判断入口模式：
   - 用户要整篇文章时，按 `Topic -> Research -> Outline -> Writer -> Style Critic -> Packager -> Typesetter` 推进需要的阶段；已有成果直接沿用，包装和排版仅在请求包含它们时执行
   - 用户只要某一个步骤时，也先读 style layer 与对应 rubric，再只执行这一步
5. 研究型步骤前必须先读 `references/source-policy.md`
6. 读 `references/workflow-rubrics.md`，只读取当前阶段的 schema 与通过标准；用户指定的交付形式优先
7. 输出阶段结果时使用对应 schema：`TopicCard`、`ResearchBrief`、`OutlineSpec`、`ArticleDraft`、`PolishReport`、`PackagingSet`、`HTMLExport`、`ReflectionNote`
8. 只交付用户请求的成稿和后续资产。反思按需提供；仅在用户明确要求保存记忆时，按当前环境的记忆写入规则执行。

## 入口场景

- `选题`：调用 topic-engine 逻辑，返回 3-5 个 `TopicCard`
- `深度调研`：围绕一个已选题目或论点生成 `ResearchBrief`
- `生成大纲`：把题目和调研转成 `OutlineSpec`
- `写成文`：把已批准的大纲展开成 `ArticleDraft`
- `审校润色`：输出 `PolishReport + FinalDraft`
- `标题与配图`：输出一个 `PackagingSet`
- `公众号排版`：把 `FinalDraft` 转换为一个 `HTMLExport`
- `导出公众号 HTML`：输出带严格内联样式的 `HTMLExport`
- `全流程写一篇`：跑完整链路，按请求返回最终文章、包装及公众号 HTML

## 工作规则

- 默认使用简体中文，除非用户明确要求其他语言
- 最终文章要面向读者，而不是面向框架，不要把内部 rubric 暴露给用户
- 最终成文优先自然段，而不是满屏 bullet
- 避免空心的力度词、咨询腔套话与公式化 AI 转折
- 推断必须标成推断；不能直接支持的结论，要说明已知与推断边界
- 当用户给的是热点题时，不要先夸它“很重要”，要先判断它背后的机制、激励或结构变化值不值得写

## 伴随 skill

- `deep-biz-topic-engine`（商业选题雷达）
- `deep-biz-research`（商业深度调研）
- `deep-biz-outline-engine`（商业文章大纲引擎）
- `deep-biz-writer`（商业长文写作器）
- `deep-biz-style-critic`（商业文章风格审校器）
- `deep-biz-packager`（商业文章包装器）
- `deep-biz-typesetter`（公众号排版导出器）
- `ima-skill`（默认参考语料读取；见 `references/ima-corpus.md`）
- `youdaonote`（仅在用户明确要求操作有道云时使用）

当用户只要单一步骤时，可以直接调用这些 companion skills 的逻辑；当本 master skill 处于激活状态时，要镜像它们的规则，而不是重新发明一套工作流。

## 参考地图

- `references/style-layer.md`：语气与反 AI 质感的核心约束，必须先读
- `references/author-voice.md`：作品、生活场景如何进入论证，以及审校时保留个人笔触的规则
- `references/author-voice-evidence.md`：语料校准时按需读取的笔记定位与样本边界
- `references/source-policy.md`：信源层级、交叉验证规则与证据标准
- `references/workflow-rubrics.md`：各阶段交付物与 markdown schema
- `references/sample-ingest.md`：如何优先从 IMA 语料提炼风格，以及何时退回链接、粘贴文本或本地文件
- `references/ima-corpus.md`：IMA 知识库路径、内部定位和正文读取规则
- 如果 IMA 语料暂时不可用，普通写作继续使用已沉淀的 style layer；只有用户明确要求刷新 IMA 语料时，才暂停该刷新步骤并报告原因

## 完成检查清单

- 选题背后有值得展开的机制，而不是只有表面热度
- 调研里的证据足以支撑论点，或清楚标出了仍未证实之处
- 大纲有向前推进的论证力，不是一堆观察堆叠
- 文章读起来像一个人在深入思考，而不是多个 bullet list 缝起来
- 最终润色真正去掉了 AI 质感，并把作者判断磨尖
- 包装只在终稿之后执行一次，标题与视觉方案不在写作和审校阶段重复生成
- HTMLExport 使用内联样式并可直接用于公众号后台
- 请求的交付物完整；不附加未请求的记忆更新
