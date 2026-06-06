"""
API v1 — Prediction, plant info, and health endpoints.
"""

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from loguru import logger

from app.core.labels import PLANT_METADATA, DISEASE_LABELS
from app.models.schemas import (
    ErrorResponse,
    HealthResponse,
    PlantInfoResponse,
    PredictionResponse,
)
from app.utils.image_utils import validate_and_load_image

api_router = APIRouter()


def get_model_service(request: Request):
    """Dependency: retrieve the ModelService stored on app state."""
    svc = getattr(request.app.state, "model_service", None)
    if svc is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model service not initialized. Please retry shortly.",
        )
    return svc


# ── POST /predict ─────────────────────────────────────────────────────────────

@api_router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict plant species and disease from an image",
    responses={
        413: {"model": ErrorResponse, "description": "Image too large"},
        415: {"model": ErrorResponse, "description": "Unsupported media type"},
        422: {"model": ErrorResponse, "description": "Invalid image"},
        503: {"model": ErrorResponse, "description": "Models not loaded"},
    },
    tags=["Prediction"],
)
async def predict(
    file: UploadFile = File(..., description="JPEG or PNG leaf/plant image (max 10 MB)"),
    model_service=Depends(get_model_service),
):
    """
    Upload a plant or leaf image and receive:
    - **Plant identification** with scientific details
    - **Disease detection** with causes, prevention, and treatment advice
    """
    image = await validate_and_load_image(file)
    logger.info(f"Running prediction for file: {file.filename}")

    try:
        result = await model_service.predict(image)
    except Exception as e:
        logger.exception(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed. Please try again with a clearer image.",
        )

    logger.info(
        f"Prediction complete | plant={result.plant.name} ({result.plant.confidence:.0%}) | "
        f"disease={result.disease.name} ({result.disease.confidence:.0%}) | "
        f"time={result.processing_time_ms:.1f}ms"
    )
    return result


# ── GET /plant-info/{plant_name} ──────────────────────────────────────────────

@api_router.get(
    "/plant-info/{plant_name}",
    response_model=PlantInfoResponse,
    summary="Get detailed information about a plant species",
    tags=["Plant Info"],
)
async def get_plant_info(plant_name: str):
    """
    Retrieve structured information for a known plant species.
    Use the common name (e.g., `Tomato`, `Apple`, `Potato`).
    """
    # Case-insensitive lookup
    matched_key = next(
        (k for k in PLANT_METADATA if k.lower() == plant_name.lower()), None
    )
    if matched_key is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Plant '{plant_name}' not found. "
                f"Available plants: {', '.join(sorted(PLANT_METADATA.keys()))}"
            ),
        )

    meta = PLANT_METADATA[matched_key]

    # Gather known diseases for this plant
    known_diseases = [
        v["disease"]
        for v in DISEASE_LABELS.values()
        if v["plant"].lower() in matched_key.lower() and not v["healthy"]
    ]

    return PlantInfoResponse(
        name=matched_key,
        scientific_name=meta["scientific_name"],
        family=meta.get("family", "Unknown"),
        description=meta["description"],
        common_names=meta["common_names"],
        uses=meta["uses"],
        growing_conditions=meta["growing_conditions"],
        interesting_facts=meta["interesting_facts"],
        origin=meta.get("origin", "Unknown"),
        season=meta.get("season", "Unknown"),
        known_diseases=known_diseases,
    )


# ── GET /plants ───────────────────────────────────────────────────────────────

@api_router.get(
    "/plants",
    summary="List all supported plant species",
    tags=["Plant Info"],
)
async def list_plants():
    """Return a list of all plant species supported by the prediction models."""
    return {
        "count": len(PLANT_METADATA),
        "plants": sorted(PLANT_METADATA.keys()),
    }


# ── GET /health ───────────────────────────────────────────────────────────────

@api_router.get(
    "/health",
    response_model=HealthResponse,
    summary="API health check",
    tags=["Monitoring"],
)
async def health_check(model_service=Depends(get_model_service)):
    """Returns service status and model load state."""
    loaded = not model_service.demo_mode
    return HealthResponse(
        status="healthy" if loaded else "demo_mode",
        models_loaded=loaded,
        species_model="efficientnet_b3_species_v1",
        disease_model="efficientnet_b3_disease_v1",
        version="1.0.0",
    )
