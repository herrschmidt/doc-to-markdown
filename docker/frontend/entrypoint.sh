#!/bin/bash

# Exit on error
set -e

# Start Python HTTP server
cd /app/src
python3 -m http.server 8000 --bind 0.0.0.0