# WeChat Typography

Use this file as the fixed formatting spec for all HTML exports intended for WeChat backend publishing.

## TypographySpec

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

## Image Priority

- 优先保留原文图片 URL
- 如原文只有本地绝对路径图片，可直接写入 `<img src="...">`
- 如原文无可读取图片数据，至少在开头插入一张默认占位图
- 如正文存在明显配图位置但原图不可用，则在对应位置补默认占位图

## HTML Mapping

- Outer wrapper -> `<section ...>`
- First-level subheads -> `<h1 ...>标题</h1>`
- Second-level subheads when present -> `<h2 ...>● 标题</h2>`
- Body paragraphs -> `<p style="margin-bottom: 15px;">正文</p>`
- Image slot -> source image `<img ... />`, fallback to placeholder `<img ... />`

## Notes

- Do not add explanatory notes into the body HTML.
- If no second-level subheads exist in the article, skip them entirely.
- The exported HTML should be ready for browser rendering and then copy-paste into WeChat.
