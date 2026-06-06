"""
Plant Disease Prediction System — FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.services.model_service import ModelService

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML models on startup, clean up on shutdown."""
    logger.info("🌿 Starting Plant Disease Prediction System...")
    model_service = ModelService()
    await model_service.load_models()
    app.state.model_service = model_service
    logger.info("✅ Models loaded successfully. API ready.")
    yield
    logger.info("🛑 Shutting down. Releasing resources...")
    await model_service.cleanup()


def create_application() -> FastAPI:
    app = FastAPI(
        title="Plant Disease Prediction API",
        description=(
            "A two-stage deep learning API that identifies plant species "
            "and detects diseases from leaf images."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── Middleware ──────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # ── Routes ──────────────────────────────────────────────────
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_application()


@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "Plant Disease Prediction API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
    }
