# 🌿 Plant Disease Prediction System

A production-ready, AI-powered web application that identifies plant species and detects diseases from leaf images using a two-stage deep learning pipeline.

---

## 🏗️ Architecture Overview

```
plant-disease-system/
├── backend/          # FastAPI REST API + ML inference
├── frontend/         # React + Tailwind CSS UI
├── ml/               # Model training scripts & notebooks
└── docs/             # Deployment guides & API docs
```

**Tech Stack:**
- **ML**: PyTorch + EfficientNet-B3 (Transfer Learning)
- **Backend**: FastAPI + Python 3.10
- **Frontend**: React 18 + Tailwind CSS + Vite
- **Containerization**: Docker + Docker Compose
- **Deployment**: Render (backend) + Vercel (frontend)

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)

### 1. Clone the repo
```bash
git clone https://github.com/yourname/plant-disease-system.git
cd plant-disease-system
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download pretrained weights (first run)
python app/core/download_weights.py

# Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local → set VITE_API_URL=http://localhost:8000
npm run dev
```

Open http://localhost:5173

### 4. Docker (Full Stack)
```bash
docker-compose up --build
```
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🧠 ML Pipeline

### Training the Models

```bash
cd ml

# 1. Download PlantVillage dataset
python scripts/download_dataset.py

# 2. Preprocess & augment data
python scripts/preprocess.py

# 3. Train Plant Species Classifier (Stage 1)
python scripts/train_species.py --epochs 30 --batch-size 32

# 4. Train Disease Classifier (Stage 2)
python scripts/train_disease.py --epochs 30 --batch-size 32

# 5. Export to ONNX for efficient inference
python scripts/export_onnx.py
```

### Model Architecture
- **Stage 1 (Species)**: EfficientNet-B3, fine-tuned on 38-class plant dataset
- **Stage 2 (Disease)**: EfficientNet-B3, fine-tuned on PlantVillage (38 disease classes)
- **Inference**: ONNX Runtime for 3-5x speedup vs PyTorch

### Datasets
| Dataset | Classes | Images | Usage |
|---------|---------|--------|-------|
| PlantVillage | 38 | ~87,000 | Disease detection |
| iNaturalist (subset) | 50+ | ~120,000 | Species ID |

---

## 📡 API Reference

### `POST /api/v1/predict`
Upload a plant image for analysis.

**Request:** `multipart/form-data` with field `file` (JPEG/PNG, max 10MB)

**Response:**
```json
{
  "plant": {
    "name": "Tomato",
    "scientific_name": "Solanum lycopersicum",
    "confidence": 0.94,
    "description": "...",
    "uses": ["culinary", "medicinal"],
    "growing_conditions": "...",
    "interesting_facts": ["..."]
  },
  "disease": {
    "detected": true,
    "name": "Early Blight",
    "confidence": 0.87,
    "severity": "moderate",
    "description": "...",
    "causes": ["..."],
    "prevention": ["..."],
    "treatment": ["..."]
  },
  "image_id": "uuid-here",
  "processing_time_ms": 342
}
```

### `GET /api/v1/plant-info/{plant_name}`
Get detailed info for a plant species.

### `GET /api/v1/history`
Retrieve prediction history (session-based).

### `GET /api/v1/health`
Health check endpoint.

---

## ☁️ Deployment

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for full step-by-step guides for:
- Render (backend)
- Vercel (frontend)
- AWS ECS + CloudFront
- GCP Cloud Run

---

## 📊 Model Performance

| Model | Accuracy | F1-Score | Inference Time |
|-------|----------|----------|----------------|
| Species (EfficientNet-B3) | 94.2% | 0.941 | ~120ms |
| Disease (EfficientNet-B3) | 97.1% | 0.969 | ~130ms |

---

## 🗂️ Environment Variables

### Backend (`backend/.env`)
```
MODEL_SPECIES_PATH=models/species_efficientnet_b3.onnx
MODEL_DISEASE_PATH=models/disease_efficientnet_b3.onnx
MAX_IMAGE_SIZE_MB=10
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
```

### Frontend (`frontend/.env.local`)
```
VITE_API_URL=http://localhost:8000
VITE_MAX_FILE_SIZE_MB=10
```

---

## 📄 License
MIT License — see [LICENSE](LICENSE)
