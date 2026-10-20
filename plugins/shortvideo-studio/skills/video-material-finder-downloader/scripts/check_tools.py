#!/usr/bin/env python3
"""Report availability of video-download dependencies as JSON."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_tool(name: str) -> str | None:
    """Prefer a skill-bundled executable, then fall back to PATH."""
    bundled = Path(__file__).resolve().parent.parent / "bin" / name
    if bundled.is_file() and os.access(bundled, os.X_OK):
        return str(bundled)
    return shutil.which(name)


def python_runtime() -> str | None:
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
    return None


def version(command: list[str] | None, env: dict[str, str] | None = None) -> str | None:
    if not command:
        return None
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else None


def main() -> int:
    vendor = Path(__file__).resolve().parent.parent / "vendor"
    yt_dlp = str(vendor / "yt_dlp") if (vendor / "yt_dlp" / "__main__.py").is_file() else None
    ffmpeg = find_tool("ffmpeg")
    ffprobe = find_tool("ffprobe")
    node = find_tool("node")
    python = python_runtime()
    yt_env = os.environ.copy()
    if not yt_dlp and python:
        if version([python, "-m", "yt_dlp", "--version"]):
            yt_dlp = "yt_dlp (installed Python module)"
    if yt_dlp:
        yt_env["PYTHONPATH"] = str(vendor) + os.pathsep + yt_env.get("PYTHONPATH", "")
    report = {
        "ready": bool(yt_dlp and ffmpeg and ffprobe and node and python and version([python, "-m", "yt_dlp", "--version"], yt_env)),
        "yt_dlp": {"path": yt_dlp, "version": version([python, "-m", "yt_dlp", "--version"], yt_env) if python and yt_dlp else None},
        "ffmpeg": {"path": ffmpeg, "version": version([ffmpeg, "-version"]) if ffmpeg else None},
        "ffprobe": {"path": ffprobe, "version": version([ffprobe, "-version"]) if ffprobe else None},
        "python_runtime": {"path": python, "version": version([python, "--version"]) if python else None},
        "javascript_runtime": {"name": "node", "path": node, "version": version([node, "--version"]) if node else None},
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
