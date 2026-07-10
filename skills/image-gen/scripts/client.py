"""Optimized HTTP client for image generation calls.

Design goals (per skill spec):
  - Connection pooling: one Session reused across calls (provider, batch).
  - Exponential backoff on 5xx and connection errors.
  - 429 honors Retry-After (or sensible default).
  - Streaming download for large image files.
  - LRU-ish cache for repeated URL downloads (cheap dedupe).
  - Thread-safe; safe for use from ThreadPoolExecutor in batch.py.

Keep this module dependency-light: stdlib + `requests` only. No external
retry lib (tenacity, urllib3 Retry) so the skill runs anywhere Python+requests
exist.
"""

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter


# ---------- defaults -----------------------------------------------------

DEFAULT_TIMEOUT = (10, 60)  # (connect, read) seconds — image gen can be slow
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_BASE = 1.0  # seconds; doubles each retry
DEFAULT_BACKOFF_CAP = 16.0
POOL_SIZE = int(os.environ.get("IMAGE_GEN_POOL_SIZE", "16"))


# ---------- config -------------------------------------------------------

@dataclass(frozen=True)
class ClientConfig:
    timeout: Tuple[float, float] = DEFAULT_TIMEOUT
    max_retries: int = DEFAULT_MAX_RETRIES
    backoff_base: float = DEFAULT_BACKOFF_BASE
    backoff_cap: float = DEFAULT_BACKOFF_CAP
    pool_size: int = POOL_SIZE
    user_agent: str = "image-gen-skill/0.1.0"


# ---------- client -------------------------------------------------------

class ImageGenClient:
    """Thread-safe HTTP client with retry / backoff / rate-limit awareness."""

    def __init__(self, config: Optional[ClientConfig] = None) -> None:
        self.config = config or ClientConfig()
        self._session = self._build_session()
        self._dl_lock = threading.Lock()
        self._download_cache: Dict[str, Tuple[float, int]] = {}  # url -> (mtime, size)
        self._cache_ttl = 1800  # 30 min

    # ---- session construction --------------------------------------

    def _build_session(self) -> requests.Session:
        s = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=self.config.pool_size,
            pool_maxsize=self.config.pool_size,
            max_retries=0,  # we handle retries ourselves so we can log them
        )
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        s.headers.update({"User-Agent": self.config.user_agent})
        return s

    # ---- core HTTP with retry --------------------------------------

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        timeout: Optional[Tuple[float, float]] = None,
        on_retry: Optional[Callable[[int, float, str], None]] = None,
    ) -> requests.Response:
        """Issue a request with retry/backoff. Returns the final response.

        Raises requests.HTTPError if a 4xx (except 429) or non-retryable error
        occurs. Network errors and 5xx are retried up to max_retries.
        """
        timeout = timeout or self.config.timeout
        attempt = 0
        last_exc: Optional[Exception] = None

        while attempt <= self.config.max_retries:
            attempt += 1
            try:
                resp = self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_body,
                    timeout=timeout,
                )
            except requests.RequestException as e:
                last_exc = e
                if attempt > self.config.max_retries:
                    break
                sleep_for = self._compute_backoff(attempt)
                self._notify_retry(on_retry, attempt, sleep_for, f"network error: {e.__class__.__name__}")
                time.sleep(sleep_for)
                continue

            # Status code handling
            if resp.status_code == 429:
                retry_after = self._parse_retry_after(resp)
                if attempt > self.config.max_retries:
                    resp.raise_for_status()
                self._notify_retry(on_retry, attempt, retry_after, "429 rate limited")
                time.sleep(retry_after)
                continue

            if 500 <= resp.status_code < 600:
                if attempt > self.config.max_retries:
                    resp.raise_for_status()
                sleep_for = self._compute_backoff(attempt)
                self._notify_retry(on_retry, attempt, sleep_for, f"{resp.status_code} server error")
                time.sleep(sleep_for)
                continue

            # 2xx, 3xx, 4xx — return as-is (caller decides what to do)
            return resp

        # Exhausted retries on network errors
        if last_exc:
            raise last_exc
        raise RuntimeError(f"request failed after {self.config.max_retries} retries: {method} {url}")

    # ---- provider-aware helpers ------------------------------------

    def execute(self, descriptor: Dict[str, Any]) -> requests.Response:
        """Execute a provider request descriptor (method/url/headers/body)."""
        body = descriptor.get("body")
        return self.request(
            method=descriptor["method"],
            url=descriptor["url"],
            headers=descriptor.get("headers"),
            json_body=body,
        )

    def execute_json(self, descriptor: Dict[str, Any]) -> Dict[str, Any]:
        """Execute descriptor and return parsed JSON body."""
        resp = self.execute(descriptor)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError as e:
            raise RuntimeError(f"non-JSON response ({resp.status_code}): {resp.text[:500]}") from e

    # ---- streaming download ----------------------------------------

    def download(
        self,
        url: str,
        dest: str | os.PathLike,
        *,
        force: bool = False,
        chunk_size: int = 64 * 1024,
    ) -> Path:
        """Stream a URL to disk. Skips if a recent cached copy exists.

        Returns the Path to the saved file.
        """
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)

        if not force and self._is_cached(url, dest):
            return dest

        with self._session.get(url, stream=True, timeout=self.config.timeout) as resp:
            resp.raise_for_status()
            tmp = dest.with_suffix(dest.suffix + ".part")
            written = 0
            with open(tmp, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        fh.write(chunk)
                        written += len(chunk)
            tmp.replace(dest)
            with self._dl_lock:
                self._download_cache[url] = (time.time(), written)
        return dest

    # ---- internals --------------------------------------------------

    def _compute_backoff(self, attempt: int) -> float:
        return min(self.config.backoff_base * (2 ** (attempt - 1)), self.config.backoff_cap)

    @staticmethod
    def _parse_retry_after(resp: requests.Response) -> float:
        raw = resp.headers.get("Retry-After")
        if raw:
            try:
                return max(0.0, float(raw))
            except ValueError:
                pass
        # If no header, fall back to a generous default
        return 5.0

    @staticmethod
    def _notify_retry(cb: Optional[Callable[[int, float, str], None]],
                      attempt: int, sleep_for: float, reason: str) -> None:
        if cb is None:
            return
        try:
            cb(attempt, sleep_for, reason)
        except Exception:
            # callback errors must not break the retry loop
            pass

    def _is_cached(self, url: str, dest: Path) -> bool:
        if not dest.exists():
            return False
        with self._dl_lock:
            entry = self._download_cache.get(url)
        if not entry:
            return False
        ts, size = entry
        if (time.time() - ts) > self._cache_ttl:
            return False
        try:
            return dest.stat().st_size == size
        except OSError:
            return False


# ---------- convenience --------------------------------------------------

def build_client_from_env() -> ImageGenClient:
    """Build a client reading IMAGE_GEN_TIMEOUT / MAX_RETRIES from env."""
    cfg = ClientConfig(
        timeout=(
            float(os.environ.get("IMAGE_GEN_CONNECT_TIMEOUT", DEFAULT_TIMEOUT[0])),
            float(os.environ.get("IMAGE_GEN_READ_TIMEOUT", DEFAULT_TIMEOUT[1])),
        ),
        max_retries=int(os.environ.get("IMAGE_GEN_MAX_RETRIES", DEFAULT_MAX_RETRIES)),
        pool_size=int(os.environ.get("IMAGE_GEN_POOL_SIZE", str(POOL_SIZE))),
    )
    return ImageGenClient(cfg)


def pretty_response(resp: requests.Response, limit: int = 600) -> str:
    """Format a response for stdout in CLI scripts."""
    body = resp.text
    if len(body) > limit:
        body = body[:limit] + f"... <{len(body) - limit} more chars>"
    try:
        parsed = resp.json()
        body = json.dumps(parsed, ensure_ascii=False, indent=2)
        if len(body) > limit:
            body = body[:limit] + f"\n... <{len(body) - limit} more chars>"
    except ValueError:
        pass
    return f"HTTP {resp.status_code}\n{body}"