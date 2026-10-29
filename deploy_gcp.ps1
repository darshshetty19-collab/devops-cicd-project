<#
.SYNOPSIS
    Automated GCP Cloud Run Deployment Script for DevOps Mini-Project.
.DESCRIPTION
    Builds and deploys the containerized Flask application to Google Cloud Run
    using the official Google Cloud CLI (gcloud). Uses minimal resources:
    - Zero minimum instances (scales down to 0 when idle)
    - 1 maximum instance cap
    - 256Mi memory allocation
    - 1 vCPU
    Note: Cloud resources remain subject to standard GCP pricing if usage exceeds
    the monthly free tier limits (2 million requests/month on Cloud Run).
#>

[CmdletBinding()]
param (
    [string]$ServiceName = "devops-mini-project",
    [string]$Region = "us-central1"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Google Cloud Platform Deployment (Cloud Run Serverless)  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verify gcloud CLI availability
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Error "CRITICAL: gcloud CLI is not installed or not in system PATH."
    Write-Host "Install Google Cloud SDK from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    Write-Host "Alternative: Run this script directly in browser via Google Cloud Shell (https://shell.cloud.google.com)" -ForegroundColor Yellow
    exit 1
}

# 2. Check active GCP project
$project = gcloud config get-value project 2>$null
if (-not $project -or $project -eq "(unset)") {
    Write-Host "[!] Setting default GCP project to project-5d074ea5-fe5a-455d-acd..." -ForegroundColor Yellow
    gcloud config set project project-5d074ea5-fe5a-455d-acd
    $project = "project-5d074ea5-fe5a-455d-acd"
}

Write-Host "[+] Target GCP Project: $project" -ForegroundColor Green
Write-Host "[+] Target Region:      $Region" -ForegroundColor Green
Write-Host "[+] Target Service:     $ServiceName" -ForegroundColor Green

# 3. Ensure required Google Cloud APIs are enabled
Write-Host "[+] Checking / enabling required GCP APIs (Cloud Run, Cloud Build, Artifact Registry)..." -ForegroundColor Cyan
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Failed to auto-enable APIs. Ensure your account has the Service Usage Admin or Project Owner role."
}

# 4. Deploy to Cloud Run using source build
Write-Host "[+] Building container via Cloud Build and deploying to Cloud Run..." -ForegroundColor Cyan
Write-Host "    Configuration: Min instances: 0 | Max instances: 1 | Memory: 256Mi | Port: 5000" -ForegroundColor Yellow
gcloud run deploy $ServiceName `
    --source . `
    --region $Region `
    --port 5000 `
    --allow-unauthenticated `
    --min-instances 0 `
    --max-instances 1 `
    --memory 256Mi `
    --cpu 1 `
    --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Error "CRITICAL: GCP Cloud Run deployment failed. Check Cloud Build logs."
    exit $LASTEXITCODE
}

# 5. Retrieve Live Service URL
$serviceUrl = gcloud run services describe $ServiceName --platform managed --region $Region --format 'value(status.url)'
Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "               DEPLOYMENT SUCCESSFUL!                     " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "Live Web Application URL: $serviceUrl" -ForegroundColor Green
Write-Host "Health Check Endpoint:    $serviceUrl/health" -ForegroundColor Green
Write-Host "API Info Endpoint:        $serviceUrl/api/info" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

# 6. Verify live endpoint
Write-Host "[+] Verifying live health endpoint..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$serviceUrl/health" -Method Get
    Write-Host "[+] Verification response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Green
} catch {
    Write-Warning "Health endpoint check timed out or failed. Verify Cloud Run service status in GCP Console."
}
