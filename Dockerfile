# =========================
# Builder stage
# =========================
FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# =========================
# Runtime stage
# =========================
FROM python:3.13-slim AS runtime

WORKDIR /app

# Only copy installed packages & needed binaries
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Only copy application code
COPY --from=builder /app/ /app

# Clean up unnecessary Python files (optional)
RUN find /usr/local/lib/python3.13/site-packages -name '*.pyc' -delete \
    && find /usr/local/lib/python3.13/site-packages -name '*.pyo' -delete \
    && find /usr/local/lib/python3.13/site-packages -name '__pycache__' -type d -exec rm -r {} + \
    && rm -rf /root/.cache

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
