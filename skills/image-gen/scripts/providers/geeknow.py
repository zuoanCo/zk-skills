"""Geeknow AI image generation provider.

Endpoint reference (from https://docs.geeknow.top):
  - Sync:  POST  /v1/images/generations
  - Async: POST  /v1/images/generations/async
  - Poll:  GET   /v1/images/generations/async/{task_id}

Auth:  Authorization: Bearer <api_key>
Body:  OpenAI-shaped (model, prompt, n, size, response_format, quality, image)
       Reference images in async mode must be public http(s) URLs (no b64).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import ImageProvider


class GeeknowProvider(ImageProvider):
    name = "geeknow"
    base_url = "https://www.geeknow.top/v1"
    default_model = "gpt-image-2"

    def _endpoint(self, suffix: str) -> str:
        return f"{self.base_url}{suffix}"

    # ---- sync -------------------------------------------------------

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
        body = self._build_body(
            model=model or self.default_model,
            prompt=prompt,
            n=n,
            size=size,
            response_format=response_format,
            quality=quality,
            image=image,
            **extra,
        )
        # The caller (CLI scripts) will inject `client` for the actual HTTP call
        # so we can keep this provider free of HTTP details. We return a request
        # descriptor instead.
        return {
            "method": "POST",
            "url": self._endpoint("/images/generations"),
            "headers": self.auth_headers(),
            "body": body,
            "_kind": "image.sync",
        }

    # ---- async submit ----------------------------------------------

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
        body = self._build_body(
            model=model or self.default_model,
            prompt=prompt,
            n=n,
            size=size,
            response_format=response_format,
            quality=quality,
            image=image,
            **extra,
        )
        return {
            "method": "POST",
            "url": self._endpoint("/images/generations/async"),
            "headers": self.auth_headers(),
            "body": body,
            "_kind": "image.async.submit",
        }

    # ---- async poll ------------------------------------------------

    def poll_async(self, task_id: str) -> Dict[str, Any]:
        return {
            "method": "GET",
            "url": self._endpoint(f"/images/generations/async/{task_id}"),
            "headers": self.auth_headers(),
            "_kind": "image.async.poll",
        }

    # ---- response normalization ------------------------------------

    def normalize_sync(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        items = self.extract_items(raw)
        return {
            "created": raw.get("created"),
            "model": raw.get("model"),
            "items": items,
        }

    def normalize_async_submit(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        task_id = self._first("id", "task_id", "taskId", source=raw)
        return {
            "task_id": task_id,
            "raw": raw,
        }

    def normalize_async_poll(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        task_id = self._first("id", "task_id", "taskId", source=raw) or raw.get("task_id")
        status = self.normalize_status(raw.get("status"))
        progress = raw.get("progress")
        items = self.extract_items(raw)

        error = None
        if status == "failed":
            err = raw.get("error") or {}
            error = {
                "code": err.get("code"),
                "message": err.get("message") or err.get("msg") or "unknown error",
            }

        return {
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "items": items if status == "success" else [],
            "error": error,
        }

    # ---- helpers ----------------------------------------------------

    @staticmethod
    def _build_body(
        *,
        model: str,
        prompt: str,
        n: int,
        size: str,
        response_format: str,
        quality: Optional[str],
        image: Optional[List[str]],
        **extra: Any,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "n": ImageProvider._coerce_int(n),
            "size": size,
            "response_format": response_format,
        }
        if quality:
            body["quality"] = quality
        if image:
            body["image"] = image
        # Pass through anything caller wants to add (background, style, watermark, ...)
        for k, v in extra.items():
            if v is not None and k not in body:
                body[k] = v
        return body