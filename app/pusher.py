import logging
from concurrent.futures import ThreadPoolExecutor

import httpx

from .config import config

logger = logging.getLogger(__name__)

# ── Shared HTTP client (persistent connection pool, keep-alive) ───────────────
_http_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.Client(
            timeout=config.AI_PUSH_TIMEOUT,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _http_client


# ── Bounded thread pool — at most 4 concurrent pushes, queue up to 20 ────────
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="pusher")


def push_manual_exit(plate_number: str) -> None:
    if not config.AI_PUSH_ENABLED:
        logger.debug("[PUSHER] Push disabled — skipping.")
        return

    _executor.submit(_do_push, plate_number)


def _do_push(plate_number: str) -> None:
    url     = f"{config.AI_BASE_URL.rstrip('/')}/api/v1/manual-exit"
    payload = {"plate_number": plate_number, "qr_scan": True}

    try:
        logger.info(f"[PUSHER] POST {url}  plate_number={plate_number}")

        resp = _get_client().post(url, json=payload)
        resp.raise_for_status()

        logger.info(f"[PUSHER] {resp.status_code} — {resp.text[:200]}")

    except httpx.ConnectError:
        logger.error(f"[PUSHER] Connection failed — {url} unreachable.")
    except httpx.TimeoutException:
        logger.error(f"[PUSHER] Timed out after {config.AI_PUSH_TIMEOUT}s.")
    except httpx.HTTPStatusError as e:
        logger.error(f"[PUSHER] HTTP {e.response.status_code} — {e.response.text[:200]}")
    except Exception as e:
        logger.error(f"[PUSHER] Unexpected error: {e}")
