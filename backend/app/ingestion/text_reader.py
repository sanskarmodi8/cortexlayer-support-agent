"""Text extraction utilities for TXT/MD files."""

from backend.app.utils.logger import logger


def decode_utf8(data: bytes) -> str:
    """Wrapper used so tests can monkeypatch utf-8 decode."""
    return data.decode("utf-8")


def decode_latin1(data: bytes) -> str:
    """Wrapper used so tests can monkeypatch latin-1 decode."""
    return data.decode("latin-1")


def extract_text(file_bytes: bytes) -> str:
    """Extract text from TXT/MD files using UTF-8 with latin-1 fallback."""
    # Try UTF-8
    try:
        text = decode_utf8(file_bytes)
        logger.info("Text extracted using UTF-8 decoding")
        return text.strip()
    except UnicodeDecodeError:
        logger.warning("UTF-8 decoding failed, falling back to latin-1")

    # Fallback: Latin-1
    try:
        text = decode_latin1(file_bytes)
        logger.info("Text extracted using latin-1 decoding")
        return text.strip()
    except Exception as err:  # noqa: BLE001
        logger.error(f"Failed to decode text file: {err}")
        raise ValueError("Failed to decode text file") from err
