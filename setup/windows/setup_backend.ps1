# Stop on error
$ErrorActionPreference = "Stop"

# Navigate to backend directory
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$SCRIPT_DIR\..\..\backend"

# Create Python virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing backend dependencies..."
pip install -r requirements.txt

# Create necessary directories
New-Item -ItemType Directory -Force -Path app/api/routes | Out-Null
New-Item -ItemType Directory -Force -Path app/core | Out-Null
New-Item -ItemType Directory -Force -Path app/schemas | Out-Null
New-Item -ItemType Directory -Force -Path tests/fixtures | Out-Null

# Create upload directory in temp
$TEMP_DIR = [System.IO.Path]::GetTempPath()
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\doc-to-markdown" | Out-Null

Write-Host "Backend setup complete!"
Write-Host "To start the development server:"
Write-Host "cd backend; uvicorn app.main:app --reload --port 8001 --host 0.0.0.0"