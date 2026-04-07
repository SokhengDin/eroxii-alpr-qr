from fastapi           import FastAPI
from fastapi.responses import JSONResponse

from . import state
from .config import config

app = FastAPI(title="USB QR Reader Host Server", version="1.0.0")


@app.get("/")
def home():
    return {
        "status"   : "running",
        "message"  : "USB QR Reader Host Server",
        "endpoints": {
            "get_qr": f"http://{config.HOST}:{config.PORT}/get_qr",
            "latest": f"http://{config.HOST}:{config.PORT}/latest",
            "health": f"http://{config.HOST}:{config.PORT}/health",
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/get_qr")
def get_qr():
    with state.lock:
        if state.has_new_qr:
            data = {
                "status"    : "new",
                "qr"        : state.latest_qr,
                "time"      : state.latest_time,
                "scan_count": state.scan_count,
            }
            state.has_new_qr = False
            return JSONResponse(content=data)

        return JSONResponse(content={
            "status"    : "empty",
            "qr"        : "",
            "time"      : "",
            "scan_count": state.scan_count,
        })


@app.get("/latest")
def latest():
    with state.lock:
        return {
            "status"    : "ok",
            "qr"        : state.latest_qr,
            "time"      : state.latest_time,
            "scan_count": state.scan_count,
        }
