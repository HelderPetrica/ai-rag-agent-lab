from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastapi import FastAPI

from app.agents.answer_agent import AnswerAgent
from app.agents.ingest_agent import IngestionAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.validation_agent import ValidationAgent
from app.config import Settings, get_settings
from app.ingestion.loader import load_sample_documents
from app.logging_config import configure_logging
from app.retrieval.embeddings import DeterministicEmbeddingModel
from app.retrieval.hybrid_search import HybridSearch
from app.retrieval.vector_store import InMemoryVectorStore, SearchResult
from app.schemas import (
    HealthResponse,
    IndexRequest,
    IndexResponse,
    QueryRequest,
    QueryResponse,
    RetrievedContext,
)


@dataclass
class AppState:
    settings: Settings
    store: InMemoryVectorStore
    ingestion_agent: IngestionAgent
    retrieval_agent: RetrievalAgent
    answer_agent: AnswerAgent
    validation_agent: ValidationAgent


def build_state() -> AppState:
    settings = get_settings()
    configure_logging(settings.log_level)
    store = InMemoryVectorStore()
    embedding_model = DeterministicEmbeddingModel(dimensions=settings.embedding_dimensions)
    search_engine = HybridSearch(store=store, embedding_model=embedding_model)
    return AppState(
        settings=settings,
        store=store,
        ingestion_agent=IngestionAgent(
            store=store,
            embedding_model=embedding_model,
            max_chunk_tokens=settings.max_chunk_tokens,
            chunk_overlap_tokens=settings.chunk_overlap_tokens,
        ),
        retrieval_agent=RetrievalAgent(search_engine=search_engine),
        answer_agent=AnswerAgent(),
        validation_agent=ValidationAgent(),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.demo = build_state()
    yield


app = FastAPI(
    title="AI RAG Agent Lab",
    description="A sanitized portfolio API for document RAG, retrieval and agentic workflows.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root() -> dict[str, str | bool]:
    return {
        "name": "AI RAG Agent Lab",
        "status": "ready",
        "sanitized_demo": True,
        "description": "Sanitized FastAPI demo for document retrieval and agentic workflows.",
    }


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    state = _state()
    return HealthResponse(
        status="ok",
        service=state.settings.app_name,
        version=app.version,
        indexed_chunks=state.store.count(),
    )


@app.post("/documents/index", response_model=IndexResponse)
def index_documents(payload: IndexRequest) -> IndexResponse:
    state = _state()
    documents = payload.documents or []
    if payload.use_sample_data:
        documents.extend(load_sample_documents())

    indexed_documents, indexed_chunks, sources = state.ingestion_agent.ingest(documents)
    return IndexResponse(
        indexed_documents=indexed_documents,
        indexed_chunks=indexed_chunks,
        sources=sources,
    )


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    state = _state()
    contexts = state.retrieval_agent.retrieve(payload.question, payload.top_k)
    answer = state.answer_agent.answer(payload.question, contexts)
    confidence, warnings = state.validation_agent.validate(answer, contexts)
    return QueryResponse(
        answer=answer,
        retrieved_context=[_to_context(item) for item in contexts],
        sources=sorted({item.chunk.source for item in contexts}),
        confidence=confidence,
        warnings=warnings,
        metadata={
            "service": state.settings.app_name,
            "top_k": payload.top_k,
            "indexed_chunks": state.store.count(),
            "retrieved_chunks": len(contexts),
            "uses_external_llm": False,
        },
    )


def _state() -> AppState:
    return app.state.demo


def _to_context(result: SearchResult) -> RetrievedContext:
    chunk = result.chunk
    return RetrievedContext(
        chunk_id=chunk.chunk_id,
        document_id=chunk.document_id,
        source=chunk.source,
        text=chunk.text,
        score=result.score,
        metadata=chunk.metadata,
    )
