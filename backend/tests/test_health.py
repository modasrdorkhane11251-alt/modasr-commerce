"""Test health check endpoints."""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "modasr-commerce"}


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "MODASR Commerce API"
    assert data["version"] == "1.0.0"
