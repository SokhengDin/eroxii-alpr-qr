import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── Serial ────────────────────────────────────────────────────────────────
    SERIAL_PORT             : str   = os.getenv("SERIAL_PORT",              "COM3")
    BAUDRATE                : int   = int(os.getenv("BAUDRATE",             "9600"))
    SERIAL_TIMEOUT          : float = float(os.getenv("SERIAL_TIMEOUT",     "1"))
    SERIAL_RETRY_SECONDS    : int   = int(os.getenv("SERIAL_RETRY_SECONDS", "3"))

    # ── Duplicate suppression ─────────────────────────────────────────────────
    DUPLICATE_IGNORE_SECONDS: int   = int(os.getenv("DUPLICATE_IGNORE_SECONDS", "3"))

    # ── Server ────────────────────────────────────────────────────────────────
    HOST                    : str   = os.getenv("HOST", "0.0.0.0")
    PORT                    : int   = int(os.getenv("PORT", "5000"))

    # ── AI backend ────────────────────────────────────────────────────────────
    AI_BASE_URL             : str   = os.getenv("AI_BASE_URL",    "http://localhost:8000")
    AI_PUSH_TIMEOUT         : int   = int(os.getenv("AI_PUSH_TIMEOUT", "10"))
    AI_PUSH_ENABLED         : bool  = os.getenv("AI_PUSH_ENABLED", "true").lower() == "true"


config = Config()
