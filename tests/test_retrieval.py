from app.ingestion.chunker import chunk_text
from app.retrieval.embeddings import DeterministicEmbeddingModel
from app.retrieval.hybrid_search import HybridSearch
from app.retrieval.vector_store import InMemoryVectorStore


def test_deterministic_embeddings_are_stable() -> None:
    model = DeterministicEmbeddingModel(dimensions=16)

    first = model.embed("same document text")
    second = model.embed("same document text")
    different = model.embed("different document text")

    assert first == second
    assert first != different
    assert len(first) == 16
    assert all(isinstance(value, float) for value in first)


def test_vector_store_handles_empty_index() -> None:
    model = DeterministicEmbeddingModel(dimensions=16)
    store = InMemoryVectorStore()

    assert store.search(model.embed("query"), top_k=3) == []


def test_vector_store_respects_top_k_and_document_filter() -> None:
    model = DeterministicEmbeddingModel(dimensions=16)
    store = InMemoryVectorStore()
    first_chunks = chunk_text("doc-a", "alpha retrieval context for document isolation", 10, 2)
    second_chunks = chunk_text("doc-b", "beta retrieval context for document isolation", 10, 2)
    store.add_chunks(first_chunks, "source-a", [model.embed(chunk.text) for chunk in first_chunks])
    store.add_chunks(second_chunks, "source-b", [model.embed(chunk.text) for chunk in second_chunks])

    all_results = store.search(model.embed("retrieval context"), top_k=1)
    filtered_results = store.search(model.embed("retrieval context"), top_k=5, document_id="doc-a")

    assert len(all_results) == 1
    assert filtered_results
    assert all(result.chunk.document_id == "doc-a" for result in filtered_results)
    assert all(isinstance(result.score, float) for result in filtered_results)


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


def test_hybrid_search_exact_terms_improve_relevance() -> None:
    model = DeterministicEmbeddingModel(dimensions=32)
    store = InMemoryVectorStore()
    chunks = chunk_text(
        "doc-2",
        "Alpha topic covers billing. Retrieval validation covers grounded answers.",
        max_tokens=8,
        overlap_tokens=1,
    )
    store.add_chunks(chunks, source="unit-test", embeddings=[model.embed(chunk.text) for chunk in chunks])

    results = HybridSearch(store, model).search("Retrieval validation", top_k=1)

    assert "Retrieval validation" in results[0].chunk.text
    assert results[0].score > 0
