"""Tests for the GLM runner's result normalization (import-free of mlx-vlm)."""

import pytest

from paper_siphon._glm_runner import _extract_text


def test_extract_text_from_str():
    assert _extract_text("hello") == "hello"


def test_extract_text_from_object_with_text_attr():
    class R:
        text = "world"

    assert _extract_text(R()) == "world"


def test_extract_text_unexpected_type_raises():
    class R:
        pass

    with pytest.raises(RuntimeError, match="unexpected"):
        _extract_text(R())
    with pytest.raises(RuntimeError, match="unexpected"):
        _extract_text(123)
