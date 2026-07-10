#!/usr/bin/env python3
"""batch.py — submit N image tasks in parallel.

Each prompt on its own line in the input file. Tasks are submitted
concurrently via a ThreadPoolExecutor; the main thread never blocks on
network IO longer than the slowest single submission.

Examples:
  python3 batch.py --prompts-file prompts.txt --parallel 4
  python3 batch.py --prompts-file prompts.txt --parallel 4 --async
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _common import emit_json, emit_error, load_provider  # noqa: E402
from client import build_client_from_env  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="batch.py", description="Batch-submit image tasks.")
    p.add_argument("--prompts-file", required=True,
                   help="path to a text file, one prompt per line. Lines starting with # are skipped.")
    p.add_argument("--parallel", type=int, default=4, help="concurrent workers (default: 4)")
    p.add_argument("--model", default=None, help="model name (default: provider default)")
    p.add_argument("--size", default="1024x1024", help="image size (default: 1024x1024)")
    p.add_argument("--n", type=int, default=1, help="images per prompt (default: 1)")
    p.add_argument("--response-format", default="url", choices=["url", "b64_json"])
    p.add_argument("--provider", default="geeknow", help="provider name (default: geeknow)")
    p.add_argument("--api-key", default=None, help="override API key")
    p.add_argument("--base-url", default=None, help="override provider base URL")
    p.add_argument("--async", dest="async_mode", action="store_true",
                   help="use async submission; output is a list of task_ids")
    p.add_argument("--dry-run", action="store_true", help="don't actually call")
    return p.parse_args()


def read_prompts(path: Path) -> list[str]:
    out: list[str] = []
    for raw in path.read_text().splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        out.append(stripped)
    return out


def submit_one(idx: int, prompt: str, args, provider, client) -> dict:
    """Submit a single prompt. Returns a result dict (caller-facing)."""
    kwargs = dict(
        model=args.model,
        prompt=prompt,
        n=args.n,
        size=args.size,
        response_format=args.response_format,
    )
    descriptor = (
        provider.submit_async(**kwargs) if args.async_mode
        else provider.submit_sync(**kwargs)
    )
    if args.dry_run:
        return {
            "index": idx,
            "ok": True,
            "dry_run": True,
            "endpoint": descriptor["url"],
            "method": descriptor["method"],
            "request": descriptor.get("body"),
        }
    try:
        resp = client.execute(descriptor)
    except Exception as e:
        return {"index": idx, "ok": False, "prompt": prompt, "error": f"{e.__class__.__name__}: {e}"}
    if resp.status_code >= 400:
        return {
            "index": idx,
            "ok": False,
            "prompt": prompt,
            "http_status": resp.status_code,
            "error": resp.text[:300],
        }
    try:
        raw = resp.json()
    except ValueError:
        return {"index": idx, "ok": False, "prompt": prompt, "error": "non-JSON response"}
    if args.async_mode:
        n = provider.normalize_async_submit(raw)
        return {"index": idx, "ok": True, "mode": "async", "task_id": n["task_id"]}
    n = provider.normalize_sync(raw)
    return {"index": idx, "ok": True, "mode": "sync", "items": n["items"]}


def main() -> int:
    args = parse_args()

    try:
        provider = load_provider(args.provider, api_key=args.api_key, base_url=args.base_url)
    except ValueError as e:
        emit_error(str(e))
    if not provider.api_key:
        emit_error(f"missing API key for provider '{args.provider}'",
                   hint="set IMAGE_GEN_API_KEY or pass --api-key.")

    prompts = read_prompts(Path(args.prompts_file).expanduser())
    if not prompts:
        emit_error(f"no prompts found in {args.prompts_file}")

    client = build_client_from_env()
    started = time.monotonic()
    results: list[dict] = []
    failures = 0

    # Main thread just dispatches. Each worker submits independently; the
    # shared Session in `client` is thread-safe thanks to requests' connection
    # pooling. We deliberately do NOT serialize work — that would defeat the
    # point of "non-blocking main thread".
    with ThreadPoolExecutor(max_workers=max(1, args.parallel)) as pool:
        futures = {
            pool.submit(submit_one, i, p, args, provider, client): i
            for i, p in enumerate(prompts)
        }
        for fut in as_completed(futures):
            r = fut.result()
            results.append(r)
            if not r.get("ok"):
                failures += 1
            sys.stderr.write(
                f"[batch] {len(results)}/{len(prompts)} "
                f"task_idx={r['index']} ok={r['ok']} "
                f"{'task_id=' + r['task_id'] if 'task_id' in r else ''}\n"
            )

    results.sort(key=lambda r: r["index"])
    emit_json({
        "ok": failures == 0,
        "provider": provider.name,
        "mode": "async" if args.async_mode else "sync",
        "total": len(prompts),
        "succeeded": len(prompts) - failures,
        "failed": failures,
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "results": results,
    })
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())