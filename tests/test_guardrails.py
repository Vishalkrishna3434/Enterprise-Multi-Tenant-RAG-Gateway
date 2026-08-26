from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_rejects_empty_string():
    response = client.post("/api/v1/query", json={"query": ""})
    assert response.status_code == 422

def test_query_rejects_whitespace_only():
    response = client.post("/api/v1/query", json={"query": "   "})
    assert response.status_code == 422

def test_ingest_rejects_unsupported_file_type():
    response = client.post(
        "/api/v1/document_ingest",
        files={"file": ("test.exe", b"fake content", "application/octet-stream")}
    )
    assert response.status_code == 400

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200