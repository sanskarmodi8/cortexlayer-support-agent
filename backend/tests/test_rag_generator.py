"""Tests for the RAG LLM answer generator with provider fallback."""

import pytest

from backend.app.rag.generator import generate_answer


@pytest.mark.asyncio
async def test_generate_answer_returns_text(monkeypatch) -> None:
    """Ensure generate_answer returns text and correct usage stats."""

    class FakeResponse:
        class Choice:
            class Message:
                content = "Test answer"

            message = Message()

        choices = [Choice()]

        class Usage:
            prompt_tokens = 10
            completion_tokens = 5

        usage = Usage()

    def fake_groq_call(prompt, max_tokens):
        return FakeResponse()

    monkeypatch.setattr(
        "backend.app.rag.generator._call_groq",
        fake_groq_call,
    )

    answer, stats = await generate_answer("Test prompt")

    assert answer == "Test answer"
    assert stats["input_tokens"] == 10
    assert stats["output_tokens"] == 5
    assert stats["cost_usd"] > 0
