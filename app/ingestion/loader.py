from pathlib import Path

from app.schemas import DocumentInput


def load_sample_documents(sample_dir: Path = Path("sample_data")) -> list[DocumentInput]:
    documents: list[DocumentInput] = []
    for path in sorted(sample_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(
                DocumentInput(document_id=path.stem, text=text, source=f"sample_data/{path.name}")
            )
    return documents

