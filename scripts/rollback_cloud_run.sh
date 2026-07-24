#!/usr/bin/env bash
set -euo pipefail

GCP_REGION="${GCP_REGION:-asia-south1}"
CLOUD_RUN_SERVICE="${CLOUD_RUN_SERVICE:-styleai-web}"

echo "==> Initiating Cloud Run rollback for service: ${CLOUD_RUN_SERVICE} in region: ${GCP_REGION}"

# Fetch list of revisions sorted by creation timestamp descending
REVISIONS=$(gcloud run revisions list \
    --service="${CLOUD_RUN_SERVICE}" \
    --region="${GCP_REGION}" \
    --format="value(metadata.name)" \
    --sort-by="~metadata.creationTimestamp")

PREVIOUS_REVISION=$(echo "${REVISIONS}" | sed -n '2p')

if [ -z "${PREVIOUS_REVISION}" ]; then
    echo "ERROR: Could not locate a previous stable revision to rollback to."
    exit 1
fi

echo "==> Restoring 100% traffic to previous revision: ${PREVIOUS_REVISION}"
gcloud run services update-traffic "${CLOUD_RUN_SERVICE}" \
    --region="${GCP_REGION}" \
    --to-revisions="${PREVIOUS_REVISION}=100" \
    --quiet

echo "==> Rollback completed successfully! Traffic reverted to ${PREVIOUS_REVISION}."
