#!/bin/bash

# Exit on error
set -e

# Create config file with API key
echo "window.MARKDOWN_CONFIG = { apiKey: '$MARKDOWN_API_KEY' };" > /app/src/config.js

# Start Python HTTP server
cd /app/src
python3 -m http.server 8000 --bind 0.0.0.0