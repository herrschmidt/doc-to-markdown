#!/bin/bash

# Exit on error
set -e

# Get the project root directory
PROJECT_ROOT="/workspace/magic-markdown"

# Navigate to frontend directory
cd "$PROJECT_ROOT/frontend"

# Check for .env file
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "Reading environment variables from .env file..."
    API_KEY=$(grep MARKDOWN_API_KEY "$PROJECT_ROOT/.env" | cut -d '=' -f2 | tr -d '\r' | sed -e 's/[[:space:]]*$//')
    RATE_LIMIT=$(grep MARKDOWN_RATE_LIMIT_PER_MINUTE "$PROJECT_ROOT/.env" | cut -d '=' -f2 | tr -d '\r' | sed -e 's/[[:space:]]*$//')
else
    echo "Error: .env file not found. Please create a .env file with:"
    echo "MARKDOWN_API_KEY=your_api_key_here"
    echo "MARKDOWN_RATE_LIMIT_PER_MINUTE=60"
    exit 1
fi

# Create config.js with all variables
echo "window.MARKDOWN_CONFIG = {
  apiKey: '$API_KEY',
  rateLimit: $RATE_LIMIT
};" > src/config.js

echo "Updated config.js with environment variables"

# Verify the file is created correctly
if [ $(wc -l < src/config.js) -lt 3 ]; then
    echo "Error: config.js is incomplete. Please check your setup."
    cat src/config.js
    exit 1
fi

# Install dependencies
echo "Installing frontend dependencies..."
npm install

# Create necessary directories
mkdir -p src/styles
mkdir -p public

# Copy static assets if they exist
if [ -d "../assets" ]; then
    echo "Copying static assets..."
    cp -r ../assets/* public/
fi

echo "Frontend setup complete!"
echo "To start the development server:"
echo "1. Regular mode (blocks terminal):"
echo "   cd frontend/src && python3 -m http.server 8000 --bind 0.0.0.0"
echo ""
echo "2. Background mode (doesn't block terminal):"
echo "   nohup python3 -m http.server 8000 --bind 0.0.0.0 --directory frontend/src > frontend.log 2>&1 &"
echo "   # View logs with: tail -f frontend.log"
echo "   # Find process with: ps aux | grep 'http.server'"
echo ""
echo "To stop the server:"
echo "- If running in regular mode: press Ctrl+C"
echo "- If running in background mode:"
echo "  * Easy method: pkill -f 'http.server'"
echo "  * Alternative: ps aux | grep 'http.server' (to find PID) then kill PID"
