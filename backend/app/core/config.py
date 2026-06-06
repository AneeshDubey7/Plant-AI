"""
Application configuration — loaded from environment variables / .env file.
"""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── App ────────────────────────────────────────────────────
    APP_NAME: str = "Plant Disease Prediction System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # ── CORS ───────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://plant-disease-app.vercel.app",
    ]

    # ── Model paths ────────────────────────────────────────────
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"
    MODEL_SPECIES_PATH: str = "models/species_efficientnet_b3.onnx"
    MODEL_DISEASE_PATH: str = "models/disease_efficientnet_b3.onnx"

    # ── Inference ──────────────────────────────────────────────
    SPECIES_CONFIDENCE_THRESHOLD: float = 0.40
    DISEASE_CONFIDENCE_THRESHOLD: float = 0.50
    MAX_IMAGE_SIZE_MB: int = 10
    IMAGE_SIZE: int = 300  # EfficientNet-B3 input size

    # ── Rate limiting ──────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = 30

    @property
    def MAX_IMAGE_BYTES(self) -> int:
        return self.MAX_IMAGE_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
