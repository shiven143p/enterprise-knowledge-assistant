
#!/bin/sh
set -eu

echo "Starting FastAPI backend..."

python -m uvicorn app.backend.main:app \
    --host 127.0.0.1 \
    --port 8000 &

API_PID=$!

cleanup() {
    kill "$API_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

echo "Waiting for FastAPI..."

python - <<'PY'
import time
import urllib.request

url = "http://127.0.0.1:8000/api/health"

for attempt in range(60):
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if response.status == 200:
                print("FastAPI is ready.")
                break
    except Exception:
        pass

    time.sleep(2)
else:
    raise SystemExit("FastAPI failed to start.")
PY

echo "Starting Streamlit frontend..."

python -m streamlit run app/frontend/streamlit_app.py \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    --server.headless true

