"""Tests for text_reader module."""

from unittest.mock import patch

import pytest

from backend.app.ingestion.text_reader import extract_text


def test_extract_text_utf8_success():
    """UTF-8 decoding should succeed when bytes are valid."""
    data = "Hello UTF-8!".encode("utf-8")
    result = extract_text(data)
    assert result == "Hello UTF-8!"


def test_extract_text_latin1_fallback():
    """If UTF-8 fails, latin-1 fallback should be used."""
    bad_utf8 = b"\xff\xfeABC"  # invalid UTF-8

    # Patch our internal helpers
    with patch(
        "backend.app.ingestion.text_reader.decode_utf8",
        side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "bad utf-8"),
    ):
        with patch(
            "backend.app.ingestion.text_reader.decode_latin1",
            return_value="latin1 text",
        ):
            result = extract_text(bad_utf8)

    assert result == "latin1 text"


def test_extract_text_decode_failure():
    """If BOTH UTF-8 and latin-1 decoding fail, raise ValueError."""

    def fail_utf8(*args, **kwargs):  # noqa: ANN001, ANN003
        raise UnicodeDecodeError("utf-8", b"", 0, 1, "utf8 failed")

    def fail_latin1(*args, **kwargs):  # noqa: ANN001, ANN003
        raise UnicodeDecodeError("latin-1", b"", 0, 1, "latin1 failed")

    with patch(
        "backend.app.ingestion.text_reader.decode_utf8",
        side_effect=fail_utf8,
    ):
        with patch(
            "backend.app.ingestion.text_reader.decode_latin1",
            side_effect=fail_latin1,
        ):
            with pytest.raises(ValueError):
                extract_text(b"whatever")
