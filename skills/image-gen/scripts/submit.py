#!/usr/bin/env python3
"""submit.py — submit an image generation task.

Two modes:
  --sync   (default) Block until response. Returns image URLs / b64 directly.
  --async           Return immediately with a task_id. Use poll.py to fetch.

Examples:
  python3 submit.py --prompt "a cat in space" --size 1024x1024
  python3 submit.py --prompt "..." --async --model gpt-image-2-vip --size 3840x2160
  python3 submit.py --prompt "..." --dry-run    # don't actually call
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `from providers...` and `from client...` regardless of CWD
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _common import emit_json, emit_error, load_provider  # noqa: E402
from client import build_client_from_env  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="submit.py",
        description="Submit an image generation task to the configured provider.",
    )
    p.add_argument("--prompt", required=True, help="text prompt for image generation")
    p.add_argument("--model", default=None, help="model name (default: provider default, e.g. gpt-image-2)")
    p.add_argument("--size", default="1024x1024",
                   help="WxH such as 1024x1024, 1536x1024, 1920x1080 (default: 1024x1024)")
    p.add_argument("--n", type=int, default=1, help="number of images (default: 1)")
    p.add_argument("--quality", default=None, help="optional quality field (auto|low|medium|high)")
    p.add_argument("--response-format", default="url", choices=["url", "b64_json"],
                   help="how the result image data should be returned (default: url)")
    p.add_argument("--reference-image", action="append", default=[],
                   metavar="URL",
                   help="reference image URL (repeatable). Note: async mode requires public http(s) URLs.")
    p.add_argument("--provider", default="geeknow", help="provider name (default: geeknow)")
    p.add_argument("--api-key", default=None, help="override API key (otherwise env/config)")
    p.add_argument("--base-url", default=None, help="override provider base URL")
    p.add_argument("--async", dest="async_mode", action="store_true",
                   help="submit asynchronously and return task_id without blocking for result")
    p.add_argument("--dry-run", action="store_true",
                   help="print the request descriptor without making the call")
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
            hint="set IMAGE_GEN_API_KEY (or GEEKKNOW_API_KEY) env var, "
                 "or write ~/.claude/skills/image-gen/config.json, "
                 "or pass --api-key.",
        )

    kwargs = dict(
        model=args.model,
        prompt=args.prompt,
        n=args.n,
        size=args.size,
        response_format=args.response_format,
        quality=args.quality,
        image=args.reference_image or None,
    )

    if args.async_mode:
        descriptor = provider.submit_async(**kwargs)
    else:
        descriptor = provider.submit_sync(**kwargs)

    if args.dry_run:
        emit_json({
            "ok": True,
            "dry_run": True,
            "provider": provider.name,
            "endpoint": descriptor["url"],
            "method": descriptor["method"],
            "request": descriptor.get("body"),
            "mode": "async" if args.async_mode else "sync",
        })
        return 0

    client = build_client_from_env()

    def _retry(attempt: int, sleep: float, reason: str) -> None:
        sys.stderr.write(f"[retry] attempt={attempt} sleep={sleep:.1f}s reason={reason}\n")

    try:
        resp = client.execute(descriptor)
    except Exception as e:
        emit_error(f"transport error: {e.__class__.__name__}: {e}")

    if resp.status_code >= 400:
        emit_error(
            f"HTTP {resp.status_code} from {provider.name}",
            hint=resp.text[:600],
        )

    try:
        raw = resp.json()
    except ValueError:
        emit_error(f"non-JSON response: HTTP {resp.status_code}", hint=resp.text[:600])

    if args.async_mode:
        normalized = provider.normalize_async_submit(raw)
        emit_json({
            "ok": True,
            "provider": provider.name,
            "mode": "async",
            "task_id": normalized["task_id"],
            "poll_url": descriptor["url"].rsplit("/async", 1)[0] + f"/async/{normalized['task_id']}",
            "raw": raw,
        })
    else:
        normalized = provider.normalize_sync(raw)
        emit_json({
            "ok": True,
            "provider": provider.name,
            "mode": "sync",
            "created": normalized["created"],
            "model": normalized.get("model"),
            "items": normalized["items"],
        })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())