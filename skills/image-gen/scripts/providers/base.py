"""Abstract base class for image generation providers.

All OpenAI / NewAPI-compatible services implement the same surface:
  - submit_sync(model, prompt, **kwargs) -> dict
  - submit_async(model, prompt, **kwargs) -> dict (returns task ID)
  - poll_async(task_id) -> dict

Concrete providers normalize request bodies and parse response shapes for their
specific endpoints. The normalized output is a dict that the calling CLI knows
how to consume (urls / b64_json / task_id / status / progress).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ImageProvider(ABC):
    """Common contract for any OpenAI/NewAPI-compatible image service."""

    name: str = "base"
    base_url: str = ""
    default_model: str = "gpt-image-2"

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        if not api_key:
            raise ValueError(
                f"[{self.name}] api_key is empty. Set IMAGE_GEN_API_KEY "
                f"or {self.name.upper()}_API_KEY env var, or pass --api-key."
            )
        self.api_key = api_key
        self.base_url = (base_url or self.base_url).rstrip("/")

    # ---- public API -------------------------------------------------

    @abstractmethod
    def submit_sync(
        self,
        *,
        model: Optional[str] = None,
        prompt: str,
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        quality: Optional[str] = None,
        image: Optional[List[str]] = None,
        **extra: Any,
    ) -> Dict[str, Any]:
        """Synchronous submission. Returns a normalized dict:

        {
          "created": int,
          "model": str,
          "items": [{"url": str} | {"b64_json": str}, ...]
        }
        """

    @abstractmethod
    def submit_async(
        self,
        *,
        model: Optional[str] = None,
        prompt: str,
        n: int = 1,
        size: str = "1024x1024",
        response_format: str = "url",
        quality: Optional[str] = None,
        image: Optional[List[str]] = None,
        **extra: Any,
    ) -> Dict[str, Any]:
        """Async submission. Returns normalized:

        {"task_id": str, "raw": <provider response>}
        """

    @abstractmethod
    def poll_async(self, task_id: str) -> Dict[str, Any]:
        """Poll an async task. Returns normalized:

        {
          "task_id": str,
          "status": "pending" | "in_progress" | "success" | "failed",
          "progress": str | None,        # e.g. "42%"
          "items": [...],                # when status == "success"
          "error": {"code": str, "message": str} | None,
        }
        """

    # ---- helpers ----------------------------------------------------

    def auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _coerce_int(value: Any, default: int = 1) -> int:
        try:
            n = int(value)
        except (TypeError, ValueError):
            return default
        return n if n > 0 else default

    @staticmethod
    def _first(*keys: str, source: Optional[Dict[str, Any]] = None) -> Any:
        """Pick the first present key from a dict. Used because providers vary
        on whether they return 'id', 'task_id', or 'taskId'."""
        for k in keys:
            if source and source.get(k):
                return source[k]
        return None

    @staticmethod
    def normalize_status(raw: Optional[str]) -> str:
        """Map provider-specific status strings onto a small canonical set."""
        if not raw:
            return "pending"
        s = raw.lower()
        if s in {"success", "succeeded", "completed", "done", "finished"}:
            return "success"
        if s in {"fail", "failed", "failure", "error", "cancelled", "canceled"}:
            return "failed"
        if s in {"in_progress", "running", "processing", "queued", "started"}:
            return "in_progress"
        return s  # unknown → leave it as-is for debugging

    @staticmethod
    def extract_items(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Pull a list of {url|b64_json} items out of an arbitrary response shape.

        Tries: data → images → result → results.
        """
        for key in ("data", "images", "result", "results"):
            container = raw.get(key)
            if isinstance(container, list) and container:
                return [item for item in container if isinstance(item, dict)]
        return []