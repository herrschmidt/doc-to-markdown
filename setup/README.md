# Setup Scripts

This directory contains setup scripts for Unix-like systems (Linux, macOS).

## Prerequisites

- Python 3.12 or later
- Node.js 20 or later
- npm 10 or later

## Setup Instructions

Run the setup script:
```bash
# Make scripts executable
chmod +x setup/unix/*.sh

# Run setup
./setup/unix/setup_all.sh
```

### Starting the Servers

After setup, you can start the servers in two ways:

#### 1. Regular Mode (Blocks Terminal)
This mode will block your terminal, and you'll need separate terminals for frontend and backend:
```bash
# Start backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8001 --host 0.0.0.0

# Start frontend (in another terminal)
cd frontend/src && python3 -m http.server 8000 --bind 0.0.0.0
```

#### 2. Background Mode
This mode runs the servers in the background, not blocking your terminal:
```bash
# Start backend
cd backend && source venv/bin/activate && nohup uvicorn app.main:app --reload --port 8001 --host 0.0.0.0 > backend.log 2>&1 &

# Start frontend
nohup python3 -m http.server 8000 --bind 0.0.0.0 --directory frontend/src > frontend.log 2>&1 &
```

> **Note:** When copying commands from the setup script output, make sure not to include any surrounding quotes that might be part of the echo statements.

Monitor the background processes:
```bash
# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log

# Find running processes
ps aux | grep uvicorn    # For backend
ps aux | grep "http.server"  # For frontend
```

### Stopping the Servers

#### Regular Mode
If running in regular mode, simply press `Ctrl+C` in each terminal window to stop the servers.

#### Background Mode
If running in background mode, you can stop the servers using one of these methods:

1. Using process ID:
```bash
# Find the process IDs
ps aux | grep uvicorn    # For backend
ps aux | grep "http.server"  # For frontend

# Kill the processes (replace XXXX with actual process ID)
kill XXXX  # Graceful shutdown
# or
kill -9 XXXX  # Force shutdown if graceful shutdown doesn't work
```

2. Using pkill (easier):
```bash
# Stop backend
pkill -f uvicorn

# Stop frontend
pkill -f "python3 -m http.server"
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

### Unix-like Systems
- If scripts aren't executable, run `chmod +x setup/unix/*.sh`
- If Python venv fails, install python3-venv package
- If npm install fails, make sure Node.js and npm are installed