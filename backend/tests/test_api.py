"""
tests/test_api.py — FastAPI endpoint tests using httpx AsyncClient.

Run with:
    cd backend
    pytest tests/ -v
"""

import io
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_test_image(fmt="JPEG", size=(224, 224), color=(80, 160, 80)) -> bytes:
    """Create a small in-memory image for upload tests."""
    img = Image.new("RGB", size, color)
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.read()


def mock_prediction_response():
    """Return a minimal valid PredictionResponse dict."""
    return {
        "image_id": "test-uuid-1234",
        "plant": {
            "name": "Tomato",
            "scientific_name": "Solanum lycopersicum",
            "family": "Solanaceae",
            "confidence": 0.94,
            "description": "A fruiting plant.",
            "common_names": ["Tomato"],
            "uses": ["Culinary"],
            "growing_conditions": "Full sun.",
            "interesting_facts": ["Botanically a fruit."],
            "origin": "South America",
            "season": "Summer",
        },
        "disease": {
            "detected": True,
            "name": "Early Blight",
            "confidence": 0.87,
            "severity": "moderate",
            "pathogen": "Alternaria solani",
            "description": "A fungal disease.",
            "causes": ["Warm humid weather"],
            "prevention": ["Crop rotation"],
            "treatment": ["Copper fungicide"],
        },
        "processing_time_ms": 250.0,
        "model_versions": {"species": "v1", "disease": "v1"},
    }


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    """Synchronous test client with mock model service pre-loaded."""
    mock_svc = MagicMock()
    mock_svc.demo_mode = True
    mock_svc.predict = AsyncMock(return_value=MagicMock(
        **mock_prediction_response(),
        model_dump=lambda: mock_prediction_response()
    ))

    with TestClient(app) as c:
        app.state.model_service = mock_svc
        yield c


# ── Root ──────────────────────────────────────────────────────────────────────

def test_root_returns_service_info(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["service"] == "Plant Disease Prediction API"
    assert data["status"] == "healthy"


# ── Health ────────────────────────────────────────────────────────────────────

def test_health_check_returns_status(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "models_loaded" in data


# ── Predict ───────────────────────────────────────────────────────────────────

def test_predict_valid_jpeg(client):
    img_bytes = make_test_image("JPEG")
    resp = client.post(
        "/api/v1/predict",
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")},
    )
    assert resp.status_code == 200


def test_predict_valid_png(client):
    img_bytes = make_test_image("PNG")
    resp = client.post(
        "/api/v1/predict",
        files={"file": ("leaf.png", img_bytes, "image/png")},
    )
    assert resp.status_code == 200


def test_predict_rejects_non_image(client):
    resp = client.post(
        "/api/v1/predict",
        files={"file": ("file.pdf", b"%PDF-1.4 fake content", "application/pdf")},
    )
    assert resp.status_code == 415


def test_predict_rejects_oversized_file(client):
    # Create a fake large payload that exceeds 10 MB
    large_data = b"x" * (11 * 1024 * 1024)
    resp = client.post(
        "/api/v1/predict",
        files={"file": ("big.jpg", large_data, "image/jpeg")},
    )
    assert resp.status_code == 413


def test_predict_rejects_corrupt_image(client):
    resp = client.post(
        "/api/v1/predict",
        files={"file": ("corrupt.jpg", b"\xFF\xD8 not a real jpeg body", "image/jpeg")},
    )
    assert resp.status_code == 422


def test_predict_requires_file_field(client):
    resp = client.post("/api/v1/predict")
    assert resp.status_code == 422


# ── Plant info ────────────────────────────────────────────────────────────────

def test_get_plant_info_tomato(client):
    resp = client.get("/api/v1/plant-info/Tomato")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Tomato"
    assert "scientific_name" in data
    assert "known_diseases" in data
    assert isinstance(data["known_diseases"], list)


def test_get_plant_info_case_insensitive(client):
    resp = client.get("/api/v1/plant-info/tomato")
    assert resp.status_code == 200


def test_get_plant_info_unknown_plant(client):
    resp = client.get("/api/v1/plant-info/MarsPlant9000")
    assert resp.status_code == 404
    assert "MarsPlant9000" in resp.json()["detail"]


def test_list_plants_returns_all(client):
    resp = client.get("/api/v1/plants")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] > 0
    assert "Tomato" in data["plants"]
    assert "Potato" in data["plants"]
