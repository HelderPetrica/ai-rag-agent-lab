# Retrieval Notes

## Dense Vector Embeddings

Dense embeddings convert text into numeric vectors. Similar text should land near similar vectors. This demo uses deterministic hashed vectors so the project can run without external services or API keys.

## FAISS, pgvector And Vector Databases

In production, the in-memory store could be replaced by:

- FAISS for local high-performance vector search.
- Postgres with pgvector when SQL metadata and vectors should live together.
- Qdrant or Pinecone when a managed or specialized vector database is preferred.

## Lexical Search

Lexical search matches exact terms. It is useful for precise keywords, codes, names and domain vocabulary.

## Hybrid Retrieval

Hybrid retrieval combines vector similarity and lexical overlap. This often performs better than using either signal alone, especially in document-heavy workflows where exact terms and semantic similarity both matter.

## top_k

`top_k` controls how many chunks return from retrieval. Low values reduce noise. Higher values may improve recall but can add irrelevant context.

## Reranking

Reranking reorders candidate chunks after an initial search. This demo uses a simple combined score. Production systems may use BM25, cross-encoders, learned rankers or domain-specific rules.

## Metadata And Traceability

Every returned chunk includes source, document id, chunk id and basic metadata. Traceable sources make generated answers easier to audit.

