#!/bin/bash

# Exit on error
set -e

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8001