# syntax=docker/dockerfile:1

# ---- Stage 1: Builder ----
FROM node:20-slim AS builder

WORKDIR /build

COPY package*.json ./
RUN npm ci --omit=dev

# ---- Stage 2: Runtime ----
FROM node:20-slim AS runtime

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

COPY --from=builder /build/node_modules ./node_modules
COPY app.js .
COPY views/ ./views/

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/healthz', r => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

CMD ["node", "app.js"]
