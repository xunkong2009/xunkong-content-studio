# 分享版依赖来源

不随包分发平台专用 FFmpeg、Python 扩展、账号 Cookie 或运行时缓存。搜索和返回素材链接不依赖以下下载组件。

- Python 3.10+：使用当前安装者的 Python 环境。
- yt-dlp：在同一个 Python 环境中从 PyPI 安装 `yt-dlp[default]`。项目 https://github.com/yt-dlp/yt-dlp 。
- FFmpeg / FFprobe：由安装者从 https://ffmpeg.org/download.html 获取适合本机平台的程序，并加入 PATH。
- Node.js：使用官方 https://nodejs.org 的受支持版本并加入 PATH；Remotion 工程按自带 package-lock 安装。

用 `scripts/check_tools.py` 检查实际环境。缺少工具时明确提示缺失项，按用户授权安装，不假装已经下载或制作成功。
