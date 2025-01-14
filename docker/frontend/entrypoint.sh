#!/bin/bash

# Exit on error
set -e

# Create config file with API key
# Read backend URL from .env file
MARKDOWN_BACKEND_URL=$(grep MARKDOWN_BACKEND_URL /app/.env | cut -d '=' -f2 | tr -d '\r' | sed -e 's/[[:space:]]*$//')

# Create config file with API key and backend URL
echo "window.MARKDOWN_CONFIG = {
  apiKey: '$MARKDOWN_API_KEY',
  backendUrl: '$MARKDOWN_BACKEND_URL'
};" > /app/src/config.js

# Start Python HTTP server
cd /app/src
python3 -m http.server 8000 --bind 0.0.0.0