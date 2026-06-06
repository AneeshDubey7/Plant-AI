FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    torch==2.3.0+cpu \
    torchvision==0.18.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    fastapi==0.111.0 \
    "uvicorn[standard]==0.29.0" \
    python-multipart==0.0.9 \
    pydantic==2.7.1 \
    pydantic-settings==2.2.1 \
    onnxruntime==1.18.0 \
    Pillow==10.3.0 \
    numpy==1.26.4 \
    python-dotenv==1.0.1 \
    httpx==0.27.0 \
    aiofiles==23.2.1 \
    loguru==0.7.2

COPY . .

RUN mkdir -p logs models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]