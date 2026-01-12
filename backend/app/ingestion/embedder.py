"""Embedding service for generating vector embeddings for text chunks."""

from typing import Dict, List, Tuple

from openai import OpenAI

from backend.app.core.config import settings
from backend.app.ingestion.embedder_hf import get_embeddings as ge
from backend.app.utils.logger import logger

# Initialize OpenAI client once
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


async def get_embeddings(
    texts: List[str],
) -> Tuple[List[List[float]], Dict]:
    """
    Generate embeddings.
    Falls back to HF embeddings.
    """

    try:
        response = openai_client.embeddings.create(
            model=settings.OPENAI_EBD_MODEL,
            input=texts
        )

        embeddings = [item.embedding for item in response.data]

        total_tokens = response.usage.total_tokens
        cost = (total_tokens / 1_000_000) * 0.02

        logger.info(
            f"OpenAI embeddings generated: {len(embeddings)} | "
            f"Tokens: {total_tokens} | Cost: ${cost:.6f}"
        )

        return embeddings, {
            "tokens": total_tokens,
            "cost_usd": cost,
            "model": "text-embedding-3-small"
        }

    except Exception as e:
        logger.error(
            "OpenAI Embedding API unavailable. "
            "Using HF embeddings temporarily."
        )
        logger.error(str(e))

        embeddings, _, tokens = ge(texts)

        return embeddings, {
            "tokens": tokens,
            "cost_usd": 0.0,
            "model": settings.HF_EBD_MODEL
        }

async def embed_chunks(chunks: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Attach embeddings directly to chunks.
    Kept as a thin public helper for tests and legacy compatibility.
    """

    if not chunks:
        return [], {"tokens": 0, "cost_usd": 0.0}

    texts = [chunk["text"] for chunk in chunks]

    embeddings, usage_stats = await get_embeddings(texts)

    for idx, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[idx]
        chunk["embedding_model"] = usage_stats.get("model", "unknown")

    return chunks, usage_stats


async def embed_and_index(
    client_id: str,
    chunks: List[Dict],
    document_id: str
) -> Dict:
    """
    Full ingestion pipeline:
    chunks → embeddings → FAISS
    """

    from backend.app.core.vectorstore import add_to_index

    if not chunks:
        logger.warning("No chunks provided for embedding")
        return {"tokens": 0, "cost_usd": 0.0}

    texts = [chunk["text"] for chunk in chunks]

    embeddings, usage_stats = await get_embeddings(texts)

    metadata_list = []
    for idx, chunk in enumerate(chunks):
        metadata_list.append({
            "text": chunk["text"],
            "metadata": chunk.get("metadata", {}),
            "document_id": document_id,
            "chunk_index": idx
        })

    add_to_index(
        client_id=client_id,
        embeddings=embeddings,
        metadata_list=metadata_list
    )

    logger.info(
        f"Indexed {len(embeddings)} chunks "
        f"client={client_id} document={document_id}"
    )

    return usage_stats
