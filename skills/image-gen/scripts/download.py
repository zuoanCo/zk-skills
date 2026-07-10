#!/usr/bin/env python3
"""download.py — stream-download an image URL to disk.

Examples:
  python3 download.py --url https://example.com/x.png --out /tmp/x.png
  python3 download.py --url ... --out /tmp/x.png --force   # re-download
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _common import emit_json, emit_error  # noqa: E402
from client import build_client_from_env  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="download.py", description="Stream-download an image URL.")
    p.add_argument("--url", required=True, help="image URL")
    p.add_argument("--out", required=True, help="destination path")
    p.add_argument("--force", action="store_true", help="re-download even if cached")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    client = build_client_from_env()
    try:
        path = client.download(args.url, args.out, force=args.force)
    except Exception as e:
        emit_error(f"download failed: {e.__class__.__name__}: {e}")
    emit_json({"ok": True, "url": args.url, "path": str(path)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())