from app.agents.base import BaseAgent
from app.retrieval.vector_store import SearchResult


class AnswerAgent(BaseAgent):
    name = "answer-agent"

    def answer(self, question: str, contexts: list[SearchResult]) -> str:
        if not contexts:
            return "I do not have enough indexed context to answer this question."

        strongest = contexts[0].chunk
        supporting_sources = ", ".join(sorted({item.chunk.source for item in contexts}))
        return (
            f"Based on the retrieved demo context, the most relevant finding is: "
            f"{_compact(strongest.text)} "
            f"This answer is grounded in {len(contexts)} retrieved chunk(s) from {supporting_sources}."
        )


def _compact(text: str, limit: int = 320) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."

