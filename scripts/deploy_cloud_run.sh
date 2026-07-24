#!/usr/bin/env bash
set -euo pipefail

GCP_PROJECT_ID="${GCP_PROJECT_ID:-my-gcp-project}"
GCP_REGION="${GCP_REGION:-asia-south1}"
ARTIFACT_REGISTRY_REPO="${ARTIFACT_REGISTRY_REPO:-styleai}"
CLOUD_RUN_SERVICE="${CLOUD_RUN_SERVICE:-styleai-web}"
GIT_SHA="${GIT_SHA:-$(git rev-parse --short HEAD 2>/dev/null || echo 'manual')}"
IMAGE_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${ARTIFACT_REGISTRY_REPO}/${CLOUD_RUN_SERVICE}:${GIT_SHA}"

echo "==> Deploying StyleAI to Google Cloud Run..."
echo "    Project: ${GCP_PROJECT_ID}"
echo "    Region: ${GCP_REGION}"
echo "    Service: ${CLOUD_RUN_SERVICE}"
echo "    Image: ${IMAGE_URI}"

# 1. Build and tag
docker build -t "${IMAGE_URI}" .

# 2. Push to Artifact Registry
gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet || true
docker push "${IMAGE_URI}"

# 3. Deploy to Cloud Run
gcloud run deploy "${CLOUD_RUN_SERVICE}" \
    --image="${IMAGE_URI}" \
    --region="${GCP_REGION}" \
    --platform=managed \
    --allow-unauthenticated \
    --port=8080 \
    --set-env-vars="FLASK_ENV=production,LOG_LEVEL=INFO,GROQ_MODEL=llama-3.3-70b-versatile" \
    --revision-suffix="${GIT_SHA}" \
    --quiet

# Fetch deployed URL
SERVICE_URL=$(gcloud run services describe "${CLOUD_RUN_SERVICE}" --region="${GCP_REGION}" --format='value(status.url)')
echo "==> Deployment complete. Deployed URL: ${SERVICE_URL}"

# Execute post-deploy smoke test
bash scripts/smoke_test.sh "${SERVICE_URL}" || {
    echo "CRITICAL: Smoke test failed on new revision! Triggering automatic rollback..."
    bash scripts/rollback_cloud_run.sh
    exit 1
}
