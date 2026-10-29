<#
.SYNOPSIS
    Automated GCP Cloud Run Deployment Script for DevOps Mini-Project.
.DESCRIPTION
    Builds and deploys the containerized Flask application to Google Cloud Run
    using the gcloud CLI. Uses minimal resources (free tier friendly) and outputs
    the live verified HTTPS service URL.
#>

[CmdletBinding()]
param (
    [string]$ServiceName = "devops-mini-project",
    [string]$Region = "us-central1"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Google Cloud Platform Deployment (Cloud Run Serverless)  " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verify gcloud CLI availability
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Error "gcloud CLI is not installed or not in PATH."
    Write-Host "Install Google Cloud SDK from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# 2. Check active GCP project
$project = gcloud config get-value project 2>$null
if (-not $project -or $project -eq "(unset)") {
    Write-Error "No active GCP project configured."
    Write-Host "Run: gcloud auth login && gcloud config set project <YOUR_PROJECT_ID>" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Target GCP Project: $project" -ForegroundColor Green
Write-Host "[+] Target Region: $Region" -ForegroundColor Green
Write-Host "[+] Target Service: $ServiceName" -ForegroundColor Green

# 3. Deploy to Cloud Run
Write-Host "[+] Submitting source and deploying to Cloud Run..." -ForegroundColor Cyan
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
    Write-Error "GCP Cloud Run deployment failed."
    exit $LASTEXITCODE
}

# 4. Retrieve Live Service URL
$serviceUrl = gcloud run services describe $ServiceName --platform managed --region $Region --format 'value(status.url)'
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "Live Web Application URL: $serviceUrl" -ForegroundColor Green
Write-Host "Health Check Endpoint:    $serviceUrl/health" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green

# 5. Verify live endpoint
Write-Host "[+] Verifying health endpoint..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$serviceUrl/health" -Method Get
    Write-Host "[+] Verification response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Green
} catch {
    Write-Warning "Health endpoint check timed out or failed. Check Cloud Run logs."
}
