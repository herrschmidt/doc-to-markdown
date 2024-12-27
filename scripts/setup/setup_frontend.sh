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
echo "cd frontend/src && python3 -m http.server 8000 --bind 0.0.0.0"