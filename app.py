"""
Automated CI/CD Pipeline for a Python Web Application
College DevOps Mini-Project
Technology Stack: Python, Flask, pytest, Docker, Jenkins, GitHub, GCP
"""

import os
import platform
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Application metadata
APP_NAME = "DevOps Mini-Project: Automated CI/CD Web App"
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
APP_ENV = os.environ.get("FLASK_ENV", "production")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }}</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --success: #16a34a;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: var(--bg); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 2rem 1rem; }
        .container { width: 100%; max-width: 800px; }
        .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05); padding: 2rem; margin-bottom: 1.5rem; }
        .header { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 1.25rem; margin-bottom: 1.5rem; }
        .title { font-size: 1.5rem; font-weight: 700; color: var(--text-main); }
        .badge { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.35rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600; }
        .badge-success { background-color: #dcfce7; color: #15803d; }
        .pulse-dot { width: 8px; height: 8px; background: #16a34a; border-radius: 50%; display: inline-block; box-shadow: 0 0 0 2px rgba(22,163,74,0.3); }
        .pipeline-flow { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin: 1.5rem 0; }
        .stage { flex: 1; min-width: 100px; background: #f1f5f9; border-radius: 8px; padding: 0.75rem; text-align: center; border: 1px solid var(--border); }
        .stage-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); }
        .stage-status { font-weight: 600; color: var(--primary); font-size: 0.875rem; margin-top: 0.25rem; }
        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .info-box { background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 1rem; }
        .info-label { font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.25rem; }
        .info-value { font-size: 1rem; font-weight: 600; color: var(--text-main); word-break: break-all; }
        .api-links { margin-top: 1.5rem; display: flex; gap: 1rem; }
        .btn { display: inline-flex; align-items: center; gap: 0.5rem; background: var(--primary); color: #ffffff; text-decoration: none; padding: 0.625rem 1.25rem; border-radius: 6px; font-weight: 500; font-size: 0.875rem; transition: background 0.2s; }
        .btn:hover { background: var(--primary-dark); }
        .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text-main); }
        .btn-outline:hover { background: #f1f5f9; }
        footer { margin-top: 2rem; font-size: 0.875rem; color: var(--text-muted); text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="header">
                <div>
                    <h1 class="title">{{ app_name }}</h1>
                    <p style="color: var(--text-muted); font-size: 0.875rem; margin-top: 0.25rem;">Automated CI/CD Pipeline Demo</p>
                </div>
                <span class="badge badge-success">
                    <span class="pulse-dot"></span> Live & Healthy
                </span>
            </div>

            <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem;">Pipeline Automation Flow</h3>
            <div class="pipeline-flow">
                <div class="stage">
                    <div class="stage-title">Source</div>
                    <div class="stage-status">GitHub</div>
                </div>
                <div style="color: var(--text-muted);">&rarr;</div>
                <div class="stage">
                    <div class="stage-title">CI Server</div>
                    <div class="stage-status">Jenkins</div>
                </div>
                <div style="color: var(--text-muted);">&rarr;</div>
                <div class="stage">
                    <div class="stage-title">Testing</div>
                    <div class="stage-status">pytest</div>
                </div>
                <div style="color: var(--text-muted);">&rarr;</div>
                <div class="stage">
                    <div class="stage-title">Package</div>
                    <div class="stage-status">Docker</div>
                </div>
                <div style="color: var(--text-muted);">&rarr;</div>
                <div class="stage">
                    <div class="stage-title">Deploy</div>
                    <div class="stage-status">GCP / Cloud</div>
                </div>
            </div>

            <h3 style="font-size: 1rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem;">Runtime Diagnostics</h3>
            <div class="info-grid">
                <div class="info-box">
                    <div class="info-label">Application Version</div>
                    <div class="info-value">{{ version }}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Deployment Status</div>
                    <div class="info-value" style="color: var(--success);">Operational</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Environment</div>
                    <div class="info-value">{{ environment }}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Host Node</div>
                    <div class="info-value">{{ hostname }}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Python Version</div>
                    <div class="info-value">{{ python_version }}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Server Time</div>
                    <div class="info-value">{{ current_time }} UTC</div>
                </div>
            </div>

            <div class="api-links">
                <a href="/health" class="btn">View /health JSON Endpoint</a>
                <a href="/api/info" class="btn btn-outline">View /api/info Metadata</a>
            </div>
        </div>

        <footer>
            College DevOps Mini-Project &bull; CS & DS Engineering &bull; Automated Deployment Pipeline
        </footer>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    """Home page displaying project details, pipeline flow, and runtime status."""
    return render_template_string(
        HTML_TEMPLATE,
        app_name=APP_NAME,
        version=APP_VERSION,
        environment=APP_ENV,
        hostname=platform.node() or "localhost",
        python_version=platform.python_version(),
        current_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    ), 200

@app.route("/health")
def health():
    """Health check endpoint required by load balancers, Docker, and CI/CD monitors."""
    return jsonify({
        "status": "healthy",
        "service": "devops-mini-project-api",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route("/api/info")
def info():
    """Detailed metadata endpoint for diagnostics and integration testing."""
    return jsonify({
        "project": APP_NAME,
        "version": APP_VERSION,
        "system": {
            "os": platform.system(),
            "python_version": platform.python_version(),
            "node": platform.node()
        },
        "pipeline_stages": [
            "GitHub (Source)",
            "Jenkins (CI Automation)",
            "pytest (Automated Testing)",
            "Docker (Containerization)",
            "Google Cloud Platform (Deployment)"
        ]
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Run development server (host 0.0.0.0 makes it accessible inside Docker and across network)
    app.run(host="0.0.0.0", port=port, debug=False)
