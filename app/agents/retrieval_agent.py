from app.agents.base import BaseAgent
from app.retrieval.hybrid_search import HybridSearch
from app.retrieval.vector_store import SearchResult


class RetrievalAgent(BaseAgent):
    name = "retrieval-agent"

    def __init__(self, search_engine: HybridSearch) -> None:
        super().__init__()
        self.search_engine = search_engine

    def retrieve(self, question: str, top_k: int) -> list[SearchResult]:
        results = self.search_engine.search(question, top_k=top_k)
        self.logger.info("retrieved_chunks=%s top_k=%s", len(results), top_k)
        return results

