from pathlib import Path


README = Path(__file__).resolve().parents[1] / "README.md"


def test_readme_documents_real_commands_and_endpoints() -> None:
    content = README.read_text(encoding="utf-8")

    assert "uvicorn app.main:app --reload" in content
    assert "docker compose up --build" in content
    assert "GET `/health`" in content
    assert "POST `/documents/index`" in content
    assert "POST `/query`" in content
