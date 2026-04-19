#!/usr/bin/env bash
# Build script for Vercel static deployment.
# Runs the analytics pipeline and assembles the public/ output directory.
set -euo pipefail

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Running analytics pipeline..."
python scripts/run_pipeline.py

echo "==> Assembling static site..."
python scripts/build_site.py

echo "==> Build complete. Output is in public/"
