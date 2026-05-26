from pydantic import BaseModel, Field


class DocumentInput(BaseModel):
    document_id: str | None = Field(default=None, description="Optional external document id.")
    text: str = Field(min_length=20, description="Plain text document content.")
    source: str = Field(default="inline", description="Source label shown in retrieval results.")


class IndexRequest(BaseModel):
    documents: list[DocumentInput] | None = None
    use_sample_data: bool = True


class IndexResponse(BaseModel):
    indexed_documents: int
    indexed_chunks: int
    sources: list[str]


class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=3, ge=1, le=8)


class RetrievedContext(BaseModel):
    chunk_id: str
    document_id: str
    source: str
    text: str
    score: float
    metadata: dict[str, str | int | float]


class QueryResponse(BaseModel):
    answer: str
    retrieved_context: list[RetrievedContext]
    sources: list[str]
    confidence: float
    warnings: list[str]


class HealthResponse(BaseModel):
    status: str
    indexed_chunks: int

