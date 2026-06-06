"""
Pydantic schemas for API request/response validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


# ── Plant Info ────────────────────────────────────────────────────────────────

class PlantResult(BaseModel):
    name: str = Field(..., description="Common plant name")
    scientific_name: str = Field(..., description="Scientific (Latin) name")
    family: str = Field(..., description="Plant family")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence 0–1")
    description: str
    common_names: List[str]
    uses: List[str]
    growing_conditions: str
    interesting_facts: List[str]
    origin: str
    season: str


# ── Disease Info ──────────────────────────────────────────────────────────────

class DiseaseResult(BaseModel):
    detected: bool = Field(..., description="True if disease detected")
    name: str = Field(..., description="Disease name or 'Healthy'")
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: str = Field(..., description="none | mild | moderate | severe")
    pathogen: str
    description: str
    causes: List[str]
    prevention: List[str]
    treatment: List[str]


# ── Full Prediction Response ──────────────────────────────────────────────────

class PredictionResponse(BaseModel):
    image_id: str = Field(..., description="Unique identifier for this prediction")
    plant: PlantResult
    disease: DiseaseResult
    processing_time_ms: float
    model_versions: dict = Field(
        default={"species": "efficientnet_b3_v1", "disease": "efficientnet_b3_v1"}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "plant": {
                    "name": "Tomato",
                    "scientific_name": "Solanum lycopersicum",
                    "family": "Solanaceae",
                    "confidence": 0.94,
                    "description": "Tomato is a fruiting plant native to South America...",
                    "common_names": ["Tomato", "Love Apple"],
                    "uses": ["Culinary", "Medicinal"],
                    "growing_conditions": "Full sun, well-drained soil...",
                    "interesting_facts": ["Botanically a fruit..."],
                    "origin": "South America",
                    "season": "Summer-Autumn",
                },
                "disease": {
                    "detected": True,
                    "name": "Early Blight",
                    "confidence": 0.87,
                    "severity": "moderate",
                    "pathogen": "Alternaria solani",
                    "description": "Early Blight is a common fungal disease...",
                    "causes": ["Warm, humid weather"],
                    "prevention": ["Use certified disease-free seeds"],
                    "treatment": ["Apply copper-based fungicides"],
                },
                "processing_time_ms": 342.5,
            }
        }


# ── Plant Info (standalone) ───────────────────────────────────────────────────

class PlantInfoResponse(BaseModel):
    name: str
    scientific_name: str
    family: str
    description: str
    common_names: List[str]
    uses: List[str]
    growing_conditions: str
    interesting_facts: List[str]
    origin: str
    season: str
    known_diseases: List[str]


# ── Health Check ──────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    species_model: str
    disease_model: str
    version: str


# ── Error ─────────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
