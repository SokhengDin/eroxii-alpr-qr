import logging
import time
from datetime import datetime

import serial

from . import state
from .config  import config
from .pusher  import push_manual_exit

logger = logging.getLogger(__name__)


def reader_loop() -> None:
    while True:
        ser = None
        try:
            logger.info(f"[SERIAL] Opening {config.SERIAL_PORT} @ {config.BAUDRATE} baud ...")
            ser = serial.Serial(config.SERIAL_PORT, config.BAUDRATE, timeout=config.SERIAL_TIMEOUT)
            logger.info(f"[SERIAL] Connected on {config.SERIAL_PORT}")

            while True:
                raw = ser.readline()
                if raw:
                    qr_text = raw.decode("utf-8", errors="ignore").strip()
                    if qr_text:
                        _handle_scan(qr_text)

                time.sleep(0.02)

        except Exception as e:
            logger.error(f"[SERIAL] Error: {e}")
            logger.info(f"[SERIAL] Retrying in {config.SERIAL_RETRY_SECONDS}s ...")
            time.sleep(config.SERIAL_RETRY_SECONDS)

        finally:
            try:
                if ser and ser.is_open:
                    ser.close()
            except Exception:
                pass


def _handle_scan(qr_text: str) -> None:
    now_ts  = time.time()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with state.lock:
        is_duplicate = (
            qr_text == state.last_qr
            and (now_ts - state.last_qr_time) < config.DUPLICATE_IGNORE_SECONDS
        )

        if is_duplicate:
            logger.debug(f"[SERIAL] Duplicate ignored: {qr_text}")
            return

        state.latest_qr     = qr_text
        state.latest_time   = now_str
        state.has_new_qr    = True
        state.scan_count   += 1
        state.last_qr       = qr_text
        state.last_qr_time  = now_ts

    logger.info(f"[SERIAL] Scanned #{state.scan_count}: {qr_text}")

    push_manual_exit(qr_text)
