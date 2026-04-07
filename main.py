import gzip
import logging
import shutil
import threading
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

import uvicorn

from app.config        import config
from app.serial_reader import reader_loop
from app.server        import app


def _gz_rotator(source: str, dest: str) -> None:
    with open(source, "rb") as f_in, gzip.open(dest + ".gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    Path(source).unlink()


_file_handler = TimedRotatingFileHandler(
    filename    = "app.log",
    when        = "midnight",
    interval    = 1,
    backupCount = 7,
    encoding    = "utf-8",
    utc         = False,
)
_file_handler.rotator  = _gz_rotator
_file_handler.setFormatter(logging.Formatter(
    fmt     = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
))

logging.basicConfig(
    level    = logging.INFO,
    format   = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt  = "%Y-%m-%d %H:%M:%S",
    handlers = [logging.StreamHandler(), _file_handler],
)


def main() -> None:
    t = threading.Thread(target=reader_loop, daemon=True)
    t.start()

    logging.info(f"[SERVER] Starting on {config.HOST}:{config.PORT}")
    logging.info(f"[SERVER] AI backend : {config.AI_BASE_URL}")
    logging.info(f"[SERVER] Serial port: {config.SERIAL_PORT} @ {config.BAUDRATE} baud")

    uvicorn.run(
        "app.server:app",
        host    = config.HOST,
        port    = config.PORT,
        reload  = False,
    )


if __name__ == "__main__":
    main()
