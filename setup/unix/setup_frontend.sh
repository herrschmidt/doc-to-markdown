#!/bin/bash

# Exit on error
set -e

# Navigate to frontend directory
cd "$(dirname "$0")/../../frontend"

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