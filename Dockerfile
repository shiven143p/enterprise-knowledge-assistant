
FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    API_BASE_URL=http://127.0.0.1:8000 \
    HF_HOME=/app/.cache/huggingface \
    CUDA_VISIBLE_DEVICES=""

ENV PIP_DEFAULT_TIMEOUT=120 \
    PIP_RETRIES=10 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
        
# Install minimal system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Install CPU-only PyTorch
RUN python -m pip install --no-cache-dir \
    torch==2.14.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install application dependencies
COPY requirements.txt .

RUN python -m pip install \
    --no-cache-dir \
    --timeout 120 \
    --retries 10 \
    -r requirements.txt

# Copy application and required model/data files
COPY app/ ./app/
COPY data/ ./data/
COPY models/eka-distilbert-model/ ./models/eka-distilbert-model/
COPY start.sh ./start.sh

# Download embedding model during image build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s \
    --start-period=180s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=5)"

CMD ["sh", "start.sh"]
