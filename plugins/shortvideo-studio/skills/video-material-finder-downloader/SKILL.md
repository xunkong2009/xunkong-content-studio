---
name: video-material-finder-downloader
description: Find, evaluate, and download free-source editable video material for talking-head scripts or topic videos. Use when the user provides a script and wants source routing across Chinese or global social platforms, official media centers, free stock libraries, or open archives; exact source links; selected public clips or time ranges downloaded; Chinese local filenames; and a source manifest. Exclude every paid library, paid license, and paid asset. Do not use for importing media into ChatCut or another editor.
---

## 分享版个人配置

用户当轮提供的材料和要求优先。需要语料库、主播照片或本地字体时，可读取当前项目的 `.xunkong-studio/config.json`（如存在）；相对文件路径以当前项目为基准。配置示例见插件根目录 `config.example.json`，不要改写安装目录。

未配置语料库时使用随包风格规则继续写作；未配置真人参考照片时可先交付提示词或无人像方案。需要复现某个真人且缺少参考时，向当前用户索取参考，不使用发布者的身份。配置文件中不存储 API Key、密码或账号 Cookie。

# Video Material Finder Downloader

Turn a script into a bounded, source-labeled footage package. Search first, download only when requested, and return absolute clickable file links in the final response.

## Plugin handoff

When called by `shortvideo-workbench` with a `VisualBeatPlan`, process only `network-footage`, `stock-footage`, and the real-footage portion of `mixed` beats. Do not split the full script again. Preserve each supplied `beat_id` in shortlist rows, manifest entries, and filenames such as `B03-年轻员工核对AI报告.mp4`. All source verification, rights labeling, download limits, and delivery-mode rules below remain mandatory.

## Choose the delivery mode

- **Links only:** Return exact source or download-page links. Do not download files.
- **Review first:** Return a numbered shortlist, then download the user's selections.
- **Search and download:** Select a bounded set, download it during the current task, and return clickable files.

Treat phrases such as “直接下载”, “给我可点击文件”, and “找好并下载” as authorization to download the selected assets. Treat “找素材” alone as links-only unless the surrounding request clearly asks for files.

## Local filename policy

- Name every downloaded local video file in Chinese. Keep a beat or sequence prefix when useful, for example `B03-年轻员工核对AI报告.mp4` or `03-老板追加任务.mp4`.
- Require the descriptive portion of every filename to contain Chinese characters. Do not use English slugs such as `ai-work-pressure.mp4` for downloaded deliverables.
- Pass an explicit, unique Chinese `name` for every CLI or manifest download. The downloader rejects missing names, names without Chinese characters, and duplicate names within one manifest.
- Keep the source's original-language title in `materials.json` or `materials.md`; do not reuse it as the local filename.
- Use the same Chinese filename in ready-to-edit outputs, source manifests, ZIP packages, and final clickable links. A transcoding suffix such as `-1080p` may be retained only when operationally necessary.

## Workflow

1. **Break the script into visual beats.** Estimate spoken duration and identify hook, evidence, named people or organizations, mechanisms, examples, and closing. Prefer 3–8 second inserts. Reuse different moments from a longer source when appropriate.
2. **Route and search exact sources.**
   - Read [references/platform-search.md](references/platform-search.md). Classify each beat before searching, then query only the source classes suited to its visual job. Do not search every supported site mechanically.
   - Available source classes include Chinese social video, global social video, official websites and media centers, free stock footage, and historical/open archives. Do not search paid news, paid UGC, subscription, or paid stock sources.
   - For named people, organizations, events, and products, prefer original uploads and official accounts from institutions, companies, universities, conferences, media organizations, and named creators.
   - Exclude third-party product reviews, taste tests, unboxings, reactions, commentary channels, consumer street interviews, and influencer evaluations. Do not shortlist them even when they contain relevant product shots.
   - When official footage is unavailable, use UGC with direct no-fee written permission, free licensed stock, openly licensed footage, or an existing generated visual. If permission requires payment, skip it. Do not fill the gap with a reviewer video.
   - For generic B-roll, prefer relevant free stock footage with clear commercial-use terms and clean visuals.
   - Return exact video, post, or stock-detail pages, never search-result pages.
   - Use current web, browser, or available platform-search tools. Verify title, uploader, publish date, relevance, likely overlays or burned-in subtitles, and rights signals.
3. **Label rights and practical risks.** Read [references/source-policy.md](references/source-policy.md). Distinguish free stock footage, original or official footage, direct creator permission, open archives, academic talks, creator uploads, and reposts.
4. **Build a shortlist.** For each candidate record the script beat, visual job, source class, title, source URL, uploader, suggested time range, orientation, subtitle/overlay note, rights note, delivery status, and a unique Chinese local filename. Use one delivery status: `automatic-download`, `official-download`, `manual-login`, or `link-only-awaiting-free-permission`.
5. **Bound the download.** Default to no more than 12 unique files or 2 GB per run. For social and network platforms, download only the recommended 3–15 second ranges unless the user explicitly requests full videos. Stock clips may be downloaded in full. Ask before exceeding either bound.
6. **Create an output folder.** Use `<workspace>/output/video-materials/<topic>-<YYYYMMDD-HHMMSS>/`. Never place downloads in the skill directory.
7. **Check dependencies.** Run:

   ```bash
   python3 <skill-dir>/scripts/check_tools.py
   ```

   Require `yt-dlp`, `ffmpeg`, and `ffprobe` for supported public-platform or time-range downloads. Require a supported JavaScript runtime for current platform support. Prefer Node.js when available and pass it explicitly to yt-dlp. If missing, request approval to install official/current builds. Do not create a server, daemon, browser extension, or resident local application.
   See [references/tool-sources.md](references/tool-sources.md) for the installed component sources.
8. **Download selected files.** Run the downloader once per asset or pass a manifest:

   ```bash
   python3 <skill-dir>/scripts/download_media.py \
     --url "https://www.youtube.com/watch?v=..." \
     --start "00:01:20" --end "00:01:28" \
     --name "01-AI助手生成方案" \
     --output-dir "/absolute/workspace/output/video-materials/topic"
   ```

   ```bash
   python3 <skill-dir>/scripts/download_media.py \
     --manifest "/absolute/path/materials.json" \
     --output-dir "/absolute/workspace/output/video-materials/topic"
   ```

9. **Verify outputs.** Confirm every reported file exists and is non-empty. For video, use `ffprobe` to check duration and at least one video stream. Confirm that a requested time-range is approximately correct. Do not claim that optional subtitles were removed when text is burned into the source image.
10. **Deliver clickable files.** Use absolute Markdown file links, grouped by script beat. Also provide `materials.json` or `materials.md` when created. Keep the original source URL beside each file.

## Download rules

- Give every downloaded local video a unique Chinese filename. Do not allow the source title or an English slug to become the delivered filename.
- Never download or deliver third-party review, taste-test, reaction, unboxing, commentary, or influencer-evaluation videos as script footage.
- Do not use `yt-dlp -g` or expose transient platform/CDN URLs as deliverables. Resolve and download during the task.
- Use MP4 up to 1080p by default. Do not request or embed separate subtitles unless the user asks.
- Preserve audio unless the user asks for silent B-roll.
- Do not use browser cookies or authenticated/private videos unless the user explicitly authorizes the exact account-bound source.
- Do not bypass paywalls, DRM, age verification, private access, geographic restrictions, or platform safety controls.
- Skip any source that requires payment, credits, a subscription, or a paid license. For account-bound free platforms and media centers, use the user's signed-in session only when explicitly authorized; never bypass access controls.
- Do not imply that public availability grants reuse rights. Download only material the user is entitled to download and reuse.
- Keep a source manifest with original URL, title, uploader when available, selected time range, download time, local filename, and rights note.

## Manifest format

Use a JSON array or an object with an `items` array:

```json
{
  "items": [
    {
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "name": "01-AI代理主题演讲",
      "start": "00:01:20",
      "end": "00:01:28",
      "max_height": 1080
    },
    {
      "url": "https://www.bilibili.com/video/BVxxxxxxxxxx/",
      "name": "02-实验室研究画面",
      "start": "00:00:30",
      "end": "00:00:38"
    },
    {
      "url": "https://weibo.com/tv/show/EXAMPLE",
      "name": "03-新闻现场画面",
      "start": "00:00:05",
      "end": "00:00:12"
    },
    {
      "url": "https://www.pexels.com/video/example-123456/",
      "name": "04-程序员办公画面"
    }
  ]
}
```

## Final response

Lead with the completed package and download location. For every file provide:

- script beat or intended use;
- clickable absolute MP4 link with the Chinese filename visible;
- original source link;
- downloaded range or “full clip”;
- concise rights/subtitle note.

If a source failed, retain the shortlist entry, mark the failure precisely, and provide the closest verified alternative instead of inventing a file link.
