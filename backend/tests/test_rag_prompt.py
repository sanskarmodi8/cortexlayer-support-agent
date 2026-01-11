"""Tests for RAG prompt construction and query schemas."""

from backend.app.rag.prompt import (
    build_fallback_prompt,
    build_rag_prompt,
)
from backend.app.schemas.query import (
    Citation,
    QueryRequest,
    QueryResponse,
)


def test_build_rag_prompt_contains_context() -> None:
    """Ensure RAG prompt includes context and metadata."""
    chunks = [
        {
            "text": "FastAPI is a modern web framework.",
            "metadata": {"filename": "docs.pdf", "chunk_index": 0},
        }
    ]

    prompt = build_rag_prompt("What is FastAPI?", chunks)

    assert "FastAPI is a modern web framework." in prompt
    assert "[Document: docs.pdf, Chunk: 0]" in prompt
    assert "USER QUESTION:" in prompt


def test_build_fallback_prompt() -> None:
    """Ensure fallback prompt handles unknown queries gracefully."""
    prompt = build_fallback_prompt("Unknown question")

    assert "don't have specific information" in prompt.lower()


def test_query_request_schema() -> None:
    """Ensure QueryRequest schema validates correctly."""
    req = QueryRequest(query="Hello", conversation_id=None)
    assert req.query == "Hello"


def test_query_response_schema() -> None:
    """Ensure QueryResponse schema accepts valid data."""
    response = QueryResponse(
        answer="Test answer",
        citations=[
            Citation(
                document="doc.pdf",
                chunk_index=1,
                relevance_score=0.9,
            )
        ],
        confidence=0.9,
        latency_ms=120,
    )

    assert response.confidence == 0.9
