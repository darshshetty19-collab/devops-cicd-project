"""
Automated Unit and Integration Tests for Flask Web Application
Executed during Jenkins CI 'Test' Stage using pytest
"""

from datetime import datetime
import pytest
from app import app

@pytest.fixture
def client():
    """Create a Flask test client for sending simulated HTTP requests."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page_status_code_and_content(client):
    """
    Test Home Page (/):
    Verifies that the home page returns HTTP 200 OK, has correct Content-Type,
    and contains the project title, pipeline stages, and deployment indicators.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("Content-Type", "")
    html_content = response.get_data(as_text=True)
    assert "DevOps Mini-Project" in html_content
    assert "Live & Healthy" in html_content
    assert "Operational" in html_content
    assert "Pipeline Automation Flow" in html_content

def test_health_endpoint_status_code_and_headers(client):
    """
    Test Health Endpoint (/health) Status & Headers:
    Verifies that the health check responds with HTTP 200 OK and application/json Content-Type,
    which is essential for container orchestrators and load balancers.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert "application/json" in response.headers.get("Content-Type", "")

def test_health_endpoint_json_structure_and_values(client):
    """
    Test Health Endpoint JSON Payload:
    Verifies that the returned JSON contains the required keys:
    'status' (must strictly be 'healthy'), 'service', 'version', 'environment', and 'timestamp'.
    Validates that the timestamp adheres to ISO-8601 formatting.
    """
    response = client.get("/health")
    data = response.get_json()
    assert isinstance(data, dict), "Health endpoint must return a JSON object"
    assert data.get("status") == "healthy"
    assert data.get("service") == "devops-mini-project-api"
    assert "version" in data and len(data["version"]) > 0
    assert "environment" in data
    assert "timestamp" in data

    # Verify timestamp parseability
    ts = datetime.fromisoformat(data["timestamp"])
    assert ts is not None

def test_health_endpoint_method_not_allowed(client):
    """
    Test Health Endpoint HTTP Methods:
    Verifies that POST /health is rejected with HTTP 405 Method Not Allowed,
    ensuring the healthcheck endpoint remains an idempotent GET route.
    """
    response = client.post("/health", json={"test": "data"})
    assert response.status_code == 405

def test_api_info_endpoint(client):
    """
    Test Info API Endpoint (/api/info):
    Verifies that the diagnostic metadata endpoint returns HTTP 200,
    returns valid JSON, and lists all CI/CD pipeline stages accurately.
    """
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.get_json()
    assert "pipeline_stages" in data
    assert len(data["pipeline_stages"]) == 5
    assert "GitHub (Source)" in data["pipeline_stages"]
    assert "Jenkins (CI Automation)" in data["pipeline_stages"]
    assert "pytest (Automated Testing)" in data["pipeline_stages"]
    assert "Docker (Containerization)" in data["pipeline_stages"]
    assert "Google Cloud Platform (Deployment)" in data["pipeline_stages"]

def test_404_not_found(client):
    """
    Test Error Handling:
    Verifies that requesting an undefined route correctly returns HTTP 404 Not Found.
    """
    response = client.get("/undefined-route-endpoint")
    assert response.status_code == 404
