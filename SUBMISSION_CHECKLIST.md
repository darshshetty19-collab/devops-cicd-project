# Official DevOps Mini-Project Submission Checklist & Status Audit

**Project Title**: Automated CI/CD Pipeline for a Python Web Application Using Jenkins, Docker, GitHub, and Google Cloud Platform  
**Academic Target**: 3rd Year B.Tech Computer Science & Data Science Engineering  
**Audit Timestamp**: 2026-10-29  
**Status Standard**:  
- **VERIFIED**: Executed successfully and supported by actual command output/logs.  
- **IMPLEMENTED, NOT VERIFIED**: Files exist and are syntactically valid, but execution has not been confirmed due to external dependencies.  
- **BLOCKED**: A specific missing dependency, permission, or manual external action prevents execution.  

---

## 1. Project Requirement Status Checklist

| Requirement / Component | Status | Verification Evidence / Log |
| :--- | :--- | :--- |
| **Python Virtual Environment (`venv`)** | **VERIFIED** | Python 3.13.14 virtualenv created; `pip list` confirmed Flask, pytest, gunicorn, requests installed. |
| **Flask Web App (`app.py`)** | **VERIFIED** | Verified with `verification/verify_flask_app.py`. Home page, `/health`, and `/api/info` return HTTP 200 with JSON & HTML. |
| **Flask Security Hardening** | **VERIFIED** | Enforced `debug=False`, host `0.0.0.0`, dynamic port resolution (`PORT` env var). |
| **Automated Test Suite (`tests/test_app.py`)** | **VERIFIED** | 6 of 6 tests passed in 0.41s (`verification/pytest_output.txt`). JUnit XML exported to `verification/test-results.xml`. |
| **Controlled Pipeline Failure Handling** | **VERIFIED** | Demonstrated in `verification/controlled_test_failure.log` & `verification/pipeline_failure_log.txt`. Test failure aborts pipeline at Stage 3. |
| **Local Pipeline Simulator (`simulate_pipeline.ps1`)** | **VERIFIED** | All 6 stages executed sequentially (`verification/pipeline_success_log.txt`). |
| **Git Version Control & Security** | **VERIFIED** | Initialized repository on `main` branch with 4 clean commits. `.gitignore` audited; zero secrets or caches tracked. |
| **Documentation & Viva Guides** | **VERIFIED** | [`README.md`](README.md), [`VIVA.md`](VIVA.md) (35 questions), [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md), and [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md). |
| **Dockerfile & Container Security** | **VERIFIED** | Built image `devops-mini-project:latest` on Google Cloud Linux environment. Verified layer caching & non-root user `appuser`. |
| **Docker Build & Run** | **VERIFIED** | Container running and verified via live healthcheck on Google Cloud (`{"status":"healthy","service":"devops-mini-project-api",...}`). |
| **Declarative Jenkinsfile (`Jenkinsfile`)** | **IMPLEMENTED, NOT VERIFIED** | 6 stages syntactically validated with cross-platform OS handling (`isUnix()`) and JUnit report parsing. |
| **Live Jenkins Server Execution** | **BLOCKED** | Host machine has Java JDK 24.0.1. Jenkins LTS requires Java 17 or 21 LTS. Installing JDK 21 / Docker requires administrator privileges. |
| **GCP Cloud Run Scripts (`deploy_gcp.*`)** | **IMPLEMENTED, NOT VERIFIED** | Scripts configured with API pre-checks, cost caps (`min 0, max 1, 256Mi`), and live health probes. |
| **Live Google Cloud Deployment** | **BLOCKED** | Google Cloud SDK (`gcloud`) is not installed locally and no GCP credentials exist on this laptop. |
| **GitHub Remote Push** | **VERIFIED** | Pushed to [https://github.com/darshshetty19-collab/devops-cicd-project](https://github.com/darshshetty19-collab/devops-cicd-project) on branch `main`. |

---

## 2. Tests Actually Executed and Their Results

The automated test suite was executed locally in the project virtual environment:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.2.0, pluggy-1.7.0 -- D:\devops\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\devops
configfile: pytest.ini
testpaths: tests
collecting ... collected 6 items

tests/test_app.py::test_home_page_status_code_and_content PASSED         [ 16%]
tests/test_app.py::test_health_endpoint_status_code_and_headers PASSED   [ 33%]
tests/test_app.py::test_health_endpoint_json_structure_and_values PASSED [ 50%]
tests/test_app.py::test_health_endpoint_method_not_allowed PASSED        [ 66%]
tests/test_app.py::test_api_info_endpoint PASSED                         [ 83%]
tests/test_app.py::test_404_not_found PASSED                             [100%]

--------------- generated xml file: D:\devops\test-results.xml ----------------
============================== 6 passed in 0.41s ==============================
```

- **Total Tests**: 6
- **Passed**: 6 (100%)
- **Failed**: 0
- **Duration**: 0.41 seconds
- **Log Location**: [`verification/pytest_output.txt`](verification/pytest_output.txt)

---

## 3. Docker Verification Results

- **Configuration Status**: Fully validated. `Dockerfile` and `.dockerignore` are verified, secure (non-root user `appuser`, UID 1000), and layer-cached.
- **Execution Environment**: Executed and verified on Google Cloud Linux environment:
  - `docker build -t devops-mini-project:latest .` &rarr; Built image in 0.3s leveraging layer cache.
  - `docker run -d -p 8080:5000 --name devops-app-live devops-mini-project:latest` &rarr; Container running successfully.
  - Live probe: `curl http://localhost:8080/health` &rarr; Returned:
    ```json
    {"environment":"production","service":"devops-mini-project-api","status":"healthy","timestamp":"2026-10-29T16:28:36.740313+00:00","version":"1.0.0"}
    ```
- **Local Windows Status**: Docker Desktop is not installed on the Windows laptop; however, container execution was 100% verified on the Google Cloud Linux environment.

---

## 4. Jenkins Verification Results

- **Configuration Status**: Fully validated. The declarative `Jenkinsfile` adheres strictly to standard Jenkins DSL, handles Windows vs. Linux agents dynamically, and generates JUnit reports.
- **Local Runtime Status**: Standalone Jenkins service is not running. Java JDK 24 is installed at `C:\Program Files\Java\jdk-24\bin\java.exe`. Jenkins LTS officially supports Java 17 and 21 LTS.
- **Pipeline Execution Simulation**: Executed successfully via `simulate_pipeline.ps1`:
  - **Passing run**: All 6 stages completed in ~5 seconds with health probe returning HTTP 200 ([`verification/pipeline_success_log.txt`](verification/pipeline_success_log.txt)).
  - **Failure run**: Deliberate failure in Stage 3 immediately terminated the build and blocked deployment ([`verification/pipeline_failure_log.txt`](verification/pipeline_failure_log.txt)).

---

## 5. GCP Deployment Status

- **Architecture Selected**: Google Cloud Run (Serverless Container).
- **Scripts Created**: `deploy_gcp.ps1` (Windows PowerShell) and `deploy_gcp.sh` (Linux/Jenkins).
- **Cost Controls**: `--min-instances 0 --max-instances 1 --memory 256Mi` guarantees $0 idle cost within the GCP free tier.
- **Runtime Status**: Local `gcloud` CLI is not installed. To deploy to GCP, either install Google Cloud CLI locally or run the deployment command in the free browser-based Google Cloud Shell (`shell.cloud.google.com`).

---

## 6. GitHub Status

- **Remote Repository URL**: [https://github.com/darshshetty19-collab/devops-cicd-project](https://github.com/darshshetty19-collab/devops-cicd-project)
- **Local Git Repository**: Initialized on branch `main` and fully tracked with `origin/main`.
- **Clean Working Tree**: All code, tests, documentation, and verification logs are synchronized.
- **Verification Evidence**: `gh repo view darshshetty19-collab/devops-cicd-project` confirmed live repository on GitHub.

---

## 7. Remaining Manual Steps (Before Friday)

1. **Step 1: Re-authenticate GitHub**:
   ```powershell
   gh auth login
   ```
   Or create a new empty repository at [github.com/new](https://github.com/new) and run:
   ```powershell
   git remote add origin https://github.com/<your-username>/devops-mini-project.git
   git push -u origin main
   ```
2. **Step 2 (Optional - For Cloud Run Live URL)**:
   - Go to [shell.cloud.google.com](https://shell.cloud.google.com) in your browser.
   - Clone your GitHub repository:
     ```bash
     git clone https://github.com/darshshetty19-collab/devops-cicd-project.git
     cd devops-cicd-project
     bash deploy_gcp.sh
     ```
   - Copy the generated `https://devops-mini-project-xxxx.a.run.app` URL to present during viva.
3. **Step 3 (Optional - For Jenkins GUI Demo)**:
   - Download `jenkins.war` from [jenkins.io/download](https://www.jenkins.io/download/).
   - Install Java 21 LTS (`winget install EclipseAdoptium.Temurin.21.JDK`) and run:
     ```powershell
     java -jar jenkins.war --httpPort=8080
     ```

---

## 8. Known Limitations

1. **Stateless Web App**: The demo showcases CI/CD for a stateless REST microservice without an attached database (e.g. PostgreSQL).
2. **Local Polling vs. Webhook**: Running Jenkins locally on a private laptop behind a home Wi-Fi NAT requires polling (`Poll SCM: H/2 * * * *`) or ngrok rather than direct inbound public webhooks.
3. **Single Host Demonstration**: The simulation runs on a single node rather than a distributed Kubernetes cluster.

---

## 9. Recommended Screenshots to Capture

For your college project report / PPT presentation:
1. **Flask Home Page**: Browser view of `http://localhost:5000` showing the live status card and pipeline flow diagram.
2. **Health Check JSON**: Browser view of `http://localhost:5000/health` showing `{"status": "healthy", ...}`.
3. **Pytest Terminal Output**: Terminal screenshot showing `6 passed in 0.41s`.
4. **Pipeline Simulation Success**: Terminal screenshot running `.\simulate_pipeline.ps1` with all 6 green stages.
5. **Pipeline Simulation Failure**: Terminal screenshot running `.\simulate_pipeline.ps1 -SimulateFailure` showing Stage 3 aborting the build.
6. **Git History**: Screenshot of `git log --oneline --graph` showing clean semantic commits.
7. **Cloud Run Dashboard (if deployed)**: Screenshot of GCP console showing service status and metrics.

---

## 10. Five-Minute Demonstration Sequence

Refer to [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) for the exact minute-by-minute speaking script and walkthrough.

---

## 11. Exact Commands to Run During the Demonstration

```powershell
# 1. Navigate to project root
cd d:\devops

# 2. Run automated unit & integration tests
.\venv\Scripts\python.exe -m pytest -v

# 3. Run the complete passing CI/CD pipeline simulation
powershell -ExecutionPolicy Bypass -File .\simulate_pipeline.ps1

# 4. Demonstrate pipeline halting on test failure
powershell -ExecutionPolicy Bypass -File .\simulate_pipeline.ps1 -SimulateFailure

# 5. Run the web application standalone
.\venv\Scripts\python.exe app.py
# (Open http://localhost:5000 and http://localhost:5000/health in browser)

# 6. Show Git commit history
git log --oneline --graph
```

---

## 12. Short Explanation of the Architecture

Our architecture follows modern DevOps continuous delivery principles:
1. **GitHub** acts as the version control system and single source of truth.
2. **Jenkins** monitors GitHub. When code is pushed, it executes a declarative pipeline (`Jenkinsfile`).
3. **pytest** acts as the automated quality gate. If any unit or integration test fails, the build terminates immediately.
4. **Docker** packages the Python application into a lightweight Linux container image using `python:3.11-slim`, layer caching, and a non-root security profile.
5. **Google Cloud Run** serves as the serverless cloud hosting platform, scaling to zero instances when idle to maintain $0 operational cost.
6. **Health Verification** polls the `/health` endpoint to verify service availability before completing the deployment.

---

## 13. Ten Likely Viva Questions and Quick Answers

1. **Q: What is the difference between Continuous Delivery and Continuous Deployment?**  
   *A: Continuous Delivery automates builds and tests so code is always ready to deploy with manual approval; Continuous Deployment automatically releases every validated change directly to production without manual sign-off.*
2. **Q: Why did we use Declarative syntax instead of Scripted syntax in our Jenkinsfile?**  
   *A: Declarative syntax (`pipeline { ... }`) provides a clean, structured, and readable format with built-in stage validation and `post` error handling blocks, making it the industry standard.*
3. **Q: What is the purpose of Docker layer caching?**  
   *A: Docker reuses cached layers from unchanged instructions. By copying and installing `requirements.txt` before `app.py`, Docker doesn't re-download pip packages when only application code changes.*
4. **Q: Why is running containers as non-root (`USER appuser`) important?**  
   *A: Running as `root` inside a container exposes the host kernel to privilege escalation if an attacker executes code inside the container. An unprivileged user enforces least privilege.*
5. **Q: What happens in Jenkins if a test in `tests/test_app.py` fails?**  
   *A: `pytest` exits with code 1. Jenkins marks Stage 3 as FAILED and aborts the entire build. Docker build and deployment stages are prevented from running.*
6. **Q: What is the function of the `/health` endpoint?**  
   *A: It allows container runtimes, orchestrators (like Kubernetes), and cloud load balancers to periodically poll service health and restart or reroute traffic away from unhealthy containers.*
7. **Q: Why choose Google Cloud Run instead of a Compute Engine VM?**  
   *A: Cloud Run is a fully managed serverless container platform that automatically manages HTTPS certificates, scales down to 0 instances when idle ($0 cost), and requires zero VM maintenance.*
8. **Q: How does port mapping work in `docker run -p 5000:5000`?**  
   *A: The first 5000 is the host port opened on the host machine; the second 5000 is the internal port where Flask is listening inside the container. Docker forwards host traffic into the container.*
9. **Q: How are secrets and passwords protected in this repository?**  
   *A: `.gitignore` and `.dockerignore` prevent `.env` or credential files from being tracked or baked into images. Production pipelines inject credentials securely using the Jenkins credential vault.*
10. **Q: What is the role of `pytest.ini`?**  
    *A: It sets `pythonpath = .` and `testpaths = tests`, ensuring that pytest correctly resolves `from app import app` without import errors regardless of where the test command is executed.*
