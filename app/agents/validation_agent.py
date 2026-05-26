from app.agents.base import BaseAgent
from app.retrieval.vector_store import SearchResult


class ValidationAgent(BaseAgent):
    name = "validation-agent"

    def validate(self, answer: str, contexts: list[SearchResult]) -> tuple[float, list[str]]:
        warnings: list[str] = []
        if not contexts:
            warnings.append("No context was retrieved. The answer is not grounded.")
            return 0.0, warnings

        best_score = max(item.score for item in contexts)
        confidence = max(0.0, min(0.98, round(0.55 + best_score / 2, 2)))

        if best_score < 0.2:
            warnings.append("Low retrieval score. Review source documents before relying on this answer.")
        if "do not have enough" in answer.lower():
            warnings.append("The answer agent reported insufficient context.")

        return confidence, warnings

