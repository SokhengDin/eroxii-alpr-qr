import logging
import threading

import httpx

from .config import config

logger = logging.getLogger(__name__)


def push_manual_exit(plate_number: str) -> None:
    """
    Fire-and-forget push to the AI backend.
    Runs in a background thread so it never blocks the serial reader.
    """
    if not config.AI_PUSH_ENABLED:
        logger.debug("[PUSHER] Push disabled — skipping.")
        return

    t = threading.Thread(target=_do_push, args=(plate_number,), daemon=True)
    t.start()


def _do_push(plate_number: str) -> None:
    url     = f"{config.AI_BASE_URL.rstrip('/')}/api/v1/manual-exit"
    payload = {"plate_number": plate_number}

    try:
        logger.info(f"[PUSHER] POST {url}  plate_number={plate_number}")

        with httpx.Client(timeout=config.AI_PUSH_TIMEOUT) as client:
            resp = client.post(url, json=payload)
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
