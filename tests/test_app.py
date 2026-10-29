"""
Automated Unit and Integration Tests for Flask Web Application
Executed during Jenkins CI 'Test' Stage using pytest
"""

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
    Verifies that the home page returns HTTP 200 OK and contains
    the project title and key deployment indicators.
    """
    response = client.get("/")
    assert response.status_code == 200
    html_content = response.get_data(as_text=True)
    assert "DevOps Mini-Project" in html_content
    assert "Live & Healthy" in html_content
    assert "Operational" in html_content

def test_health_endpoint_status_code(client):
    """
    Test Health Endpoint (/health) Status:
    Verifies that the health check responds with HTTP 200 OK,
    which is essential for container orchestrators and load balancers.
    """
    response = client.get("/health")
    assert response.status_code == 200

def test_health_endpoint_json_structure(client):
    """
    Test Health Endpoint JSON Payload:
    Verifies that the returned JSON contains the required keys:
    'status' (must be 'healthy'), 'service', 'version', and 'timestamp'.
    """
    response = client.get("/health")
    data = response.get_json()
    assert isinstance(data, dict)
    assert data.get("status") == "healthy"
    assert "service" in data
    assert "version" in data
    assert "timestamp" in data

def test_api_info_endpoint(client):
    """
    Test Info API Endpoint (/api/info):
    Verifies that the diagnostic metadata endpoint returns HTTP 200
    and lists all CI/CD pipeline stages accurately.
    """
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.get_json()
    assert "pipeline_stages" in data
    assert len(data["pipeline_stages"]) == 5
    assert "GitHub (Source)" in data["pipeline_stages"]
    assert "Google Cloud Platform (Deployment)" in data["pipeline_stages"]

def test_404_not_found(client):
    """
    Test Error Handling:
    Verifies that requesting an undefined route correctly returns HTTP 404 Not Found.
    """
    response = client.get("/undefined-route-endpoint")
    assert response.status_code == 404
