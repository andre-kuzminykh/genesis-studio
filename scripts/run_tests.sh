#!/bin/bash
# Run all tests for Genesis Studio
set -e
cd "$(dirname "$0")/.."
python -m pytest backend/tests/ bot/tests/ -v --tb=short
