import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db.session import Base, engine
from app.models import User, Prediction

from app.api.auth import router as auth_router
from app.api.predict import router as predict_router
from app.api.history import router as history_router
from app.api.premium import router as premium_router

# --------------------------------------------------
# Application Setup
# --------------------------------------------------

app = FastAPI(
    title="AirValue – Airbnb Price Estimator",
    version="1.0.0",
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("airvalue")

# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

Base.metadata.create_all(bind=engine)
logger.info("Database tables ensured.")

# --------------------------------------------------
# API Routers
# --------------------------------------------------

app.include_router(auth_router)
app.include_router(predict_router)
app.include_router(history_router)
app.include_router(premium_router)

# --------------------------------------------------
# Static Frontend (HTML / JS)
# --------------------------------------------------

FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "static")
)

if os.path.exists(FRONTEND_DIR):
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="static",
    )
    logger.info("Frontend static files mounted.")
else:
    logger.warning("Frontend directory not found. API-only mode enabled.")
