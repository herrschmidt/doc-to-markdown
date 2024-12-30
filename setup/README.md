# Setup Scripts

This directory contains setup scripts for both Unix-like systems (Linux, macOS) and Windows.

## Prerequisites

- Python 3.12 or later
- Node.js 20 or later
- npm 10 or later

## Unix-like Systems (Linux, macOS)

Run the setup script:
```bash
# Make scripts executable
chmod +x setup/unix/*.sh

# Run setup
./setup/unix/setup_all.sh
```

## Windows

Run the setup script in PowerShell:
```powershell
# Allow script execution (if not already enabled)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run setup
.\setup\windows\setup_all.ps1
```

## What the Scripts Do

1. Frontend Setup:
   - Install Node.js dependencies
   - Create necessary directories
   - Copy static assets (if any)

2. Backend Setup:
   - Create Python virtual environment
   - Install Python dependencies
   - Create necessary directories
   - Set up temporary upload directory

## Docker Setup (Alternative)

If you prefer using Docker, you can skip these scripts and use Docker Compose instead:

```bash
# Development mode with hot reload
docker compose -f docker/docker-compose.dev.yml up -d

# OR Production mode
docker compose -f docker/docker-compose.yml up -d
```

## Troubleshooting

### Windows
- If script execution is blocked, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell as Administrator
- If Python venv fails, make sure Python is in your PATH
- If npm install fails, make sure Node.js is in your PATH

### Unix-like Systems
- If scripts aren't executable, run `chmod +x setup/unix/*.sh`
- If Python venv fails, install python3-venv package
- If npm install fails, make sure Node.js and npm are installed