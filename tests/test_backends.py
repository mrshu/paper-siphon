"""Tests for VLM backend selection and CLI escalation wiring.

Heavy backends (GLM-OCR / marker) are mocked so these stay fast and dep-free.
"""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from paper_siphon import backends
from paper_siphon.cli import main


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


# --- backend selection ---


def test_backend_name_apple_silicon_uses_glm():
    with patch.object(backends, "is_apple_silicon", return_value=True):
        assert backends.vlm_backend_name(use_mlx=True) == "GLM-OCR (MLX)"


def test_backend_name_no_mlx_uses_marker_even_on_mac():
    with patch.object(backends, "is_apple_silicon", return_value=True):
        assert backends.vlm_backend_name(use_mlx=False) == "marker"


def test_backend_name_non_mac_uses_marker():
    with patch.object(backends, "is_apple_silicon", return_value=False):
        assert backends.vlm_backend_name(use_mlx=True) == "marker"


def test_vlm_convert_dispatches_to_glm_on_apple_silicon():
    with patch.object(backends, "is_apple_silicon", return_value=True), \
         patch.object(backends, "glm_ocr_convert", return_value="GLM") as glm, \
         patch.object(backends, "marker_convert", return_value="MK") as mk:
        assert backends.vlm_convert("x.pdf", use_mlx=True) == "GLM"
        glm.assert_called_once()
        mk.assert_not_called()


def test_glm_requires_uv_on_path():
    with patch.object(backends.shutil, "which", return_value=None):
        with pytest.raises(ImportError, match="uv"):
            backends.glm_ocr_convert("x.pdf")


def test_marker_requires_uv_on_path():
    with patch.object(backends.shutil, "which", return_value=None):
        with pytest.raises(ImportError, match="uv"):
            backends.marker_convert("x.pdf")


def test_vlm_convert_dispatches_to_marker_when_no_mlx():
    with patch.object(backends, "is_apple_silicon", return_value=True), \
         patch.object(backends, "glm_ocr_convert", return_value="GLM") as glm, \
         patch.object(backends, "marker_convert", return_value="MK") as mk:
        assert backends.vlm_convert("x.pdf", use_mlx=False) == "MK"
        mk.assert_called_once()
        glm.assert_not_called()


# --- CLI wiring + escalation ---

GARBLED = ("## ❚■●❊❘ ▼❛♥♥❤❡✐♠\n\n❊①/a116❡♥❞❡❞ ❉❡/a115❝\n" * 30)


def _pdf(tmp_path):
    p = tmp_path / "paper.pdf"
    p.write_text("dummy")  # resolve_source only checks existence
    return p


def test_vlm_flag_uses_vlm_backend(cli_runner, tmp_path):
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.vlm_convert", return_value="# VLM out") as vc:
        result = cli_runner.invoke(
            main, [str(_pdf(tmp_path)), "-o", str(out), "--vlm"]
        )
    assert result.exit_code == 0, result.output
    vc.assert_called_once()
    assert "VLM out" in out.read_text()


def test_default_does_not_escalate_on_clean_output(cli_runner, tmp_path):
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.convert_standard", return_value="# Clean paper\n\nText."), \
         patch("paper_siphon.cli.vlm_convert", return_value="VLM") as vc:
        result = cli_runner.invoke(main, [str(_pdf(tmp_path)), "-o", str(out)])
    assert result.exit_code == 0, result.output
    vc.assert_not_called()
    assert "Clean paper" in out.read_text()


def test_default_escalates_on_garbled_output(cli_runner, tmp_path):
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.convert_standard", return_value=GARBLED), \
         patch("paper_siphon.cli.vlm_convert", return_value="# Recovered") as vc:
        result = cli_runner.invoke(main, [str(_pdf(tmp_path)), "-o", str(out)])
    assert result.exit_code == 0, result.output
    vc.assert_called_once()
    assert "garbled" in result.output
    assert "Recovered" in out.read_text()


def test_no_escalate_keeps_garbled_output(cli_runner, tmp_path):
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.convert_standard", return_value=GARBLED), \
         patch("paper_siphon.cli.vlm_convert", return_value="VLM") as vc:
        result = cli_runner.invoke(
            main, [str(_pdf(tmp_path)), "-o", str(out), "--no-escalate"]
        )
    assert result.exit_code == 0, result.output
    vc.assert_not_called()


def test_missing_backend_dependency_errors_cleanly(cli_runner, tmp_path):
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.vlm_convert", side_effect=ImportError("install paper-siphon[marker]")):
        result = cli_runner.invoke(
            main, [str(_pdf(tmp_path)), "-o", str(out), "--vlm"]
        )
    assert result.exit_code == 1
    assert "marker" in result.output
