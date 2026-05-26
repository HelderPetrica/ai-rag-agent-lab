from app.ingestion.chunker import chunk_text
from app.retrieval.embeddings import DeterministicEmbeddingModel
from app.retrieval.hybrid_search import HybridSearch
from app.retrieval.vector_store import InMemoryVectorStore


def test_hybrid_search_returns_relevant_context() -> None:
    model = DeterministicEmbeddingModel(dimensions=32)
    store = InMemoryVectorStore()
    chunks = chunk_text(
        "doc-1",
        "Vector search retrieves semantic context. Docker packages the API for deployment.",
        max_tokens=12,
        overlap_tokens=2,
    )
    store.add_chunks(chunks, source="unit-test", embeddings=[model.embed(chunk.text) for chunk in chunks])

    results = HybridSearch(store, model).search("How is the API packaged?", top_k=1)

    assert len(results) == 1
    assert "Docker" in results[0].chunk.text
    assert results[0].score > 0

