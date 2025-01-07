#!/bin/bash

# Exit on error
set -e

# Navigate to backend directory
cd "$(dirname "$0")/../../backend"

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing backend dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p app/api/routes
mkdir -p app/core
mkdir -p app/schemas
mkdir -p tests/fixtures

# Create upload directory
mkdir -p /tmp/doc-to-markdown

echo "Backend setup complete!"
echo "To start the development server:"
echo "cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8001 --host 0.0.0.0"
echo "Or step by step:"
echo "1. cd backend"
echo "2. source venv/bin/activate"
echo "3. uvicorn app.main:app --reload --port 8001 --host 0.0.0.0"