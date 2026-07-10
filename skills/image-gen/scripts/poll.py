#!/usr/bin/env python3
"""poll.py — poll the status of an async image generation task.

Examples:
  python3 poll.py --task-id task_img_abc123
  python3 poll.py --task-id ... --wait   # poll until success/failed
  python3 poll.py --task-id ... --wait --timeout 300
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _common import emit_json, emit_error, load_provider  # noqa: E402
from client import build_client_from_env  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="poll.py", description="Poll an async image task.")
    p.add_argument("--task-id", required=True, help="task ID returned by submit.py --async")
    p.add_argument("--provider", default="geeknow", help="provider name (default: geeknow)")
    p.add_argument("--api-key", default=None, help="override API key")
    p.add_argument("--base-url", default=None, help="override provider base URL")
    p.add_argument("--wait", action="store_true",
                   help="block and poll until status is success / failed")
    p.add_argument("--interval", type=float, default=3.0,
                   help="seconds between polls in --wait mode (default: 3)")
    p.add_argument("--timeout", type=float, default=600.0,
                   help="max wait seconds in --wait mode (default: 600)")
    p.add_argument("--dry-run", action="store_true", help="print request descriptor only")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        provider = load_provider(args.provider, api_key=args.api_key, base_url=args.base_url)
    except ValueError as e:
        emit_error(str(e))
    if not provider.api_key:
        emit_error(
            f"missing API key for provider '{args.provider}'",
            hint="set IMAGE_GEN_API_KEY or pass --api-key.",
        )

    descriptor = provider.poll_async(args.task_id)

    if args.dry_run:
        emit_json({"ok": True, "dry_run": True, "request": descriptor})
        return 0

    client = build_client_from_env()
    deadline = time.monotonic() + args.timeout

    while True:
        try:
            resp = client.execute(descriptor)
        except Exception as e:
            emit_error(f"transport error: {e.__class__.__name__}: {e}")
        if resp.status_code >= 400:
            emit_error(f"HTTP {resp.status_code}", hint=resp.text[:600])
        try:
            raw = resp.json()
        except ValueError:
            emit_error(f"non-JSON response: HTTP {resp.status_code}", hint=resp.text[:600])

        normalized = provider.normalize_async_poll(raw)
        normalized["ok"] = True

        if not args.wait or normalized["status"] in {"success", "failed"}:
            emit_json(normalized)
            return 0 if normalized["status"] == "success" else 2

        # --wait: continue, but emit a progress line to stderr
        sys.stderr.write(
            f"[poll] task_id={args.task_id} status={normalized['status']} "
            f"progress={normalized.get('progress') or '?'}\n"
        )
        if time.monotonic() >= deadline:
            emit_error(f"timed out after {args.timeout}s waiting for {args.task_id}")
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())