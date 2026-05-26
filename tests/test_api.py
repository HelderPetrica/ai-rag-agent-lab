from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "AI RAG Agent Lab"
    assert payload["version"] == "1.0.0"


def test_root_endpoint_explains_sanitized_demo() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["sanitized_demo"] is True
    assert "Sanitized" in payload["description"]


def test_query_endpoint_without_indexed_documents_is_safe() -> None:
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "What is indexed?", "top_k": 2})

    assert response.status_code == 200
    payload = response.json()
    assert payload["retrieved_context"] == []
    assert payload["sources"] == []
    assert payload["confidence"] == 0.0
    assert payload["warnings"]
    assert payload["metadata"]["indexed_chunks"] == 0


def test_query_endpoint_returns_grounded_shape_after_indexing() -> None:
    with TestClient(app) as client:
        index_response = client.post("/documents/index", json={"use_sample_data": True})
        query_response = client.post(
            "/query",
            json={"question": "How should a RAG service validate weak context?", "top_k": 2},
        )

    assert index_response.status_code == 200
    assert index_response.json()["indexed_chunks"] > 0
    assert query_response.status_code == 200
    payload = query_response.json()
    assert payload["answer"]
    assert payload["retrieved_context"]
    assert payload["sources"]
    assert 0 <= payload["confidence"] <= 1
    assert "warnings" in payload
    assert payload["metadata"]["retrieved_chunks"] == len(payload["retrieved_context"])
