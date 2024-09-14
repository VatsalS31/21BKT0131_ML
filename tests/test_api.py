from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "API is active"}

def test_search_endpoint():
    response = client.post("/search", json={"text": "AI", "top_k": 3, "threshold": 0.6})
    assert response.status_code == 200
