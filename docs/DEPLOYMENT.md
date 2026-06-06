# 🚀 Deployment Guide — Plant Disease Prediction System

This guide covers three deployment paths:
- **Option A** — Render (backend) + Vercel (frontend) — *Recommended for beginners*
- **Option B** — Docker on a VPS / AWS EC2
- **Option C** — AWS ECS + CloudFront (production-grade)

---

## 📋 Pre-deployment Checklist

Before deploying, ensure you have:
- [ ] Trained ONNX model files (`species_efficientnet_b3.onnx`, `disease_efficientnet_b3.onnx`)
- [ ] Backend `.env` filled in (copy from `.env.example`)
- [ ] Frontend `.env.local` set with the correct `VITE_API_URL`
- [ ] All tests passing: `cd backend && pytest tests/ -v`

---

## Option A — Render + Vercel (Free Tier Friendly)

### Step 1 — Deploy Backend on Render

1. Push your code to GitHub.

2. Go to [render.com](https://render.com) → **New** → **Web Service**

3. Connect your GitHub repo. Configure:

   | Field | Value |
   |---|---|
   | **Name** | `plantai-backend` |
   | **Root Directory** | `backend` |
   | **Runtime** | `Docker` |
   | **Dockerfile Path** | `./Dockerfile` |
   | **Plan** | Starter ($7/mo) or Free |

4. Add Environment Variables in Render dashboard:
   ```
   MODEL_SPECIES_PATH=models/species_efficientnet_b3.onnx
   MODEL_DISEASE_PATH=models/disease_efficientnet_b3.onnx
   LOG_LEVEL=INFO
   CORS_ORIGINS=["https://your-app.vercel.app"]
   ```

5. **Upload model files** — Since Render doesn't support large file uploads directly,
   use one of these approaches:
   - **Render Disk** (paid): Mount a persistent disk at `/app/models`
   - **Hugging Face Hub** (free): Upload models to HF Hub, download at startup
   - **AWS S3**: Store models in S3, download on container start

   Add a startup download script (`backend/app/core/download_weights.py`):
   ```python
   import os, urllib.request
   from pathlib import Path

   MODELS = {
       "models/species_efficientnet_b3.onnx": os.environ.get("SPECIES_MODEL_URL", ""),
       "models/disease_efficientnet_b3.onnx": os.environ.get("DISEASE_MODEL_URL", ""),
   }

   for path, url in MODELS.items():
       if url and not Path(path).exists():
           print(f"Downloading {path}...")
           urllib.request.urlretrieve(url, path)
           print(f"Downloaded {path}")
   ```

6. Your backend URL will be: `https://plantai-backend.onrender.com`

> ⚠️ **Free tier note**: Render free instances spin down after 15 min inactivity.
> First request after sleep takes ~30s. Upgrade to Starter to avoid this.

---

### Step 2 — Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**

2. Import your GitHub repo. Configure:

   | Field | Value |
   |---|---|
   | **Framework Preset** | `Vite` |
   | **Root Directory** | `frontend` |
   | **Build Command** | `npm run build` |
   | **Output Directory** | `dist` |

3. Add Environment Variable:
   ```
   VITE_API_URL = https://plantai-backend.onrender.com
   ```

4. Click **Deploy**. Your app will be live at `https://your-app.vercel.app`

5. Go back to Render → update `CORS_ORIGINS` with your Vercel URL.

---

## Option B — Docker on VPS / AWS EC2

### Step 1 — Provision a server

- **AWS EC2**: `t3.medium` (2 vCPU, 4 GB RAM) — minimum for ONNX inference
- **DigitalOcean**: `s-2vcpu-4gb` droplet
- **Hetzner**: `CX21` (cheapest in Europe)

### Step 2 — Install Docker

```bash
# Ubuntu 22.04
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### Step 3 — Clone and configure

```bash
git clone https://github.com/yourname/plant-disease-system.git
cd plant-disease-system

# Copy model files to backend/models/
mkdir -p backend/models
scp your-local-machine:path/to/models/*.onnx backend/models/

# Set environment
cp backend/.env.example backend/.env
nano backend/.env   # Set CORS_ORIGINS to your domain
```

### Step 4 — Build and launch

```bash
docker-compose up --build -d

# Verify running
docker-compose ps
docker-compose logs -f backend
```

### Step 5 — Set up nginx reverse proxy + SSL

```bash
sudo apt install nginx certbot python3-certbot-nginx

# Create nginx site config
sudo nano /etc/nginx/sites-available/plantai
```

```nginx
server {
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 15M;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/plantai /etc/nginx/sites-enabled/
sudo certbot --nginx -d api.yourdomain.com
sudo systemctl reload nginx
```

---

## Option C — AWS ECS + CloudFront

### Architecture

```
Users → CloudFront CDN → S3 (Frontend)
                       → ALB → ECS Fargate (Backend API)
                                     → EFS (Model files)
```

### Steps

#### 1. Push Docker images to ECR

```bash
# Authenticate
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.ap-south-1.amazonaws.com

# Build and push backend
docker build -t plantai-backend ./backend
docker tag plantai-backend:latest 123456789.dkr.ecr.ap-south-1.amazonaws.com/plantai-backend:latest
docker push 123456789.dkr.ecr.ap-south-1.amazonaws.com/plantai-backend:latest
```

#### 2. Create ECS Cluster + Task Definition

```bash
# Using AWS CLI
aws ecs create-cluster --cluster-name plantai-cluster

# Task definition (see docs/ecs-task-definition.json for full template)
aws ecs register-task-definition --cli-input-json file://docs/ecs-task-definition.json
```

#### 3. Create EFS for model storage

```bash
aws efs create-file-system --creation-token plantai-models
# Mount in ECS task definition at /app/models
```

#### 4. Deploy frontend to S3 + CloudFront

```bash
cd frontend
npm run build

# Sync to S3
aws s3 sync dist/ s3://your-plantai-bucket --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DIST_ID \
  --paths "/*"
```

---

## 🔄 CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.10" }
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest tests/ -v

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Render
        run: |
          curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: cd frontend && npm ci && npm run build
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
```

---

## 🔒 Production Security Checklist

- [ ] Set `DEBUG=false` in backend `.env`
- [ ] Use HTTPS everywhere (Certbot / Vercel handles this)
- [ ] Restrict `CORS_ORIGINS` to your exact frontend domain
- [ ] Set `MAX_IMAGE_SIZE_MB=10` (already default)
- [ ] Enable rate limiting (configured in `app/core/config.py`)
- [ ] Store secrets in environment variables — never commit `.env`
- [ ] Use non-root Docker user (already done in Dockerfile)
- [ ] Keep `onnxruntime` updated for security patches

---

## 📊 Scaling Considerations

| Traffic Level | Recommended Setup |
|---|---|
| < 1,000 req/day | Render Starter + Vercel Free |
| 1,000–50,000 req/day | ECS Fargate (1 vCPU, 2 GB) × 2 tasks |
| > 50,000 req/day | GPU inference (AWS g4dn.xlarge) + model caching |

**Model optimization tips for high traffic:**
- Use `onnxruntime` with `graph_optimization_level = ORT_ENABLE_ALL` (already configured)
- Quantize ONNX models to INT8: `python ml/scripts/quantize_onnx.py`
- Cache predictions by image hash (Redis) for identical uploads
- Use async batch inference for throughput

---

## 🆘 Troubleshooting

| Symptom | Fix |
|---|---|
| `503 Service Unavailable` on `/predict` | Models not loaded — check `GET /api/v1/health` and model file paths |
| `413 Request Entity Too Large` | Nginx `client_max_body_size` too small — set to `15M` |
| CORS errors in browser | `CORS_ORIGINS` env var doesn't include your frontend URL |
| Slow first prediction (>5s) | Cold start — upgrade from free tier or use keep-alive pings |
| `demo_mode: true` in health check | ONNX model files missing from `backend/models/` |
| Frontend shows blank page | Check `VITE_API_URL` is set correctly and backend is reachable |
