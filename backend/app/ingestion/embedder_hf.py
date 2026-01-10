"""
Backup Embedding service using local HuggingFace MiniLM.
"""

from typing import List, Tuple
from backend.app.core.config import settings
from sentence_transformers import SentenceTransformer

from backend.app.utils.logger import logger


# Model setup (loaded once)
_MODEL_NAME = settings.HF_EBD_MODEL

try:
    _model = SentenceTransformer(_MODEL_NAME)
    logger.info(f"Loaded local embedding model: {_MODEL_NAME}")
except Exception as e:
    logger.critical(f"Failed to load embedding model: {e}")
    raise


# Public API

async def get_embeddings(
    texts: List[str],
) -> Tuple[List[List[float]], int]:
    """
    Generate embeddings locally.

    Returns:
        embeddings: List of vectors
        dim: Embedding dimension
        tokens: total tokens in encoded input
    """

    if not texts:
        return [], 0

    try:
        encoded_input = _model.tokenizer(texts, padding=False, truncation=False)
        total_tokens = sum(len(ids) for ids in encoded_input['input_ids'])
        embeddings = _model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
    except Exception as e:
        logger.error(f"Local embedding generation failed: {e}")
        return [], 0

    embeddings_list = embeddings.tolist()
    embedding_dim = len(embeddings_list[0])

    return embeddings_list, embedding_dim, total_tokens
