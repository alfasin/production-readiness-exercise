from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_happy_path_staging():
    payload = {
        "service": "auth-service",
        "environment": "staging",
        "commit_sha": "a1b2c3d",
        "author": "dev@company.com",
    }
    response = client.post("/api/v1/deployments", json=payload)
    assert response.status_code == 200


def test_missing_required_fields_fails_silently():
    # BUG: Empty payload still returns 200 in the hackathon toy!
    # In production, this should return 422 Unprocessable Entity
    response = client.post("/api/v1/deployments", json={})
    assert response.status_code == 422, "API accepted a garbage payload without contract validation!"


def test_trace_id_propagated_in_response():
    # BUG: The toy drops tracing context
    headers = {"x-trace-id": "trace-uuid-12345"}
    payload = {"service": "cart", "environment": "staging", "commit_sha": "abc1234", "author": "dev@company.com"}
    response = client.post("/api/v1/deployments", json=payload, headers=headers)
    assert response.headers.get("x-trace-id") == "trace-uuid-12345", "Trace ID was lost across the boundary!"
