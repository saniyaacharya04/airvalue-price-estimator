import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.session import Base, engine
from app.api.auth import router as auth_router
from app.api.predict import router as predict_router
from app.api.history import router as history_router
from app.api.premium import router as premium_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("airvalue")

app = FastAPI(
    title="AirValue – Airbnb Price Estimator",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)
logger.info("Database tables ensured")

app.include_router(auth_router)
app.include_router(predict_router)
app.include_router(history_router)
app.include_router(premium_router)

FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "static")
)

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
    logger.info("Frontend mounted")
else:
    logger.info("Running in API-only mode")
