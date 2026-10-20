#!/usr/bin/env python3
"""Download selected network-platform, stock-footage, or direct HTTP media."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import ssl
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLATFORM_DOMAINS = {
    "youtube": {"youtube.com", "youtu.be"},
    "weibo": {"weibo.com", "weibo.cn"},
    "bilibili": {"bilibili.com", "b23.tv"},
    "douyin": {"douyin.com", "iesdouyin.com"},
    "xiaohongshu": {"xiaohongshu.com", "xhslink.com"},
    "x": {"x.com", "twitter.com"},
    "tiktok": {"tiktok.com"},
    "reddit": {"reddit.com", "redd.it"},
}
STOCK_DOMAINS = {
    "pexels": {"pexels.com"},
    "pixabay": {"pixabay.com"},
    "mixkit": {"mixkit.co"},
}
DEFAULT_MAX_BYTES = 2 * 1024 * 1024 * 1024
DEFAULT_BATCH_LIMIT = 12
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36"
CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


@dataclass
class Item:
    url: str
    name: str | None = None
    start: str | None = None
    end: str | None = None
    max_height: int = 1080


def safe_name(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\x00-\x1f]+", "-", value).strip(" .-")
    value = re.sub(r"\s+", " ", value)
    return value[:120] or "视频素材"


def require_chinese_name(value: str) -> str:
    name = safe_name(value)
    if not CJK_PATTERN.search(name):
        raise ValueError("Each download name must contain Chinese characters")
    return name


def parsed_http_url(value: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Only public HTTP(S) URLs are supported")
    return parsed


def source_platform(parsed: urllib.parse.ParseResult) -> str | None:
    host = (parsed.hostname or "").lower().rstrip(".")
    for platform, domains in PLATFORM_DOMAINS.items():
        if any(host == domain or host.endswith("." + domain) for domain in domains):
            return platform
    return None


def stock_site(parsed: urllib.parse.ParseResult) -> str | None:
    host = (parsed.hostname or "").lower().rstrip(".")
    for site, domains in STOCK_DOMAINS.items():
        if any(host == domain or host.endswith("." + domain) for domain in domains):
            return site
    return None


def pexels_download_url(url: str) -> str | None:
    parsed = parsed_http_url(url)
    if stock_site(parsed) != "pexels":
        return None
    match = re.search(r"/video/(?:[^/]*-)?(\d+)/?", parsed.path)
    if not match:
        return None
    return f"https://www.pexels.com/download/video/{match.group(1)}/"


def require_tool(name: str) -> str:
    bundled = Path(__file__).resolve().parent.parent / "bin" / name
    path = str(bundled) if bundled.is_file() and os.access(bundled, os.X_OK) else shutil.which(name)
    if not path:
        raise RuntimeError(f"Required tool not found: {name}")
    return path


def require_python_runtime() -> str:
    candidates = [
        Path(sys.executable),
        Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    ]
    candidates.extend(Path(path) for name in ("python3.13", "python3.12", "python3.11", "python3.10") if (path := shutil.which(name)))
    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            result = subprocess.run(
                [str(candidate), "-c", "import sys; raise SystemExit(sys.version_info < (3, 10))"],
                timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode == 0:
            return str(candidate)
    raise RuntimeError("Python 3.10+ runtime not found for the portable yt-dlp file")


def validate_range(start: str | None, end: str | None) -> None:
    if bool(start) != bool(end):
        raise ValueError("Both start and end are required for a time-range download")
    if not start:
        return
    pattern = re.compile(r"^(?:\d+(?::[0-5]?\d){0,2})(?:\.\d+)?$")
    if not pattern.fullmatch(start) or not pattern.fullmatch(end or ""):
        raise ValueError("Time values must be seconds, MM:SS, or HH:MM:SS")


def platform_download(item: Item, platform: str, output_dir: Path, max_bytes: int) -> dict[str, Any]:
    validate_range(item.start, item.end)
    python = require_python_runtime()
    vendor = Path(__file__).resolve().parent.parent / "vendor"
    has_vendor = (vendor / "yt_dlp" / "__main__.py").is_file()
    if not has_vendor:
        probe = subprocess.run([python, "-m", "yt_dlp", "--version"], capture_output=True, text=True)
        if probe.returncode != 0:
            raise RuntimeError("yt-dlp is not installed in this Python environment; install the declared optional download dependency")
    ffmpeg = require_tool("ffmpeg")
    require_tool("ffprobe")
    node = require_tool("node")
    result_file = output_dir / f".yt-dlp-result-{uuid.uuid4().hex}.txt"
    template = f"{require_chinese_name(item.name or '')}.%(ext)s"
    command = [
        python,
        "-m",
        "yt_dlp",
        "--no-playlist",
        "-t",
        "mp4",
        "-S",
        f"res:{item.max_height}",
        "--no-write-subs",
        "--no-write-auto-subs",
        "--js-runtimes",
        f"node:{node}",
        "--ffmpeg-location",
        str(Path(ffmpeg).parent),
        "--paths",
        str(output_dir),
        "--output",
        template,
        "--print-to-file",
        "after_move:filepath",
        str(result_file),
    ]
    if item.start and item.end:
        command.extend([
            "--download-sections",
            f"*{item.start}-{item.end}",
            "--force-keyframes-at-cuts",
        ])
    command.append(item.url)
    environment = os.environ.copy()
    if has_vendor:
        environment["PYTHONPATH"] = str(vendor) + os.pathsep + environment.get("PYTHONPATH", "")
    try:
        subprocess.run(command, check=True, env=environment)
        paths = [Path(line.strip()) for line in result_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    finally:
        result_file.unlink(missing_ok=True)
    if not paths:
        raise RuntimeError("yt-dlp completed without reporting an output filepath")
    path = paths[-1].resolve()
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"Downloaded file is missing or empty: {path}")
    if path.stat().st_size > max_bytes:
        path.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded file exceeds remaining size limit of {max_bytes} bytes")
    return result_record(item, path, "yt-dlp", platform)


def filename_from_response(response: Any, fallback_url: str) -> str:
    disposition = response.headers.get("Content-Disposition", "")
    match = re.search(r"filename\*?=(?:UTF-8''|\")?([^\";]+)", disposition, flags=re.I)
    if match:
        return urllib.parse.unquote(match.group(1)).strip()
    final_path = urllib.parse.urlparse(response.geturl()).path
    name = Path(urllib.parse.unquote(final_path)).name
    if name:
        return name
    source_path = urllib.parse.urlparse(fallback_url).path
    return Path(source_path).name or "视频素材.mp4"


def direct_download(item: Item, site: str | None, output_dir: Path, max_bytes: int) -> dict[str, Any]:
    source = pexels_download_url(item.url) if site == "pexels" else None
    source = source or item.url
    parsed_http_url(source)
    request = urllib.request.Request(source, headers={"User-Agent": USER_AGENT})
    response = None
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            response = urllib.request.urlopen(request, timeout=60)
            break
        except (urllib.error.URLError, TimeoutError, ConnectionError, ssl.SSLError) as exc:
            last_error = exc
            if attempt < 4:
                time.sleep(2 ** attempt)
    if response is None:
        raise RuntimeError(f"Download connection failed after retries: {last_error}")
    with response:
        content_type = response.headers.get_content_type()
        if content_type in {"text/html", "application/xhtml+xml"}:
            raise RuntimeError("URL returned a web page, not a media file; manual download link required")
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > max_bytes:
            raise RuntimeError(f"Remote file exceeds max size of {max_bytes} bytes")
        suggested = filename_from_response(response, source)
        suffix = Path(suggested).suffix
        if not suffix:
            suffix = mimetypes.guess_extension(content_type) or ".mp4"
        filename = f"{safe_name(item.name)}{suffix}" if item.name else safe_name(Path(suggested).stem) + suffix
        destination = (output_dir / filename).resolve()
        partial = destination.with_name(destination.name + ".part")
        written = 0
        try:
            with partial.open("wb") as handle:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    written += len(chunk)
                    if written > max_bytes:
                        raise RuntimeError(f"Download exceeded max size of {max_bytes} bytes")
                    handle.write(chunk)
            os.replace(partial, destination)
        except Exception:
            partial.unlink(missing_ok=True)
            raise
    if destination.stat().st_size == 0:
        destination.unlink(missing_ok=True)
        raise RuntimeError("Downloaded file is empty")
    return result_record(item, destination, "direct-http", site or "direct")


def result_record(item: Item, path: Path, method: str, platform: str) -> dict[str, Any]:
    probe = probe_video(path)
    return {
        "success": True,
        "source_url": item.url,
        "source_platform": platform,
        "method": method,
        "start": item.start,
        "end": item.end,
        "local_file": str(path),
        "size_bytes": path.stat().st_size,
        "duration_seconds": probe["duration_seconds"],
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
    }


def probe_video(path: Path) -> dict[str, float]:
    ffprobe = require_tool("ffprobe")
    command = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=codec_type:format=duration",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=60)
    data = json.loads(result.stdout)
    if not data.get("streams"):
        raise RuntimeError(f"Downloaded file has no video stream: {path}")
    try:
        duration = float(data["format"]["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Could not verify video duration: {path}") from exc
    if duration <= 0:
        raise RuntimeError(f"Downloaded video has invalid duration: {path}")
    return {"duration_seconds": round(duration, 3)}


def load_manifest(path: Path) -> list[Item]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("items") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError("Manifest must be an array or an object with an items array")
    items: list[Item] = []
    seen_names: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not row.get("url"):
            raise ValueError("Each manifest item must be an object with a url")
        if not row.get("name"):
            raise ValueError("Each manifest item must include a Chinese name")
        name = require_chinese_name(str(row["name"]))
        name_key = name.casefold()
        if name_key in seen_names:
            raise ValueError(f"Duplicate download name in manifest: {name}")
        seen_names.add(name_key)
        items.append(Item(
            url=str(row["url"]),
            name=name,
            start=str(row["start"]) if row.get("start") is not None else None,
            end=str(row["end"]) if row.get("end") is not None else None,
            max_height=int(row.get("max_height", 1080)),
        ))
    return items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url")
    source.add_argument("--manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--name")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--max-height", type=int, default=1080)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--batch-limit", type=int, default=DEFAULT_BATCH_LIMIT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    if args.manifest:
        items = load_manifest(args.manifest.expanduser().resolve())
    else:
        if not args.name:
            raise ValueError("--name is required and must contain Chinese characters")
        items = [Item(args.url, require_chinese_name(args.name), args.start, args.end, args.max_height)]
    if len(items) > args.batch_limit:
        raise ValueError(f"Manifest contains {len(items)} items; limit is {args.batch_limit}")
    results: list[dict[str, Any]] = []
    remaining_bytes = args.max_bytes
    for item in items:
        if remaining_bytes <= 0:
            results.append({"success": False, "source_url": item.url, "error": "Batch size limit has been reached"})
            continue
        parsed = parsed_http_url(item.url)
        try:
            platform = source_platform(parsed)
            site = stock_site(parsed)
            if platform:
                result = platform_download(item, platform, output_dir, remaining_bytes)
            else:
                if item.start or item.end:
                    raise ValueError("Time-range download is supported only for recognized public-platform URLs")
                result = direct_download(item, site, output_dir, remaining_bytes)
            results.append(result)
            remaining_bytes -= int(result["size_bytes"])
        except Exception as exc:
            results.append({"success": False, "source_url": item.url, "error": str(exc)})
    payload = {"output_dir": str(output_dir), "results": results}
    print("\nDOWNLOAD_RESULT_JSON")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if all(result.get("success") for result in results) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
