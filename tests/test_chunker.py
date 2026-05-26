import pytest

from app.ingestion.chunker import chunk_text


def test_chunk_text_creates_overlapping_chunks() -> None:
    text = " ".join(f"token{i}" for i in range(30))

    chunks = chunk_text("demo", text, max_tokens=10, overlap_tokens=2)

    assert len(chunks) == 4
    assert chunks[0].chunk_id == "demo::chunk-0"
    assert chunks[1].token_count == 10
    assert "token8" in chunks[1].text
    assert all(chunk.text for chunk in chunks)
    assert all(chunk.token_count <= 10 for chunk in chunks)


def test_chunk_text_returns_empty_list_for_empty_text() -> None:
    assert chunk_text("empty", "", max_tokens=10, overlap_tokens=2) == []


def test_chunk_text_keeps_short_text_in_single_chunk() -> None:
    chunks = chunk_text("short", "A compact document.", max_tokens=20, overlap_tokens=5)

    assert len(chunks) == 1
    assert chunks[0].document_id == "short"
    assert chunks[0].index == 0


def test_chunk_text_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        chunk_text("demo", "short text", max_tokens=10, overlap_tokens=10)
