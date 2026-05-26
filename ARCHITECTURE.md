# Architecture

AI RAG Agent Lab is a compact document RAG service built to demonstrate clean Python architecture, retrieval design and agent-style workflow separation.

## Modularity Rule

The project intentionally keeps Python files below 350 lines. This makes code review easier, reduces hidden coupling and forces each module to keep a clear responsibility.

## Pipeline

1. Documents enter through `POST /documents/index` or `sample_data/`.
2. The ingestion agent normalizes each document into overlapping chunks.
3. A deterministic embedding model converts chunks into stable numeric vectors.
4. Chunks are stored in an in-memory vector-like store.
5. Metadata is stored in SQLite to demonstrate SQL-backed indexing boundaries.
6. User questions go through a retrieval agent.
7. Retrieval combines vector-like similarity with lexical overlap reranking.
8. The answer agent creates a grounded response from retrieved chunks.
9. The validation agent returns confidence and warnings.

## Chunking

Large documents are rarely useful as one retrieval unit. Chunking creates smaller evidence windows that can be ranked, cited and validated. Overlap reduces the risk of splitting relevant meaning across chunk boundaries.

## Embeddings And Dense Retrieval

The demo uses deterministic hashed embeddings so tests are reproducible and no API keys are required. This is not a production semantic model. In production, this layer could use OpenAI, Gemini, Hugging Face or local transformer embeddings.

Dense retrieval ranks documents by vector similarity. A production implementation could use FAISS, Postgres with pgvector, Qdrant or Pinecone.

## Hybrid Search And Reranking

Lexical search is useful for exact terms. Vector search is useful when wording differs. The `HybridSearch` class combines both signals and returns a final score. In production, this layer could add BM25, cross-encoder reranking or domain-specific filters.

## Metadata

Metadata makes retrieval auditable. Each chunk includes document id, source, chunk index and token count. In production, this layer commonly expands into tenant id, permissions, file hash, parser version, ingestion timestamp and retention policy.

## Agent Boundaries

- `IngestionAgent` owns document preparation.
- `RetrievalAgent` owns search behavior.
- `AnswerAgent` owns response drafting.
- `ValidationAgent` owns confidence and warnings.

The split keeps each step testable and avoids mixing parsing, retrieval, generation and validation in one large function.

## Why Validation Matters

RAG systems can fail silently when retrieval is weak. A validation step helps make uncertainty explicit through confidence and warnings. This demo keeps validation simple, but the boundary is ready for stronger checks such as citation coverage, entailment scoring or human review gates.
