"""
Tests for embed_and_index ingestion pipeline.
"""

from unittest.mock import patch
import pytest

from backend.app.ingestion.embedder import embed_and_index


@pytest.mark.asyncio
@patch("backend.app.ingestion.embedder.get_embeddings")
@patch("backend.app.core.vectorstore.add_to_index")
async def test_embed_and_index_success(
    mock_add_to_index,
    mock_get_embeddings,
):
    """
    Ensure embeddings are generated and passed correctly to FAISS.
    """

    fake_embeddings = [[0.0] * 1536]

    mock_get_embeddings.return_value = (
        fake_embeddings,
        {"tokens": 5, "cost_usd": 0.0001, "model": "test-model"},
    )

    chunks = [
        {
            "text": "Reset your password using the email link.",
            "metadata": {"filename": "test.txt"},
        }
    ]

    usage = await embed_and_index(
        client_id="test-client",
        chunks=chunks,
        document_id="doc-123",
    )

    mock_add_to_index.assert_called_once()

    assert usage["tokens"] == 5
    assert usage["cost_usd"] == 0.0001
    assert usage["model"] == "test-model"


@pytest.mark.asyncio
async def test_embed_and_index_empty_chunks():
    """
    Empty chunks should short-circuit without errors.
    """

    usage = await embed_and_index(
        client_id="test-client",
        chunks=[],
        document_id="doc-empty",
    )

    assert usage["tokens"] == 0
    assert usage["cost_usd"] == 0.0
