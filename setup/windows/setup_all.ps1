# Stop on error
$ErrorActionPreference = "Stop"

# Get the directory of this script
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Run frontend setup
Write-Host "Setting up frontend..."
& "$SCRIPT_DIR\setup_frontend.ps1"

# Run backend setup
Write-Host "`nSetting up backend..."
& "$SCRIPT_DIR\setup_backend.ps1"

Write-Host "`nSetup complete!"
Write-Host "To start both servers:"
Write-Host "1. Start backend: cd backend; uvicorn app.main:app --reload --port 8001 --host 0.0.0.0"
Write-Host "2. Start frontend: cd frontend/src; python -m http.server 8000 --bind 0.0.0.0"