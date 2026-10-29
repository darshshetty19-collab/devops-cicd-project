# DevOps Mini-Project: Comprehensive Viva Preparation Guide

**Project Title**: Automated CI/CD Pipeline for a Python Web Application Using Jenkins, Docker, GitHub, and Google Cloud Platform  
**Target Audience**: 3rd Year Computer Science & Data Science Engineering Viva Examination  

---

## Quick Reference Summary of Our Project
- **Application**: Python Flask REST Web App with a diagnostic dashboard (`app.py`).
- **Health Check Endpoint**: `/health` returning HTTP 200 with JSON payload (`{"status": "healthy", ...}`).
- **Testing Framework**: `pytest` running 5 automated tests in `tests/test_app.py`.
- **Packaging**: Containerized using `Dockerfile` based on `python:3.11-slim`.
- **CI/CD Orchestrator**: Declarative pipeline in `Jenkinsfile` with 6 automated stages.
- **Source Control**: Git & GitHub with automated triggers.
- **Cloud Hosting**: Google Cloud Platform (Cloud Run serverless containers).

---

## 25 Essential Viva Questions & Practical Answers

### 1. What is DevOps?
**Answer**:  
DevOps is a set of practices, cultural philosophies, and tools that combines Software Development (**Dev**) and IT Operations (**Ops**). Its goal is to shorten the systems development life cycle and deliver high-quality software continuously with speed, reliability, and security.  
*In this project*: Instead of developers writing code and manually handing it off to sysadmins to copy onto servers, our Git-push triggers automated Jenkins tests, builds a Docker image, and deploys it automatically.

---

### 2. What is CI/CD?
**Answer**:  
- **CI (Continuous Integration)**: The practice of automating the integration of code changes from multiple contributors into a single repository. Automated builds and tests run on every push to detect integration errors early.
- **CD (Continuous Delivery / Deployment)**: 
  - *Continuous Delivery*: Automatically preparing tested code artifacts ready to be released to production at the click of a button.
  - *Continuous Deployment*: Automatically releasing every validated change directly into the live production environment without manual intervention.

---

### 3. What is Jenkins and how does it fit into this project?
**Answer**:  
Jenkins is an open-source automation server written in Java. It acts as the central coordinator (CI/CD engine) of our project. Whenever new code arrives on GitHub, Jenkins automatically pulls the code, activates the Python virtual environment, runs `pytest`, instructs the Docker daemon to build a container image, and executes the deployment script.

---

### 4. What is a Jenkinsfile?
**Answer**:  
A `Jenkinsfile` is a text file that contains the definition of a Jenkins Pipeline as code (Pipeline-as-Code). It is stored in the root of the source code repository alongside the application code.  
*In our project*: `Jenkinsfile` uses the Declarative syntax and defines 6 discrete stages (`Checkout`, `Install Test Dependencies`, `Run Automated Tests`, `Build Docker Image`, `Deploy Application`, and `Verify Deployment`).

---

### 5. What is the difference between Declarative and Scripted Jenkins Pipelines?
**Answer**:  
- **Declarative Pipeline** (Used in our project): Uses a structured, opinionated syntax enclosed in `pipeline { ... }` blocks. It provides cleaner readability, strict syntax checking, and built-in error handling (`post { success {} failure {} }`).
- **Scripted Pipeline**: The legacy format built directly on Groovy syntax (`node { ... }`). It offers maximum programmatic flexibility but is harder to read, maintain, and debug.

---

### 6. What is Docker, and why is it preferred over Virtual Machines?
**Answer**:  
Docker is an open-source containerization platform that packages an application and all its dependencies (runtime, system libraries, configuration) into a lightweight, standalone container.  
*Docker vs. Virtual Machines*:
- Virtual Machines (VMs) virtualize the entire hardware stack and run a complete guest Operating System (taking gigabytes of disk and minutes to boot).
- Docker containers share the host machine's OS kernel and isolate processes at user-space level (taking megabytes and booting in milliseconds).

---

### 7. What is the difference between a Docker Image and a Docker Container?
**Answer**:  
- **Docker Image**: An immutable, read-only blueprint or template containing application code, libraries, and instructions for how to run the app. It is built using the `docker build` command.
- **Docker Container**: A runnable, live instance of a Docker image. It is launched using the `docker run` command and adds a thin writable layer on top of the image layers.

---

### 8. Explain the instructions used in our `Dockerfile`.
**Answer**:  
In our project's `Dockerfile`:
- `FROM python:3.11-slim`: Specifies a lightweight, official Linux base image with Python 3.11 pre-installed.
- `ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1`: Ensures logs flush immediately to the terminal and disables `.pyc` caching.
- `WORKDIR /app`: Creates and sets `/app` as the active working directory inside the container.
- `COPY requirements.txt .`: Copies only the dependency manifest first to leverage Docker layer caching.
- `RUN pip install --no-cache-dir -r requirements.txt`: Installs dependencies without storing cached `.whl` files, minimizing image size.
- `COPY app.py .`: Copies the application source code.
- `EXPOSE 5000`: Documents that containerized traffic listens on port 5000.
- `HEALTHCHECK`: Periodically executes an HTTP check to determine container health.
- `CMD ["python", "app.py"]`: Specifies the command executed when the container starts.

---

### 9. Why do we copy `requirements.txt` before copying `app.py` in the `Dockerfile`?
**Answer**:  
To exploit **Docker Layer Caching**. Docker caches the result of each instruction. Dependencies in `requirements.txt` change infrequently, whereas application code (`app.py`) changes constantly. By copying and installing `requirements.txt` first, subsequent builds reuse the cached dependency layer and complete in seconds rather than downloading pip packages on every build.

---

### 10. What is the role of `.dockerignore`?
**Answer**:  
`.dockerignore` excludes unnecessary files and directories (such as `venv/`, `.git/`, `.pytest_cache/`, `README.md`, and local secrets) from being sent to the Docker daemon during the `docker build` context transfer. This drastically speeds up build times and prevents sensitive files from being baked into the final image.

---

### 11. What is the role of the `/health` endpoint in microservices and DevOps?
**Answer**:  
The `/health` endpoint provides an automated mechanism for monitoring tools, container orchestrators (like Kubernetes and Docker), and cloud load balancers to verify if the application is running normally.  
*In our app*: GET `/health` returns HTTP 200 with JSON `{"status": "healthy", "service": "...", "version": "...", "timestamp": "..."}`. If this endpoint returns an error or times out, the orchestrator restarts the container or the pipeline fails the deployment.

---

### 12. What tests are implemented in `tests/test_app.py` and what does each test verify?
**Answer**:  
We implemented 5 automated tests using `pytest`:
1. `test_home_page_status_code_and_content`: Checks GET `/` returns HTTP 200 and renders HTML containing project metadata and operational indicators.
2. `test_health_endpoint_status_code`: Verifies GET `/health` responds with HTTP 200.
3. `test_health_endpoint_json_structure`: Confirms the response JSON includes required keys: `status == "healthy"`, `service`, `version`, and `timestamp`.
4. `test_api_info_endpoint`: Validates that the metadata endpoint lists all five automated CI/CD pipeline stages.
5. `test_404_not_found`: Validates proper error handling when requesting an invalid URI.

---

### 13. What happens in the Jenkins pipeline when an automated test fails?
**Answer**:  
The `Run Automated Tests` stage executes `python -m pytest`. If any test fails, pytest exits with a non-zero exit code (code 1). Jenkins intercepts this failure, immediately terminates the pipeline at Stage 3, and transitions the build status to **FAILED**.  
**Result**: The subsequent stages (`Build Docker Image` and `Deploy Application`) are completely blocked. Broken code is never packaged into a Docker image or deployed to users.

---

### 14. What is GitHub and what role does it play in the CI/CD pipeline?
**Answer**:  
GitHub is a cloud-based hosting platform for version control using Git. In our pipeline:
1. It serves as the single source of truth for all source code, tests, Dockerfile, and Jenkinsfile.
2. It tracks revision history, commits, and branches.
3. It sends automated webhook notifications to Jenkins whenever developers push code to the `main` branch.

---

### 15. How does a GitHub Webhook work?
**Answer**:  
A Webhook is an HTTP POST callback. When an event occurs on GitHub (such as `git push`), GitHub sends a JSON payload to a pre-configured webhook URL on our Jenkins server (`http://<jenkins-url>:8080/github-webhook/`). Jenkins parses this notification and instantly triggers a new build.

---

### 16. Why did we choose Google Cloud Run over Compute Engine for GCP deployment?
**Answer**:  
1. **Serverless Architecture**: Cloud Run is a fully managed Container-as-a-Service (CaaS) platform. We do not need to configure virtual machines, manage Linux OS updates, or set up SSH keys.
2. **Cost Efficiency**: Cloud Run scales down to zero instances when idle ($0 cost), whereas a Compute Engine VM runs 24/7 and incurs continuous charges.
3. **Automated SSL/TLS**: Cloud Run provides a secure, public HTTPS URL immediately upon deployment.
4. **Speed**: Deployment takes under a minute using `gcloud run deploy`.

---

### 17. How is the application deployed to Google Cloud Platform?
**Answer**:  
Through our deployment script (`deploy_gcp.ps1` / `deploy_gcp.sh`) or the Google Cloud CLI command:
```bash
gcloud run deploy devops-mini-project \
  --source . \
  --region us-central1 \
  --port 5000 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 1 \
  --memory 256Mi \
  --cpu 1
```
GCP builds the container via Cloud Build and deploys it to Cloud Run, returning a live HTTPS endpoint.

---

### 18. How are credentials and secrets protected in this project?
**Answer**:  
1. **`.gitignore` & `.dockerignore`**: Prevent local secret files (`.env`, `credentials.json`, `service-account-key.json`) from being committed to GitHub or copied into Docker images.
2. **Jenkins Credentials Store**: Passwords, API tokens, and service account keys are stored encrypted within Jenkins' native credential management system (`withCredentials([string(...)])`).
3. **IAM (Identity and Access Management)**: GCP uses least-privilege service accounts rather than root credentials.

---

### 19. How does Docker handle container port mapping (`-p 5000:5000`)?
**Answer**:  
In the command `docker run -d -p 5000:5000 devops-mini-project`:
- The first `5000` is the **Host Port** (the port opened on the developer's laptop or server).
- The second `5000` is the **Container Port** (the internal port where the Flask application is listening).
- Docker forwards external network requests hitting host port 5000 into the container's port 5000.

---

### 20. How is zero-downtime or rolling update simulated when deploying a new container?
**Answer**:  
In our Jenkinsfile deployment stage:
1. The new Docker image is built with a new tag (`devops-mini-project:${BUILD_NUMBER}`).
2. The old container is stopped (`docker stop devops-app-live`) and removed (`docker rm devops-app-live`).
3. The new container is started immediately using the updated image.
*In cloud environments (like Cloud Run or Kubernetes)*: Traffic is seamlessly redirected to the new container revision only after its health check passes, ensuring true zero downtime.

---

### 21. What is the role of `pytest.ini` in this project?
**Answer**:  
`pytest.ini` is the primary configuration file for pytest. In our project, it sets:
```ini
[pytest]
testpaths = tests
pythonpath = .
```
This automatically adds the root directory to Python's module search path (`sys.path`), ensuring tests inside `tests/test_app.py` can cleanly import `from app import app` without path errors.

---

### 22. What is the purpose of the JUnit XML report in Stage 3 of the Jenkinsfile?
**Answer**:  
Running `pytest --junitxml=test-results.xml` exports the test results into a standard XML format that Jenkins natively understands. The Jenkins `junit testResults: 'test-results.xml'` step parses this file to generate graphical test trend charts, test history, and individual test failure reports right on the Jenkins build page.

---

### 23. What are the main limitations of this mini-project?
**Answer**:  
1. **Stateless Web App**: It demonstrates CI/CD for a stateless Flask service without a database persistence layer.
2. **Single Host Deployment**: The local pipeline runs on a single host machine rather than a distributed multi-node Kubernetes cluster.
3. **Polling vs. Direct Webhooks**: When testing locally without a public IP, Jenkins relies on SCM polling rather than real-time inbound GitHub webhooks.

---

### 24. What are three realistic future enhancements you would propose?
**Answer**:  
1. **Kubernetes Integration**: Deploy container images to Google Kubernetes Engine (GKE) with automated rolling updates and Horizontal Pod Autoscaling (HPA).
2. **Static Code Analysis & Security Scans**: Add SonarQube for code smell analysis and Trivy / Snyk for container vulnerability scanning.
3. **Slack / Email Notification Stage**: Add a Jenkins post stage to notify team members on Slack or Discord regarding build failures or successful deployments.

---

### 25. Walk me through what happens from the moment you hit Enter on `git push` to the application being live.
**Answer**:  
1. Developer runs `git push origin main`. GitHub receives the commit.
2. GitHub sends a webhook POST request to Jenkins (or Jenkins polls GitHub and detects the new commit).
3. Jenkins triggers build number `#N` using `Jenkinsfile`.
4. Stage 1 checks out the commit into the workspace.
5. Stage 2 activates the virtual environment and installs dependencies from `requirements.txt`.
6. Stage 3 executes `pytest`. All 5 tests pass; test results are recorded.
7. Stage 4 builds the Docker image tagged `devops-mini-project:${BUILD_NUMBER}`.
8. Stage 5 replaces the previous container with the new version.
9. Stage 6 queries `http://localhost:5000/health` and verifies HTTP 200 OK.
10. The post-action prints the operational URL and marks the pipeline build as **SUCCESS**.
