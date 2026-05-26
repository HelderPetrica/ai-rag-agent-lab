from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_FILE_NAMES = {".env"}
FORBIDDEN_PATTERNS = [
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bgh[oprs]_[A-Za-z0-9_]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
]


def test_no_obvious_secret_files_are_committed() -> None:
    committed_files = _tracked_like_files()

    assert ".env.example" in committed_files
    assert not (FORBIDDEN_FILE_NAMES & committed_files)


def test_no_obvious_secret_patterns_are_present() -> None:
    for path in _text_files():
        content = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_PATTERNS:
            assert not pattern.search(content), f"Potential secret pattern in {path}"


def test_no_private_product_name_is_used_in_code_or_docs() -> None:
    private_product_name = "Auto" + "Juris"
    allowed = {"tests/test_security.py"}
    for path in _text_files():
        relative = path.relative_to(ROOT).as_posix()
        if relative in allowed:
            continue
        assert private_product_name not in path.read_text(encoding="utf-8")


def _tracked_like_files() -> set[str]:
    ignored_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", "logs"}
    return {
        path.name
        for path in ROOT.rglob("*")
        if path.is_file() and not (set(path.parts) & ignored_dirs)
    }


def _text_files() -> list[Path]:
    ignored_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", "logs"}
    extensions = {".py", ".md", ".txt", ".yml", ".yaml", ".json", ".example", ".dockerignore"}
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in extensions
        and not (set(path.parts) & ignored_dirs)
    ]
