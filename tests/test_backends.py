"""Tests for VLM backend selection and CLI escalation wiring.

Heavy backends (GLM-OCR / marker) are mocked so these stay fast and dep-free.
"""

from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from paper_siphon import backends
from paper_siphon.backends import VlmBackendError
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
        with pytest.raises(VlmBackendError, match="uv"):
            backends.glm_ocr_convert("x.pdf")


def test_marker_requires_uv_on_path():
    with patch.object(backends.shutil, "which", return_value=None):
        with pytest.raises(VlmBackendError, match="uv"):
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


def test_escalation_failure_keeps_standard_output(cli_runner, tmp_path):
    # RAVF001: if auto-escalation's VLM retry fails, keep the standard output
    # instead of aborting with no file.
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.convert_standard", return_value=GARBLED), \
         patch("paper_siphon.cli.vlm_convert", side_effect=VlmBackendError("uv not found")):
        result = cli_runner.invoke(main, [str(_pdf(tmp_path)), "-o", str(out)])
    assert result.exit_code == 0, result.output
    assert "escalation failed" in result.output.lower()
    assert out.exists()
    assert "❚" in out.read_text()  # the standard (garbled) output was still written


def test_escalation_does_not_swallow_programmer_bugs(cli_runner, tmp_path):
    # A non-VlmBackendError (e.g. a bug in the backend) must NOT be masked as a
    # successful standard conversion — it should surface as a failure.
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.convert_standard", return_value=GARBLED), \
         patch("paper_siphon.cli.vlm_convert", side_effect=TypeError("bug")):
        result = cli_runner.invoke(main, [str(_pdf(tmp_path)), "-o", str(out)])
    assert result.exit_code == 1


def test_marker_command_forces_ocr(tmp_path):
    captured = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        td = cmd[cmd.index("--output_dir") + 1]
        stem = Path(cmd[cmd.index("marker_single") + 1]).stem
        d = Path(td) / stem
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{stem}.md").write_text("# ok")
        class R:
            returncode = 0
            stderr = ""
        return R()

    with patch.object(backends, "is_apple_silicon", return_value=False), \
         patch.object(backends.shutil, "which", return_value="/usr/bin/uv"), \
         patch.object(backends.subprocess, "run", fake_run):
        md = backends.marker_convert(Path("paper.pdf"))
    assert md == "# ok"
    assert "--force_ocr" in captured["cmd"]
    assert "--isolated" in captured["cmd"]


def test_output_written_as_utf8(cli_runner, tmp_path):
    # non-ASCII VLM/standard output must round-trip regardless of locale
    out = tmp_path / "o.md"
    text = "Estimate 𝔼[x] under 𝒩(0, I); α → β. Ünïcödé."
    with patch("paper_siphon.cli.convert_standard", return_value=text):
        result = cli_runner.invoke(main, [str(_pdf(tmp_path)), "-o", str(out)])
    assert result.exit_code == 0, result.output
    assert out.read_text(encoding="utf-8") == text.strip() + "\n" or text in out.read_text(encoding="utf-8")


def test_timeout_includes_stderr_tail():
    import subprocess as sp

    def boom(cmd, **kwargs):
        raise sp.TimeoutExpired(cmd, 1, stderr=b"download stalled at 70%")

    with patch.object(backends.shutil, "which", return_value="/usr/bin/uv"), \
         patch.object(backends.subprocess, "run", boom):
        with pytest.raises(VlmBackendError, match="stalled at 70"):
            backends.glm_ocr_convert(Path("paper.pdf"))


def test_marker_empty_output_raises(tmp_path):
    # an empty marker result is an operational failure, not usable output
    def fake_run(cmd, **kwargs):
        td = cmd[cmd.index("--output_dir") + 1]
        stem = Path(cmd[cmd.index("marker_single") + 1]).stem
        d = Path(td) / stem
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{stem}.md").write_text("   \n")  # whitespace only
        class R:
            returncode = 0
            stderr = ""
        return R()

    with patch.object(backends, "is_apple_silicon", return_value=False), \
         patch.object(backends.shutil, "which", return_value="/usr/bin/uv"), \
         patch.object(backends.subprocess, "run", fake_run):
        with pytest.raises(VlmBackendError, match="empty"):
            backends.marker_convert(Path("paper.pdf"))


def test_backend_wraps_oserror_as_vlmbackenderror():
    def boom(cmd, **kwargs):
        raise OSError("exec failed")

    with patch.object(backends.shutil, "which", return_value="/usr/bin/uv"), \
         patch.object(backends.subprocess, "run", boom):
        with pytest.raises(VlmBackendError, match="could not start"):
            backends.glm_ocr_convert(Path("paper.pdf"))


def test_missing_backend_dependency_errors_cleanly(cli_runner, tmp_path):
    out = tmp_path / "o.md"
    with patch("paper_siphon.cli.vlm_convert", side_effect=VlmBackendError("install paper-siphon[marker]")):
        result = cli_runner.invoke(
            main, [str(_pdf(tmp_path)), "-o", str(out), "--vlm"]
        )
    assert result.exit_code == 1
    assert "marker" in result.output
