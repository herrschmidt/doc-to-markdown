#!/bin/bash

# Exit on error
set -e

# Check for .env file
if [ ! -f "$(dirname "$0")/../../.env" ]; then
    echo "Error: .env file not found. Please create a .env file with:"
    echo "MARKDOWN_API_KEY=your_api_key_here"
    echo "MARKDOWN_RATE_LIMIT_PER_MINUTE=60"
    exit 1
fi

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Navigate to backend directory
cd "$(dirname "$0")/../../backend"

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    uv venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing backend dependencies..."
uv pip install -r requirements.txt

# Create necessary directories
mkdir -p app/api/routes
mkdir -p app/core
mkdir -p app/schemas
mkdir -p tests/fixtures

# Create upload directory
mkdir -p /tmp/doc-to-markdown

echo "Backend setup complete!"
echo "To start the development server:"
echo "1. Regular mode (blocks terminal):"
echo "   # For native Unix systems:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8001 --host 0.0.0.0"
echo ""
echo "   # For WSL on Windows:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8001 --host 0.0.0.0 --forwarded-allow-ips='*'"
echo ""
echo "2. Background mode (doesn't block terminal):"
echo "   # For native Unix systems:"
echo "   cd backend && source venv/bin/activate && nohup uvicorn app.main:app --reload --port 8001 --host 0.0.0.0 > backend.log 2>&1 &"
echo ""
echo "   # For WSL on Windows:"
echo "   cd backend && source venv/bin/activate && nohup uvicorn app.main:app --reload --port 8001 --host 0.0.0.0 --forwarded-allow-ips='*' > backend.log 2>&1 &"
echo ""
echo "   # View logs with: tail -f backend.log"
echo "   # Find process with: ps aux | grep uvicorn"
echo ""
echo "To stop the server:"
echo "- If running in regular mode: press Ctrl+C"
echo "- If running in background mode:"
echo "  * Easy method: pkill -f uvicorn"
echo "  * Alternative: ps aux | grep uvicorn (to find PID) then kill PID"
