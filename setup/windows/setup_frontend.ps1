# Stop on error
$ErrorActionPreference = "Stop"

# Navigate to frontend directory
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$SCRIPT_DIR\..\..\frontend"

# Install dependencies
Write-Host "Installing frontend dependencies..."
npm install

# Create necessary directories
New-Item -ItemType Directory -Force -Path src/styles | Out-Null
New-Item -ItemType Directory -Force -Path public | Out-Null

# Copy static assets if they exist
if (Test-Path "../assets") {
    Write-Host "Copying static assets..."
    Copy-Item -Path "../assets/*" -Destination "public/" -Recurse -Force
}

Write-Host "Frontend setup complete!"
Write-Host "To start the development server:"
Write-Host "cd frontend/src; python -m http.server 8000 --bind 0.0.0.0"