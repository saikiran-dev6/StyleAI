#!/usr/bin/env bash
set -euo pipefail

TARGET_URL="${1:-http://localhost:8080}"

echo "==> Running post-deploy smoke tests against: ${TARGET_URL}"

# 1. Healthz check
echo "==> [1/3] Checking /healthz endpoint..."
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}/healthz")
if [ "${HEALTH_STATUS}" -ne 200 ]; then
    echo "ERROR: Health check failed with status code ${HEALTH_STATUS}"
    exit 1
fi
echo "✓ Healthz check passed."

# 2. Readyz check
echo "==> [2/3] Checking /readyz endpoint..."
READY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}/readyz")
if [ "${READY_STATUS}" -ne 200 ]; then
    echo "ERROR: Readiness check failed with status code ${READY_STATUS}"
    exit 1
fi
echo "✓ Readyz check passed."

# 3. Version check
echo "==> [3/3] Checking /version endpoint..."
VERSION_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${TARGET_URL}/version")
if [ "${VERSION_STATUS}" -ne 200 ]; then
    echo "ERROR: Version check failed with status code ${VERSION_STATUS}"
    exit 1
fi
echo "✓ Version check passed."

echo "==> All post-deploy smoke tests PASSED successfully!"
