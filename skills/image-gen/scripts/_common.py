"""Shared utilities for image-gen CLI scripts.

Provides:
  - load_provider(name, api_key, base_url) -> ImageProvider
  - emit_json(obj) for stable machine-readable output
  - resolve_api_key(provider_name) -> str | None (env-first, then config file)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "config.json"
CONFIG_EXAMPLE = SKILL_ROOT / "config.example.json"


def emit_json(obj: Any) -> None:
    """Print a JSON object to stdout. Always UTF-8, no escaping."""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


def emit_error(msg: str, *, hint: Optional[str] = None, code: int = 1) -> None:
    """Emit a structured error to stderr and exit."""
    payload = {"ok": False, "error": msg}
    if hint:
        payload["hint"] = hint
    sys.stderr.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.exit(code)


def resolve_api_key(provider_name: str, override: Optional[str] = None) -> Optional[str]:
    """Precedence: explicit override > provider-specific env > generic env > config file."""
    if override:
        return override
    upper = provider_name.upper()
    for var in (f"{upper}_API_KEY", "IMAGE_GEN_API_KEY", "OPENAI_API_KEY"):
        v = os.environ.get(var)
        if v:
            return v
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            return None
        key_path = ["providers", provider_name, "api_key"]
        cur: Any = cfg
        for k in key_path:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return None
        return cur if isinstance(cur, str) else None
    return None


def resolve_base_url(provider_name: str, override: Optional[str] = None) -> Optional[str]:
    if override:
        return override
    upper = provider_name.upper()
    for var in (f"{upper}_BASE_URL", "IMAGE_GEN_BASE_URL"):
        v = os.environ.get(var)
        if v:
            return v
    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            return None
        url_path = ["providers", provider_name, "base_url"]
        cur: Any = cfg
        for k in url_path:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return None
        return cur if isinstance(cur, str) else None
    return None


def load_provider(
    name: str = "geeknow",
    *,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
):
    """Instantiate a provider by name. Defaults to Geeknow."""
    if name == "geeknow":
        from providers.geeknow import GeeknowProvider
        return GeeknowProvider(
            api_key=resolve_api_key(name, api_key) or "",
            base_url=resolve_base_url(name, base_url),
        )
    raise ValueError(
        f"unknown provider: {name}. Available: geeknow. "
        f"To add a new provider, see references/providers.md."
    )