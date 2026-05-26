import sqlite3
from dataclasses import dataclass

from app.ingestion.chunker import Chunk
from app.retrieval.embeddings import cosine_similarity


@dataclass
class StoredChunk:
    chunk_id: str
    document_id: str
    source: str
    text: str
    embedding: list[float]
    metadata: dict[str, str | int | float]


@dataclass
class SearchResult:
    chunk: StoredChunk
    score: float


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: dict[str, StoredChunk] = {}
        self._db = sqlite3.connect(":memory:", check_same_thread=False)
        self._create_schema()

    def add_chunks(self, chunks: list[Chunk], source: str, embeddings: list[list[float]]) -> None:
        for chunk, embedding in zip(chunks, embeddings):
            stored = StoredChunk(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                source=source,
                text=chunk.text,
                embedding=embedding,
                metadata={"chunk_index": chunk.index, "token_count": chunk.token_count},
            )
            self._chunks[stored.chunk_id] = stored
            self._db.execute(
                """
                insert or replace into chunk_metadata
                (chunk_id, document_id, source, chunk_index, token_count)
                values (?, ?, ?, ?, ?)
                """,
                (
                    stored.chunk_id,
                    stored.document_id,
                    stored.source,
                    chunk.index,
                    chunk.token_count,
                ),
            )
        self._db.commit()

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
        document_id: str | None = None,
    ) -> list[SearchResult]:
        results = [
            SearchResult(chunk=chunk, score=cosine_similarity(query_embedding, chunk.embedding))
            for chunk in self._chunks.values()
            if document_id is None or chunk.document_id == document_id
        ]
        return sorted(results, key=lambda item: item.score, reverse=True)[:top_k]

    def count(self) -> int:
        return len(self._chunks)

    def sources(self) -> list[str]:
        rows = self._db.execute("select distinct source from chunk_metadata order by source").fetchall()
        return [row[0] for row in rows]

    def clear(self) -> None:
        self._chunks.clear()
        self._db.execute("delete from chunk_metadata")
        self._db.commit()

    def _create_schema(self) -> None:
        self._db.execute(
            """
            create table if not exists chunk_metadata (
                chunk_id text primary key,
                document_id text not null,
                source text not null,
                chunk_index integer not null,
                token_count integer not null
            )
            """
        )
        self._db.commit()
