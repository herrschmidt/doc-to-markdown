#!/bin/bash

# Exit on error
set -e

# Get the directory of this script
SCRIPT_DIR="$(dirname "$0")"

# Run frontend setup
echo "Setting up frontend..."
bash "$SCRIPT_DIR/setup_frontend.sh"

# Run backend setup
echo -e "\nSetting up backend..."
bash "$SCRIPT_DIR/setup_backend.sh"

echo -e "\nSetup complete!"
echo "To start both servers:"
echo "1. Start backend: cd backend && uvicorn app.main:app --reload --port 8001 --host 0.0.0.0"
echo "2. Start frontend: cd frontend/src && python3 -m http.server 8000 --bind 0.0.0.0"