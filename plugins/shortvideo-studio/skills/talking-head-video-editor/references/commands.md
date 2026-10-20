# 程序接口

所有路径参数使用绝对路径最稳妥。命令示例中的路径是占位值，先替换。输出必须不存在；程序不覆盖已有文件。核心 editor.py 只需 Python 标准库和 FFmpeg/FFprobe，`captions` 另需 Pillow、fonttools。

```bash
python scripts/editor.py --ffmpeg /path/ffmpeg --ffprobe /path/ffprobe probe /path/video.mp4
python scripts/transcribe.py /path/video.mp4 /path/transcript.json --model /path/local-whisper-model --prompt '品牌名，专有名词'
python scripts/editor.py rough /path/rough-plan.json /path/rough-v1.mp4
python scripts/editor.py compose /path/material-plan.json /path/final-v1.mp4
python scripts/editor.py captions /path/final-v1.mp4 /path/cues.json /path/subtitled-v1.mp4 --font /path/AlibabaPuHuiTi.ttf --size 56 --layout /path/caption-layout.json
python scripts/editor.py verify /path/subtitled-v1.mp4 --audio-base /path/final-v1.mp4 --frames 600 --report /path/check.json
```

全局 `--encoder h264_videotoolbox` 可选，默认 libx264。全局参数放子命令前。verify 完整解码，报告黑帧/静音候选供人工判断，不自动删除；全黑背景可能是素材本身。

## rough-plan.json

```json
{"source":"/absolute/raw.mp4","fps":30,"width":1080,"height":1920,"keep":[{"in":1.2,"out":4.8,"reason":"完整开头"},{"in":7.1,"out":10.4,"reason":"重录后完整一遍"}]}
```

时间为原片秒数、升序、不重叠。fps 使用整数，按实际需要选 25/30/50/60；不是盲目把所有素材升到 60。输出 `.timeline.json` 为实际量化帧数及源/成片映射。声音仅粗剪阶段编码一次，分段中间文件使用 PCM，避免逐段 AAC 编码产生缝隙。

## material-plan.json

```json
{"base":"/absolute/confirmed-rough.mp4","fps":30,"width":1080,"height":1920,"inserts":[{"start":2.0,"end":4.0,"file":"/absolute/image.png","kind":"image","reason":"说明当前观点"},{"start":5.0,"end":8.0,"file":"/absolute/motion.mp4","kind":"video","source_in":1.0,"source_span":3.0,"reason":"同主题优先动效"}]}
```

start/end 为基准成片秒数，升序不重叠。基准必须已经是相同整数 CFR；不满足时停止，先明确规范化后的新基准。source_span 可省略，默认与覆盖时长一致。source_span 与覆盖时长不同表示明确变速。程序自动补全主播片段，完整容纳素材、黑边填充，排除素材声音。

## cues.json

```json
[{"start":0.3,"end":2.1,"text":"第一句字幕"},{"start":2.2,"end":4.5,"text":"第二句字幕"}]
```

输入需完成语义与同步校对，程序不会用脚本凭空生成时间。字幕可含换行，每行须通过字体宽度检查；拒绝 ASS 控制字符注入。输出同名 `.srt`、`.ass`、`.render.log` 和 MP4。程序自动识别字体内部名称并检查 glyph；实际 fontselect 与画面仍需审查。

## 剪口审听包

```bash
python scripts/review_cuts.py /path/rough-v1.timeline.json /path/rough-v1.mp4 /path/review-v1 --ffmpeg /path/ffmpeg --context 3
python scripts/transcribe.py /path/review-v1/001-source-left.wav /path/left-transcript.json --model /path/local-whisper-model --no-vad
python scripts/transcribe.py /path/review-v1/001-source-right.wav /path/right-transcript.json --model /path/local-whisper-model --no-vad
```

使用 rough 命令生成的实际 `.timeline.json`，不是手写 keep 计划。每个连接点输出原片左段、原片右段、实际导出声音三个 WAV，以及 `review.json` 待审清单。目录必须不存在。源片段默认各取最多 3 秒，并限制在对应保留片段中；不足以判断完整短语时增大 context 或单独扩展原片范围。两个原片 WAV 分别转写，不能先拼接再识别，否则 ASR 仍可能吞掉重复。

局部转写时间从零开始，须加清单对应 start 才能映射回原片/成片；视频提取音频还须留意音轨起始偏移。审听包只生成证据，不自动判定通过；检查后如实填写停顿类型、词句、去重结果和听审状态。原片整段内部的遗漏也要检查，不能只审已有剪口。

## 测试

`tests/smoke.py --ffmpeg /path/ffmpeg --ffprobe /path/ffprobe --font /path/font.ttf` 创建临时合成媒体，验证粗剪帧数、素材拼接、字幕、声音一致、不覆盖和拒绝重叠时间轴。不使用用户视频，不是实际项目听审的替代品。

## overlays 与 sfx（material-plan 的可选扩展）

```json
{
  "base":"/absolute/confirmed-rough.mp4", "base_sha256":"<actual-sha256>",
  "fps":30,"width":1080,"height":1920,"inserts":[],
  "face_regions":[{"x":330,"y":180,"width":420,"height":600}],
  "overlays":[{
    "beat_id":"B02","template_id":"callout","start":2,"end":7,
    "file":"/absolute/02-callout.mov","kind":"video","source_in":0,
    "x":0,"y":0,"width":1080,"height":1920,
    "content_regions":[{"x":580,"y":900,"width":420,"height":650}]
  }],
  "sfx":[{"beat_id":"B02","start":2,"end":7,"file":"/absolute/02-callout.sfx.wav","source_in":0,"gain":1}]
}
```

base_sha256 为基准文件 SHA256，提供时程序验证。overlays 与 inserts 可并存；overlays 数组顺序决定叠加层级，可在时间上重叠。所有秒数使用同一粗剪坐标，浮层无隐式循环或变速。PNG/MOV/WebM 必须有 alpha，全屏 MP4 用 inserts。

face_regions 包含全段头部移动余量，content_regions 为实际可见内容、入场路径和阴影的包围区域，均为最终画布像素。省略 content_regions 时以 placement 矩形检查；不允许与保护脸部区域相交。肩手不是禁区。矩形检查仅验证声明，不能证明实际资产避脸，仍须抽查合成画面。

sfx只接受显式声音事件，gain为正的有限数，可单独放大低电平stem；保持人声源、时标和增益1不变。程序预检浮点线性混音峰值并检查输出AAC峰值，余量不足时拒绝交付，调整音效而非主轨限幅。无 sfx 整轨复制，有 sfx 则报告基准音轨哈希和参数，不用整轨哈希判断新混音。保存 .timeline.json 中 overlays/sfx/mix 记录，字幕以最终采用混音为准。不要同时保留动效内声音再叠加同一 stem。

## 分时字幕位置与动效避让

`captions --layout /path/caption-layout.json`为可选扩展，旧的`--margin-v`仍可用；未给margin时以胸前偏下高度为起点，默认字号56。所有位置在当前画布中测量。布局示意（不代表固定项目时间点）：

```json
{
  "fps": 30,
  "default_position": [540, 1530],
  "position_windows": [
    {"start_frame": 210, "end_frame": 510, "position": [540, 1750]}
  ],
  "suppress_windows": [
    {"start_frame": 1710, "end_frame": 1860, "beat_id": "B08"}
  ]
}
```

start/end秒数或整数start_frame/end_frame二选一，统一源视频坐标和帧率，使用半开区间。隐藏窗口相交部分被精确减去，原文字不变；少于约0.4秒的残片写入复核报告，不静默删除。位置窗口应用于整条保留短句，避免短句中途跳位；冲突位置需先按语义拆句。单条cue可附`position:[x,y]`覆盖布局位置；坐标是居中底部ASS锚点，需检查实际字形。程序检查行宽及画布边界，不自动证明避脸或避开素材文字。

额外输出`.caption-layout.json`保存实际可见cues、隐藏索引和复核项；SRT与ASS均对应可见字幕。ASS按帧边界取合适的厘秒落点，避免四舍五入使隐藏窗口多露一帧。字体使用内部PostScript名、绝对fontsdir；渲染发现缺字即报错，不能静默回退。

`tests/caption_layout_smoke.py`验证帧窗口差集、整句位置、异常输入、实际字幕出入帧、位置和音轨一致性，以及音效独立放大与削波拒绝。它使用临时合成媒体，不读取用户视频，不代替项目听审。
