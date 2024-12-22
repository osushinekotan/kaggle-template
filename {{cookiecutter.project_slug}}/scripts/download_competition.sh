#!/bin/bash
set -e
uv run python src/download.py competition_download || { echo "Kaggle push failed"; exit 1; }
