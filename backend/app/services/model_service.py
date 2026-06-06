"""
ModelService — loads ONNX models and runs two-stage inference pipeline.

Stage 1: Species classification  (EfficientNet-B3, 14 classes)
Stage 2: Disease classification  (EfficientNet-B3, 38 classes)

Falls back to demo/mock mode if model files are not found, so the API
can be demoed without trained weights.
"""

import time
import uuid
import random
from pathlib import Path
from typing import Tuple, Dict, Any, Optional

import numpy as np
from PIL import Image
from loguru import logger

from app.core.config import settings
from app.core.labels import (
    SPECIES_LABELS,
    DISEASE_LABELS,
    PLANT_METADATA,
    DISEASE_METADATA,
)
from app.models.schemas import PlantResult, DiseaseResult, PredictionResponse

# Optional ONNX runtime — graceful fallback
try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    logger.warning("onnxruntime not installed. Running in DEMO mode.")


# ── Image preprocessing constants ────────────────────────────────────────────
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)
INPUT_SIZE = settings.IMAGE_SIZE  # 300 for EfficientNet-B3


class ModelService:
    """Singleton-style service that holds loaded ONNX sessions."""

    def __init__(self):
        self.species_session: Optional[Any] = None
        self.disease_session: Optional[Any] = None
        self.demo_mode: bool = False

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    async def load_models(self) -> None:
        """Load ONNX model files. Falls back to demo mode if files missing."""
        species_path = Path(settings.MODEL_SPECIES_PATH)
        disease_path = Path(settings.MODEL_DISEASE_PATH)

        if not ONNX_AVAILABLE or not species_path.exists() or not disease_path.exists():
            logger.warning(
                "⚠️  Model files not found or ONNX unavailable. Starting in DEMO mode. "
                "Predictions will return realistic-looking mock data."
            )
            self.demo_mode = True
            return

        opts = ort.SessionOptions()
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]

        self.species_session = ort.InferenceSession(
            str(species_path), sess_options=opts, providers=providers
        )
        self.disease_session = ort.InferenceSession(
            str(disease_path), sess_options=opts, providers=providers
        )
        logger.info(f"✅ Species model loaded: {species_path}")
        logger.info(f"✅ Disease model loaded: {disease_path}")

    async def cleanup(self) -> None:
        self.species_session = None
        self.disease_session = None

    # ── Public API ────────────────────────────────────────────────────────────

    async def predict(self, image: Image.Image) -> PredictionResponse:
        """Run full two-stage prediction pipeline on a PIL Image."""
        start = time.perf_counter()
        image_id = str(uuid.uuid4())

        if self.demo_mode:
            result = self._demo_predict(image_id)
        else:
            result = self._onnx_predict(image, image_id)

        elapsed_ms = (time.perf_counter() - start) * 1000
        result.processing_time_ms = round(elapsed_ms, 2)
        return result

    # ── ONNX inference ────────────────────────────────────────────────────────

    def _onnx_predict(self, image: Image.Image, image_id: str) -> PredictionResponse:
        tensor = self._preprocess(image)

        # Stage 1: Species
        species_input_name = self.species_session.get_inputs()[0].name
        species_logits = self.species_session.run(None, {species_input_name: tensor})[0]
        species_probs = self._softmax(species_logits[0])
        species_idx = int(np.argmax(species_probs))
        species_conf = float(species_probs[species_idx])
        species_name = SPECIES_LABELS.get(species_idx, "Unknown Plant")

        # Stage 2: Disease
        disease_input_name = self.disease_session.get_inputs()[0].name
        disease_logits = self.disease_session.run(None, {disease_input_name: tensor})[0]
        disease_probs = self._softmax(disease_logits[0])
        disease_idx = int(np.argmax(disease_probs))
        disease_conf = float(disease_probs[disease_idx])
        disease_info = DISEASE_LABELS.get(disease_idx, {"plant": "Unknown", "disease": "Unknown", "healthy": True})

        plant_result = self._build_plant_result(species_name, species_conf)
        disease_result = self._build_disease_result(
            disease_info["disease"], disease_conf, disease_info["healthy"]
        )

        return PredictionResponse(
            image_id=image_id,
            plant=plant_result,
            disease=disease_result,
            processing_time_ms=0,  # filled by caller
        )

    # ── Demo mode ─────────────────────────────────────────────────────────────

    def _demo_predict(self, image_id: str) -> PredictionResponse:
        """Return realistic mock predictions for demo/testing purposes."""
        # Pick a random plant + matching disease for the demo
        demo_scenarios = [
            ("Tomato", "Early Blight", 0.87, False, 0.94),
            ("Tomato", "Healthy", 0.99, True, 0.91),
            ("Potato", "Late Blight", 0.91, False, 0.89),
            ("Apple", "Apple Scab", 0.78, False, 0.93),
            ("Corn (Maize)", "Common Rust", 0.83, False, 0.88),
            ("Grape", "Black Rot", 0.76, False, 0.85),
            ("Tomato", "Bacterial Spot", 0.82, False, 0.90),
            ("Strawberry", "Healthy", 0.97, True, 0.93),
        ]
        plant_name, disease_name, disease_conf, is_healthy, species_conf = random.choice(demo_scenarios)

        plant_result = self._build_plant_result(plant_name, species_conf)
        disease_result = self._build_disease_result(disease_name, disease_conf, is_healthy)

        return PredictionResponse(
            image_id=image_id,
            plant=plant_result,
            disease=disease_result,
            processing_time_ms=0,
        )

    # ── Builders ──────────────────────────────────────────────────────────────

    def _build_plant_result(self, plant_name: str, confidence: float) -> PlantResult:
        meta = PLANT_METADATA.get(
            plant_name,
            {
                "scientific_name": "Unknown species",
                "family": "Unknown",
                "common_names": [plant_name],
                "description": "Plant information not available in database.",
                "uses": [],
                "growing_conditions": "Information not available.",
                "interesting_facts": [],
                "origin": "Unknown",
                "season": "Unknown",
            },
        )
        return PlantResult(
            name=plant_name,
            scientific_name=meta["scientific_name"],
            family=meta.get("family", "Unknown"),
            confidence=round(confidence, 4),
            description=meta["description"],
            common_names=meta["common_names"],
            uses=meta["uses"],
            growing_conditions=meta["growing_conditions"],
            interesting_facts=meta["interesting_facts"],
            origin=meta.get("origin", "Unknown"),
            season=meta.get("season", "Unknown"),
        )

    def _build_disease_result(
        self, disease_name: str, confidence: float, is_healthy: bool
    ) -> DiseaseResult:
        meta = DISEASE_METADATA.get(
            disease_name,
            DISEASE_METADATA.get(
                "Healthy",
                {
                    "severity": "unknown",
                    "description": "Disease information not available.",
                    "pathogen": "Unknown",
                    "causes": [],
                    "prevention": [],
                    "treatment": [],
                },
            ),
        )
        return DiseaseResult(
            detected=not is_healthy,
            name=disease_name,
            confidence=round(confidence, 4),
            severity=meta.get("severity", "unknown"),
            pathogen=meta.get("pathogen", "Unknown"),
            description=meta["description"],
            causes=meta.get("causes", []),
            prevention=meta.get("prevention", []),
            treatment=meta.get("treatment", []),
        )

    # ── Preprocessing ─────────────────────────────────────────────────────────

    @staticmethod
    def _preprocess(image: Image.Image) -> np.ndarray:
        """Resize, normalize, and convert PIL image to ONNX-ready float32 tensor."""
        image = image.convert("RGB").resize((INPUT_SIZE, INPUT_SIZE), Image.LANCZOS)
        arr = np.array(image, dtype=np.float32) / 255.0
        arr = (arr - IMAGENET_MEAN) / IMAGENET_STD
        # HWC → CHW → NCHW
        arr = arr.transpose(2, 0, 1)[np.newaxis, ...]
        return arr.astype(np.float32)

    @staticmethod
    def _softmax(logits: np.ndarray) -> np.ndarray:
        e = np.exp(logits - np.max(logits))
        return e / e.sum()
