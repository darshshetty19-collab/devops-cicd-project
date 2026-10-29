"""
Verification script for Flask Web Application
Executes live HTTP requests against the application to verify:
1. HTTP status codes
2. Response headers (Content-Type)
3. Response JSON structure for /health and /api/info
4. HTML content for /
5. 404 behavior for unknown routes
"""

import sys
import os
import json
from datetime import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import app as flask_app
except ImportError as e:
    print(f"FAILED: Cannot import app: {e}")
    sys.exit(1)

client = flask_app.app.test_client()
flask_app.app.config["TESTING"] = True

errors = []

# 1. Test Home Page
res_home = client.get("/")
if res_home.status_code != 200:
    errors.append(f"Home page returned status {res_home.status_code}, expected 200")
if "text/html" not in res_home.headers.get("Content-Type", ""):
    errors.append(f"Home page Content-Type is {res_home.headers.get('Content-Type')}, expected text/html")
html_text = res_home.get_data(as_text=True)
if "DevOps Mini-Project" not in html_text or "Live & Healthy" not in html_text:
    errors.append("Home page HTML missing expected project title or status indicators")

# 2. Test Health Endpoint
res_health = client.get("/health")
if res_health.status_code != 200:
    errors.append(f"/health returned status {res_health.status_code}, expected 200")
if "application/json" not in res_health.headers.get("Content-Type", ""):
    errors.append(f"/health Content-Type is {res_health.headers.get('Content-Type')}, expected application/json")

try:
    health_data = res_health.get_json()
    if health_data.get("status") != "healthy":
        errors.append(f"/health status is {health_data.get('status')}, expected 'healthy'")
    if health_data.get("service") != "devops-mini-project-api":
        errors.append(f"/health service is {health_data.get('service')}, expected 'devops-mini-project-api'")
    # Validate ISO timestamp
    datetime.fromisoformat(health_data.get("timestamp"))
except Exception as e:
    errors.append(f"/health JSON parsing/validation error: {e}")

# 3. Test API Info Endpoint
res_info = client.get("/api/info")
if res_info.status_code != 200:
    errors.append(f"/api/info returned status {res_info.status_code}, expected 200")
try:
    info_data = res_info.get_json()
    if "pipeline_stages" not in info_data or len(info_data["pipeline_stages"]) != 5:
        errors.append(f"/api/info missing or invalid pipeline_stages: {info_data.get('pipeline_stages')}")
except Exception as e:
    errors.append(f"/api/info JSON parsing/validation error: {e}")

# 4. Test 404 Route
res_404 = client.get("/invalid-nonexistent-route-for-testing")
if res_404.status_code != 404:
    errors.append(f"Invalid route returned status {res_404.status_code}, expected 404")

# 5. Test Method Not Allowed
res_post_health = client.post("/health", json={"test": 123})
if res_post_health.status_code != 405:
    errors.append(f"POST /health returned status {res_post_health.status_code}, expected 405")

# Output results
if errors:
    print("VERIFICATION FAILED with errors:")
    for err in errors:
        print(f" - {err}")
    sys.exit(1)
else:
    print("VERIFICATION SUCCESS: All application endpoints and behavior verified.")
    print(f" - Home Page: HTTP 200 OK, Content-Type: {res_home.headers.get('Content-Type')}")
    print(f" - Health Endpoint: HTTP 200 OK, payload: {json.dumps(health_data)}")
    print(f" - Info Endpoint: HTTP 200 OK, pipeline stages: {len(info_data['pipeline_stages'])}")
    print(" - Error Handling: 404 Not Found and 405 Method Not Allowed verified.")
    sys.exit(0)
