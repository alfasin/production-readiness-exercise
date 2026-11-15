from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_EVENT = {
    "service": "auth-service",
    "environment": "staging",
    "commit_sha": "a1b2c3d",
    "author": "dev@company.com",
}


def test_happy_path_staging():
    response = client.post("/api/v1/deployments", json=VALID_EVENT)
    assert response.status_code == 200


def test_rejects_empty_payload():
    response = client.post("/api/v1/deployments", json={})
    assert response.status_code == 422


def test_trace_id_returned_in_response():
    headers = {"x-trace-id": "trace-uuid-12345"}
    response = client.post("/api/v1/deployments", json=VALID_EVENT, headers=headers)
    assert response.headers.get("x-trace-id") == "trace-uuid-12345"
