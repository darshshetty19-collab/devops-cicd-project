#!/usr/bin/env bash
# ==============================================================================
# Automated GCP Cloud Run Deployment Script for Linux / Bash / Jenkins Agent
# Builds and deploys the containerized Flask application to Cloud Run
# ==============================================================================

set -euo pipefail

SERVICE_NAME="${1:-devops-mini-project}"
REGION="${2:-us-central1}"

echo "=========================================================="
echo " Google Cloud Platform Deployment (Cloud Run Serverless)  "
echo "=========================================================="

# 1. Verify gcloud CLI
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI is not installed or not in PATH."
    echo "Install Google Cloud SDK from: https://cloud.google.com/sdk/docs/install"
    echo "Alternative: Run directly in browser via Google Cloud Shell (https://shell.cloud.google.com)"
    exit 1
fi

# 2. Check active GCP project
PROJECT=$(gcloud config get-value project 2>/dev/null || true)
if [ -z "$PROJECT" ] || [ "$PROJECT" = "(unset)" ]; then
    echo "ERROR: No active GCP project configured."
    echo "Run: gcloud auth login && gcloud config set project <PROJECT_ID>"
    exit 1
fi

echo "[+] Target GCP Project: ${PROJECT}"
echo "[+] Target Region:      ${REGION}"
echo "[+] Target Service:     ${SERVICE_NAME}"

# 3. Ensure required GCP APIs are enabled
echo "[+] Enabling required GCP APIs (Cloud Run, Cloud Build, Artifact Registry)..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --quiet || true

# 4. Deploy to Cloud Run
echo "[+] Submitting source and deploying container to Cloud Run..."
echo "    Configuration: Min instances: 0 | Max instances: 1 | Memory: 256Mi | Port: 5000"
gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --region "${REGION}" \
    --port 5000 \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 1 \
    --memory 256Mi \
    --cpu 1 \
    --quiet

# 5. Retrieve Live URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format 'value(status.url)')

echo ""
echo "=========================================================="
echo "               DEPLOYMENT SUCCESSFUL!                     "
echo "=========================================================="
echo "Live Web Application URL: ${SERVICE_URL}"
echo "Health Check Endpoint:    ${SERVICE_URL}/health"
echo "API Info Endpoint:        ${SERVICE_URL}/api/info"
echo "=========================================================="

# 6. Verify live endpoint
echo "[+] Verifying live health endpoint..."
curl -f "${SERVICE_URL}/health" || (echo "Health verification failed!" && exit 1)
echo ""
echo "[+] Verification successful!"
