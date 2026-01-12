"""Tests for the RAG pipeline orchestration logic."""

import pytest

from backend.app.rag.pipeline import run_rag_pipeline


@pytest.mark.asyncio
async def test_pipeline_with_context(monkeypatch) -> None:
    """Ensure pipeline returns citations and confidence when context exists."""

    async def fake_retrieve(*args, **kwargs):
        return [
            {
                "text": "FastAPI is a framework.",
                "metadata": {"filename": "docs.pdf", "chunk_index": 0},
                "score": 0.95,
            }
        ]

    async def fake_generate(prompt, model_preference):
        return (
            "FastAPI is a web framework.",
            {
                "model_used": "fake",
                "input_tokens": 10,
                "output_tokens": 5,
                "cost_usd": 0.001,
            },
        )

    monkeypatch.setattr(
        "backend.app.rag.pipeline.retrieve_relevant_chunks",
        fake_retrieve,
    )
    monkeypatch.setattr(
        "backend.app.rag.pipeline.generate_answer",
        fake_generate,
    )

    result = await run_rag_pipeline(
        client_id="test-client",
        query="What is FastAPI?",
    )

    assert result["confidence"] > 0
    assert len(result["citations"]) == 1
    assert result["latency_ms"] >= 0


@pytest.mark.asyncio
async def test_pipeline_no_context(monkeypatch) -> None:
    """Ensure pipeline falls back correctly when no context is found."""

    async def fake_retrieve(*args, **kwargs):
        return []

    async def fake_generate(prompt, model_preference):
        return (
            "I don't have information about that.",
            {
                "model_used": "fake",
                "input_tokens": 0,
                "output_tokens": 0,
                "cost_usd": 0.0,
            },
        )

    monkeypatch.setattr(
        "backend.app.rag.pipeline.retrieve_relevant_chunks",
        fake_retrieve,
    )
    monkeypatch.setattr(
        "backend.app.rag.pipeline.generate_answer",
        fake_generate,
    )

    result = await run_rag_pipeline(
        client_id="test-client",
        query="Unknown",
    )

    assert result["confidence"] == 0.0
    assert result["citations"] == []
