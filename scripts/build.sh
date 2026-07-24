#!/usr/bin/env bash
set -euo pipefail

IMAGE_TAG="${1:-styleai-web:latest}"

echo "==> Building production Docker image: ${IMAGE_TAG}"
docker build -t "${IMAGE_TAG}" -f Dockerfile .
echo "==> Docker image built successfully."
