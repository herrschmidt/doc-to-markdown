# Use Python slim image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./app

# Create upload directory
RUN mkdir -p /tmp/doc-to-markdown && chmod 777 /tmp/doc-to-markdown

# Copy entrypoint script
COPY docker/backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user
RUN useradd -m -u 1000 backend
USER backend

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8001/api/health || exit 1

# Start server
ENTRYPOINT ["/entrypoint.sh"]