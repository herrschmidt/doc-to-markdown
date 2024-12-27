# Stage 1: Build frontend assets
FROM node:20-slim AS builder

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend code
COPY frontend/src ./src

# Build frontend assets (if needed)
# RUN npm run build

# Stage 2: Final image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy built assets from builder stage
COPY --from=builder /app/src ./src

# Copy entrypoint script
COPY docker/frontend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user
RUN useradd -m -u 1000 frontend
USER frontend

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/index.html || exit 1

# Start server
ENTRYPOINT ["/entrypoint.sh"]