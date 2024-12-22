#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Error: Experiment name is required."
  exit 1
fi

echo "Uploading codes..."
uv run python src/upload.py codes

echo "Uploading artifacts for experiment: $1"
uv run python src/upload.py artifacts --exp_name "$1"
