import logging
import threading

import uvicorn

from app.config        import config
from app.serial_reader import reader_loop
from app.server        import app

logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
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
