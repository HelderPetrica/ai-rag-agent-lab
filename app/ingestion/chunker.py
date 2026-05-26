import re
from dataclasses import dataclass


TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    text: str
    index: int
    token_count: int


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text)


def chunk_text(
    document_id: str,
    text: str,
    max_tokens: int = 90,
    overlap_tokens: int = 18,
) -> list[Chunk]:
    if max_tokens <= 0:
        raise ValueError("max_tokens must be greater than zero")
    if overlap_tokens >= max_tokens:
        raise ValueError("overlap_tokens must be smaller than max_tokens")

    tokens = tokenize(text)
    if not tokens:
        return []

    chunks: list[Chunk] = []
    start = 0
    index = 0
    step = max_tokens - overlap_tokens

    while start < len(tokens):
        window = tokens[start : start + max_tokens]
        chunk_text_value = _join_tokens(window)
        chunks.append(
            Chunk(
                chunk_id=f"{document_id}::chunk-{index}",
                document_id=document_id,
                text=chunk_text_value,
                index=index,
                token_count=len(window),
            )
        )
        index += 1
        start += step

    return chunks


def _join_tokens(tokens: list[str]) -> str:
    text = " ".join(tokens)
    return (
        text.replace(" ,", ",")
        .replace(" .", ".")
        .replace(" :", ":")
        .replace(" ;", ";")
        .replace(" )", ")")
        .replace("( ", "(")
    )

