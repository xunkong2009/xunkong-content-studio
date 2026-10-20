---
name: deep-biz-typesetter
description: 公众号排版导出工具：适用于已完成文章，覆盖带严格内联样式的 HTML 正文导出，便于浏览器渲染后粘贴到公众号后台。
---

## 分享版个人配置

用户当轮提供的材料和要求优先。需要语料库、主播照片或本地字体时，可读取当前项目的 `.xunkong-studio/config.json`（如存在）；相对文件路径以当前项目为基准。配置示例见插件根目录 `config.example.json`，不要改写安装目录。

未配置语料库时使用随包风格规则继续写作；未配置真人参考照片时可先交付提示词或无人像方案。需要复现某个真人且缺少参考时，向当前用户索取参考，不使用发布者的身份。配置文件中不存储 API Key、密码或账号 Cookie。

# 公众号排版导出器

## 概述

把最终文章整理成适合公众号后台发布的版本。本 skill 默认输出可直接复制的 HTML，并把所有样式都写成内联样式，保证浏览器渲染后再粘贴进公众号后台时尽量稳定。

## 必需上下文

- 阅读 `../deep-biz-wechat-writer/references/style-layer.md`
- 阅读 `../deep-biz-wechat-writer/references/workflow-rubrics.md` 中的 `HTMLExport` 部分
- 优先使用最终成稿或 `FinalDraft`，不要用早期草稿

## 工作流

1. 阅读最终文章，保留其现有结构，而不是重写内容
2. 把文章转换为可复制的 HTML，而不是 Markdown
3. 把正文整体包在这个外层容器里：
   - `<section style="padding: 0 16px; font-size: 15px; color: #545454; line-height: 1.75; letter-spacing: 1px; word-break: break-all;">`
4. 正文段落用 `<p style="margin-bottom: 15px;">`
5. 一级小标题用 `<h1 style="font-size: 17px; color: #3daad6; margin-top: 30px; margin-bottom: 15px; font-weight: bold;">`
6. 二级小标题存在时，用 `<h2 style="font-size: 16px; color: #545454; margin-top: 25px; margin-bottom: 15px; font-weight: bold;">● 标题</h2>`
7. 如果原文已有图片，优先保留原图位置与资源
8. 如果原文没有可用图片数据，则在开头插入默认占位图；如果中间还有明显图位或视觉断点而原图不可读，也要在对应位置补占位图
9. 默认保留并输出原文里已经加粗的关键判断句；如果最终稿没有明显强调，但正文里存在特别重要的判断句，也可以在不改变结构的前提下少量补上 `<strong>` 或 `<b>`，让读者更容易扫到重点

## 输出规则

- 永远输出一个完整的 `HTMLExport`，包含：
  - `标题`
  - `正文 HTML`
  - `TypographySpec`
- `正文 HTML` 必须是直接可复制的 HTML，所有必要样式都写在标签内联样式中
- 除非用户明确要求，文章标题不要塞进正文 HTML 的 `<section>` 内
- 一级小标题用原文真实小标题，不要强行编号
- 如果原文没有二级小标题，就不要发明二级小标题
- 如果原文有二级小标题，则在 `<h2>` 文本前直接加 `● `
- 关键判断句和重要结论默认保留或补上少量加粗，但要克制，避免整篇都被强调撑满
- 如果原文已包含可用图片，必须优先保留原图，不要轻易替换成占位图
- 如果原文没有可用图片数据，至少在开头放一张默认占位图
- 不要在 `正文 HTML` 里混入说明文字、Markdown 包裹或样式解释

## 固定 TypographySpec

- 外层容器：`<section style="padding: 0 16px; font-size: 15px; color: #545454; line-height: 1.75; letter-spacing: 1px; word-break: break-all;">`
- 正文段落：`<p style="margin-bottom: 15px;">`
- 正文字体：15 号
- 正文字体颜色：`#545454`
- 一级小标题：17 号，`#3daad6`
- 一级小标题标签：`<h1 style="font-size: 17px; color: #3daad6; margin-top: 30px; margin-bottom: 15px; font-weight: bold;">`
- 二级小标题：16 号，标题前带 `●`
- 二级小标题标签：`<h2 style="font-size: 16px; color: #545454; margin-top: 25px; margin-bottom: 15px; font-weight: bold;">`
- 两端缩进：16
- 行间距：1.75
- 字间距：1
- 默认图片：`<img src="https://via.placeholder.com/800x400.png?text=Placeholder+Image" style="max-width: 100%; display: block; margin: 20px auto; border-radius: 8px;" />`
- 重点字句：优先用 `<strong>` 或 `<b>` 表示，保留文章的判断重心，但不要让加粗变成满屏装饰

## 图片优先级

1. 优先保留原文图片 URL
2. 如果原文只有可用的本地绝对路径图片，也直接插入
3. 如果原文没有可读取的图片数据，至少在开头插一张默认占位图
4. 如果正文存在明显图位、图说或视觉断点，但原图不可读，则在对应位置补默认占位图

## 重要限制

- Markdown 无法稳定承载这套严格的公众号内联样式，因此本 skill 默认输出 HTML
- 所有必须样式都应内联在 HTML 中，而不是留给用户手工二次调样
- 这个 skill 的价值在于稳定、可粘贴、适配公众号的 HTML 结构，而不是抽象的排版建议

## 失败模式

- 在文章正文 HTML 里混入说明性文字
- 标题层级标签使用不一致
- 原文没有二级小标题却硬加二级小标题
- 原文有可用图片却被错误丢弃
- 明显需要图位但又没有原图时，忘了补占位图
