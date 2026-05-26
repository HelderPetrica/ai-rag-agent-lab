# Architecture

AI RAG Agent Lab is a compact document RAG service built to demonstrate clean Python architecture, retrieval design and agent-style workflow separation.

## Modularity Rule

The project intentionally keeps Python files below 350 lines. This makes code review easier, reduces hidden coupling and forces each module to keep a clear responsibility. The current API orchestration, retrieval, ingestion, schema and agent layers are split for that reason.

## Pipeline

1. Documents enter through `POST /documents/index` or through `sample_data/`.
2. The ingestion agent normalizes each document into overlapping chunks.
3. A deterministic embedding model converts chunks into stable numeric vectors.
4. Chunks are stored in an in-memory vector store.
5. Metadata is stored in SQLite to demonstrate SQL-backed indexing boundaries.
6. User questions go through a retrieval agent.
7. Retrieval combines vector-like similarity with lexical overlap reranking.
8. The answer agent creates a grounded response from retrieved chunks.
9. The validation agent returns confidence and warnings.

## Why Chunking Matters

Large documents are rarely useful as one retrieval unit. Chunking creates smaller evidence windows that can be ranked, cited and validated. Overlap reduces the risk of splitting relevant meaning across chunk boundaries.

## Lexical Search vs Vector Search

Lexical search matches exact terms and is useful for precise keywords, identifiers and terminology. Vector search ranks by embedding similarity and can surface related content even when wording differs. This demo combines both ideas in a small hybrid search layer.

## Metadata

Metadata makes retrieval auditable. Each chunk includes document id, source, chunk index and token count. In production, this layer commonly expands into tenant id, permissions, file hash, ingestion timestamp, parser version and retention policy.

## Agent Boundaries

The agent layer is deliberately simple:

- `IngestionAgent` owns document preparation.
- `RetrievalAgent` owns search behavior.
- `AnswerAgent` owns response drafting.
- `ValidationAgent` owns confidence and warnings.

This split keeps each responsibility testable. It also mirrors how larger GenAI systems separate orchestration, retrieval, answer generation, guardrails and evaluation.

## Production Extensions

In production, the same architecture could use:

- Postgres and pgvector for durable vector search.
- FAISS, Qdrant or Pinecone for specialized retrieval.
- LangChain, LlamaIndex or a custom orchestrator for multi-step workflows.
- OpenAI, Gemini, Hugging Face or local LLMs for generation.
- Structured traces, retrieval evaluation sets and prompt versioning.

This repository keeps those integrations out of scope so it remains safe, portable and easy to review.
