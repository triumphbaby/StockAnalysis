"""
Test Main API Endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """
    Test root endpoint returns API information
    """
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Stock Analysis Platform API"
    assert data["version"] == "0.1.0"
    assert data["status"] == "running"
    assert "timestamp" in data


def test_health_check(client: TestClient, mock_redis):
    """
    Test health check endpoint
    """
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["redis"] == "connected"
    assert "timestamp" in data


def test_api_info(client: TestClient):
    """
    Test API info endpoint
    """
    response = client.get("/api/info")

    assert response.status_code == 200
    data = response.json()
    assert data["api_name"] == "Stock Analysis Platform"
    assert data["version"] == "0.1.0"
    assert "features" in data
    assert len(data["features"]) > 0
    assert data["documentation"] == "/docs"


def test_swagger_docs_accessible(client: TestClient):
    """
    Test that Swagger documentation is accessible
    """
    response = client.get("/docs")

    assert response.status_code == 200


def test_redoc_accessible(client: TestClient):
    """
    Test that ReDoc documentation is accessible
    """
    response = client.get("/redoc")

    assert response.status_code == 200
