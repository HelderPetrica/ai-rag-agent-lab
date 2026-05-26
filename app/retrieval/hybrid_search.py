import re
from collections import Counter

from app.retrieval.embeddings import DeterministicEmbeddingModel
from app.retrieval.vector_store import InMemoryVectorStore, SearchResult


WORD_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


class HybridSearch:
    def __init__(self, store: InMemoryVectorStore, embedding_model: DeterministicEmbeddingModel) -> None:
        self.store = store
        self.embedding_model = embedding_model

    def search(self, query: str, top_k: int = 3, document_id: str | None = None) -> list[SearchResult]:
        query_embedding = self.embedding_model.embed(query)
        vector_results = self.store.search(
            query_embedding,
            top_k=max(top_k * 3, top_k),
            document_id=document_id,
        )
        query_terms = _term_counts(query)

        reranked: list[SearchResult] = []
        for result in vector_results:
            lexical = _lexical_overlap(query_terms, _term_counts(result.chunk.text))
            combined_score = round((0.72 * result.score) + (0.28 * lexical), 4)
            reranked.append(SearchResult(chunk=result.chunk, score=combined_score))

        return sorted(reranked, key=lambda item: item.score, reverse=True)[:top_k]


def _term_counts(text: str) -> Counter[str]:
    return Counter(match.group(0).lower() for match in WORD_PATTERN.finditer(text))


def _lexical_overlap(left: Counter[str], right: Counter[str]) -> float:
    if not left:
        return 0.0
    matches = sum(min(count, right.get(term, 0)) for term, count in left.items())
    return matches / sum(left.values())
