from functools import lru_cache
from os import getenv

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = Field(default="AI RAG Agent Lab")
    app_env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    embedding_dimensions: int = Field(default=64, ge=8, le=512)
    max_chunk_tokens: int = Field(default=90, ge=20, le=500)
    chunk_overlap_tokens: int = Field(default=18, ge=0, le=100)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=getenv("APP_NAME", "AI RAG Agent Lab"),
        app_env=getenv("APP_ENV", "development"),
        log_level=getenv("LOG_LEVEL", "INFO"),
        embedding_dimensions=int(getenv("EMBEDDING_DIMENSIONS", "64")),
        max_chunk_tokens=int(getenv("MAX_CHUNK_TOKENS", "90")),
        chunk_overlap_tokens=int(getenv("CHUNK_OVERLAP_TOKENS", "18")),
    )

