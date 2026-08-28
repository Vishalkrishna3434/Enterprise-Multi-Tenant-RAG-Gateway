from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_before_ingest_returns_400():
    """Verifies that querying an uninitialized RAG pipeline returns 400 instead of crashing."""
    response = client.post(
        "/api/v1/query", 
        json={"query": "What is the policy?"}
    )
    assert response.status_code == 400
    assert "No documents have been ingested" in response.json()["detail"]

def test_ingest_disallowed_file_extension(tmp_path):
    """Verifies file type guardrails reject disallowed extensions before hitting ingestion logic."""
    executable_file = tmp_path / "malicious.exe"
    executable_file.write_text("echo 'bad script'")

    with open(executable_file, "rb") as f:
        response = client.post(
            "/api/v1/document_ingest",
            files={"file": ("malicious.exe", f, "application/octet-stream")}
        )
    assert response.status_code == 400

def test_query_missing_required_fields():
    """Verifies FastAPI returns 422 Unprocessable Entity when schema constraints fail."""
    response = client.post(
        "/api/v1/query", 
        json={"wrong_key": "some value"}
    )
    assert response.status_code == 422


def test_full_document_ingest_and_query_flow(tmp_path):
    """Tests full lifecycle: uploading a valid file, populating state, and querying."""
    sample_doc = tmp_path / "company_policy.txt"
    sample_doc.write_text(
        "Company Policy 2026: Employees receive 25 days of paid annual leave. "
        "Remote work is allowed up to two days per week with team lead approval."
    )

    with open(sample_doc, "rb") as f:
        ingest_res = client.post(
            "/api/v1/document_ingest",
            files={"file": ("company_policy.txt", f, "text/plain")}
        )

    assert ingest_res.status_code == 200
    assert "Successfully ingested" in ingest_res.json()["message"]
    assert ingest_res.json()["total_chunks"] > 0

    query_res = client.post(
        "/api/v1/query",
        json={"query": "How many days of paid annual leave do employees get?"}
    )

    assert query_res.status_code == 200
    payload = query_res.json()

    assert payload["query"] == "How many days of paid annual leave do employees get?"
    assert isinstance(payload["results"], list)
    assert len(payload["results"]) > 0
    assert "page_content" in payload["results"][0]
    assert "answer" in payload
    assert len(payload["answer"]) > 0