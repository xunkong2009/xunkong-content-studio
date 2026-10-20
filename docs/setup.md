# 安装与配置

## 基础写作

登录支持插件的 Codex 桌面端或 CLI，添加本私有 marketplace，再安装需要的插件。写选题、正文、审校和提示词无需配置 IMA 或视频环境；当前新闻核验需要可用的联网搜索能力。

## 个人配置

在要进行创作的项目中新建 `.xunkong-studio/config.json`，从插件根目录 `config.example.json` 复制字段。文件只描述用户自己的语料位置与资源，不填写密钥。各插件能共用一份项目配置，用户当轮明确提供的材料优先。

`corpus.provider` 支持 `none`（默认）、`ima`、`local`。使用 `local` 时填 `local_sample_dir` 并授权读取。使用 `ima` 时安装官方 IMA Skill，填其目录 `ima_skill_dir`、自己的 `knowledge_base_name`，以及文章、约稿或脚本目录的名称数组。

例如自己的知识库根目录下有“我的文章/已发布”，则 `article_folder_path` 填 `["我的文章", "已发布"]`。脚本目录可包含年度和月份，插件按请求选取代表样本，不下载或迁移整个私人资料库。

IMA 官方入口：https://ima.qq.com/agent-interface 。按官方 Skill 指引在本机配置自己的 Client ID 和 API Key。不要提交本机凭证文件、环境变量值或 Cookie。

`presenter.reference_images` 填自己可读取的本地参考图片路径；如使用 Drive，填自己已授权的文件夹 `drive_folder_url`。`cover_style_references` 可填写自己提供的封面风格参考。没有提供参考时不会默认套用发布者的脸。

## 媒体制作依赖

| 功能 | 所需环境 |
| --- | --- |
| 配图与封面成图 | 当前客户端的图片生成能力 |
| Remotion 动效 | Node.js / npm、模板 package.json 所列依赖、渲染所需浏览器和 FFprobe |
| 视频下载 | Python 3.10+、同环境的 `yt-dlp[default]`、FFmpeg、FFprobe、Node.js |
| 口播剪辑 | Python 3.10+、FFmpeg / FFprobe |
| 转写 | 同环境的 faster-whisper，以及当前用户选择的本地模型 |
| 字幕与字体检查 | Pillow、fonttools，以及用户有权使用的本机字体 |

依赖由用户在自己的环境按需安装。下载工具可先运行插件内 `scripts/check_tools.py`；Remotion 先把模板复制到当前项目，再按 lockfile 运行 `npm ci`，不在插件安装目录生成项目或缓存。FFmpeg / FFprobe 加入 PATH；剪辑脚本也接受 `--ffmpeg`、`--ffprobe` 或 FFMPEG、FFPROBE 环境变量，配置文件的 media 字段可供代理解析后传参。

官方来源：Python https://www.python.org/ 、Node.js https://nodejs.org/ 、FFmpeg https://ffmpeg.org/download.html 、yt-dlp https://github.com/yt-dlp/yt-dlp 。不安装服务、守护进程或浏览器扩展。

## 共享访问

仓库是私有的。接收者必须接受所有者的 GitHub collaborator 邀请，且使用有读取权限的账号访问。仓库链接本身不授予权限。所有者在 GitHub Settings → Collaborators 中选择具体成员；本次上传不自动邀请任何人。
