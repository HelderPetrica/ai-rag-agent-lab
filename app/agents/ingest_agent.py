from uuid import uuid4

from app.agents.base import BaseAgent
from app.ingestion.chunker import chunk_text
from app.retrieval.embeddings import DeterministicEmbeddingModel
from app.retrieval.vector_store import InMemoryVectorStore
from app.schemas import DocumentInput


class IngestionAgent(BaseAgent):
    name = "ingestion-agent"

    def __init__(
        self,
        store: InMemoryVectorStore,
        embedding_model: DeterministicEmbeddingModel,
        max_chunk_tokens: int,
        chunk_overlap_tokens: int,
    ) -> None:
        super().__init__()
        self.store = store
        self.embedding_model = embedding_model
        self.max_chunk_tokens = max_chunk_tokens
        self.chunk_overlap_tokens = chunk_overlap_tokens

    def ingest(self, documents: list[DocumentInput]) -> tuple[int, int, list[str]]:
        indexed_chunks = 0
        sources: list[str] = []

        for document in documents:
            document_id = document.document_id or f"doc-{uuid4().hex[:12]}"
            chunks = chunk_text(
                document_id=document_id,
                text=document.text,
                max_tokens=self.max_chunk_tokens,
                overlap_tokens=self.chunk_overlap_tokens,
            )
            embeddings = [self.embedding_model.embed(chunk.text) for chunk in chunks]
            self.store.add_chunks(chunks=chunks, source=document.source, embeddings=embeddings)
            indexed_chunks += len(chunks)
            sources.append(document.source)

        self.logger.info("indexed_documents=%s indexed_chunks=%s", len(documents), indexed_chunks)
        return len(documents), indexed_chunks, sorted(set(sources))

