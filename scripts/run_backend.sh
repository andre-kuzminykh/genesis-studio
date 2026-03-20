#!/bin/bash
# Run the Genesis Studio backend server
set -e
cd "$(dirname "$0")/.."
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
