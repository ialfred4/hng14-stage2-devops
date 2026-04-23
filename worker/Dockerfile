# syntax=docker/dockerfile:1

# ---- Stage 1: Builder ----
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: Runtime ----
FROM python:3.12-slim AS runtime

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY --from=builder /install /usr/local

COPY worker.py .

USER appuser

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import redis,os; r=redis.Redis(host=os.environ.get('REDIS_HOST','redis'),port=int(os.environ.get('REDIS_PORT',6379)),password=os.environ.get('REDIS_PASSWORD')); r.ping()" || exit 1

CMD ["python", "worker.py"]
