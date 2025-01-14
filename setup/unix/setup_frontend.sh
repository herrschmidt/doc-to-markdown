#!/bin/bash

# Exit on error
set -e

# Get the project root directory
PROJECT_ROOT="$(dirname "$0")/../.."

# Navigate to frontend directory
cd "$PROJECT_ROOT/frontend"

# Read API key from .env file and create config.js
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "Reading API key from .env file..."
    # Use grep to find the line, cut to get the value after =, 
    # tr to remove carriage returns, and sed to remove trailing whitespace and newlines
    MARKDOWN_API_KEY=$(grep MARKDOWN_API_KEY "$PROJECT_ROOT/.env" | cut -d '=' -f2 | tr -d '\r' | sed -e 's/[[:space:]]*$//')
    
    # Create config.js with the cleaned API key
    echo "window.MARKDOWN_CONFIG = { apiKey: '$MARKDOWN_API_KEY' };" > src/config.js
    echo "Updated config.js with API key"
    
    # Verify the file is created correctly (single line)
    if [ $(wc -l < src/config.js) -ne 1 ]; then
        echo "Warning: config.js contains multiple lines. This might indicate an issue with the API key format."
        echo "Content of config.js:"
        cat src/config.js
    fi
else
    echo "Warning: .env file not found. config.js will have an empty API key."
    echo "window.MARKDOWN_CONFIG = { apiKey: '' };" > src/config.js
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