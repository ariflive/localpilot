from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_still_works():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_still_works():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "ollama" in data
