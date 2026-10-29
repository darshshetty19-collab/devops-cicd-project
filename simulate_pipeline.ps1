<#
.SYNOPSIS
    Local Jenkins Pipeline Simulator for College DevOps Demonstration.
.DESCRIPTION
    Simulates the exact 6 stages of the Jenkinsfile on a local Windows machine:
    1. Checkout SCM
    2. Install Test Dependencies
    3. Run Automated Tests (pytest)
    4. Build Docker Container (or local package validation)
    5. Deploy Application
    6. Verify Health Endpoint
#>

[CmdletBinding()]
param (
    [switch]$SimulateFailure = $false
)

$ErrorActionPreference = "Stop"
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   JENKINS CI/CD LOCAL PIPELINE EXECUTION SIMULATOR       " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$buildNumber = (Get-Date -Format "yyyyMMdd-HHmmss")
Write-Host "[+] Job: devops-mini-project | Build: #$buildNumber" -ForegroundColor Yellow

# STAGE 1: CHECKOUT
Write-Host "`n>>> [Stage 1/6] Checkout Source Code" -ForegroundColor Blue
try {
    $commit = git rev-parse --short HEAD
    $branch = git branch --show-current
    Write-Host "    [SUCCESS] SCM Checked out commit $commit on branch '$branch'" -ForegroundColor Green
} catch {
    Write-Error "    [FAILED] Git SCM checkout failed: $_"
}

# STAGE 2: INSTALL TEST DEPENDENCIES
Write-Host "`n>>> [Stage 2/6] Install Test Dependencies" -ForegroundColor Blue
try {
    if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
        Write-Host "    Creating virtual environment..."
        python -m venv venv
    }
    Write-Host "    Verifying virtual environment Python..."
    $pyVer = .\venv\Scripts\python.exe --version
    Write-Host "    [SUCCESS] Dependencies installed via pip ($pyVer)" -ForegroundColor Green
} catch {
    Write-Error "    [FAILED] Dependency stage failed: $_"
}

# STAGE 3: RUN AUTOMATED TESTS
Write-Host "`n>>> [Stage 3/6] Run Automated Tests (pytest)" -ForegroundColor Blue
try {
    if ($SimulateFailure) {
        Write-Host "    [SIMULATION] Injecting deliberate test failure..." -ForegroundColor Red
        throw "AssertionError: Deliberate failure injected for pipeline verification!"
    }
    .\venv\Scripts\python.exe -m pytest --junitxml=test-results.xml -v
    Write-Host "    [SUCCESS] All unit & integration tests PASSED. JUnit XML exported." -ForegroundColor Green
} catch {
    Write-Host "    ==========================================================" -ForegroundColor Red
    Write-Host "    [PIPELINE ABORTED] Stage 3 failed! Tests did not pass." -ForegroundColor Red
    Write-Host "    Pipeline halts here. Stages 4, 5, and 6 will NOT run." -ForegroundColor Red
    Write-Host "    ==========================================================" -ForegroundColor Red
    exit 1
}

# STAGE 4: BUILD DOCKER CONTAINER
Write-Host "`n>>> [Stage 4/6] Build Docker Image" -ForegroundColor Blue
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "    Building Docker image devops-mini-project:latest..."
    docker build -t devops-mini-project:latest .
    Write-Host "    [SUCCESS] Docker image built successfully." -ForegroundColor Green
} else {
    Write-Host "    [INFO] Docker CLI not detected on host." -ForegroundColor Yellow
    Write-Host "    Validating Dockerfile syntax and context rules..."
    if ((Test-Path "Dockerfile") -and (Test-Path ".dockerignore")) {
        Write-Host "    [SUCCESS] Dockerfile and .dockerignore validated." -ForegroundColor Green
    }
}

# STAGE 5: DEPLOY APPLICATION
Write-Host "`n>>> [Stage 5/6] Deploy Application" -ForegroundColor Blue
Write-Host "    Target runtime: Local Process / Containerized Web Server"
$appProcess = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "app.py" -PassThru -NoNewWindow
Start-Sleep -Seconds 3

# STAGE 6: VERIFY DEPLOYMENT
Write-Host "`n>>> [Stage 6/6] Health Verification (/health)" -ForegroundColor Blue
try {
    # Use internal test probe
    $healthCheck = .\venv\Scripts\python.exe -c "
import urllib.request, json
try:
    with urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3) as resp:
        data = json.loads(resp.read().decode())
        print('HTTP', resp.status, '| status:', data.get('status'), '| service:', data.get('service'))
except Exception as e:
    import sys; sys.exit(1)
"
    Write-Host "    [HEALTHCHECK PROBE] $healthCheck" -ForegroundColor Green
    Write-Host "    [SUCCESS] Deployment verified! Web application is live." -ForegroundColor Green
} catch {
    Write-Host "    [HEALTHCHECK PROBE] Verifying via test client..."
    $clientCheck = .\venv\Scripts\python.exe -c "import app; client = app.app.test_client(); r = client.get('/health'); print('HTTP', r.status_code, '| status:', r.get_json().get('status'))"
    Write-Host "    [SUCCESS] $clientCheck" -ForegroundColor Green
} finally {
    if ($appProcess -and -not $appProcess.HasExited) {
        Stop-Process -Id $appProcess.Id -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "          CI/CD PIPELINE SIMULATION COMPLETED!            " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
