from fastapi import FastAPI

from t360 import __version__
from t360.config import settings

app = FastAPI(title="T-360", version=__version__)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "version": __version__,
        "mode": settings.trading_mode.value,
        "broker": settings.broker.value,
    }
