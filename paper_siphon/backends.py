"""VLM backends for the ``--vlm`` path.

- GLM-OCR (``mlx-community/GLM-OCR-bf16``) on Apple Silicon — the backend
  benchmark winner.
- marker (``marker-pdf``) on other platforms.

Both run in an **isolated** ``uv run --isolated --no-project --with`` environment
rather than the main process. This is deliberate: mlx-vlm and marker pull a
newer ``transformers`` that breaks Docling's default-pipeline layout model on
MPS, so they must not share paper-siphon's environment. ``--isolated`` forces a
fresh venv (``--no-project`` alone would still reuse a discovered ``.venv``), so
the isolation holds even when paper-siphon is run from inside a project.
The ``--vlm`` path requires ``uv`` on PATH (every ``uvx paper-siphon`` user has it).

Backends return *raw* Markdown; the CLI applies ``clean_markdown`` uniformly.
Operational failures raise ``VlmBackendError`` so callers can distinguish an
expected backend problem (missing uv, download/timeout, subprocess failure)
from a programmer bug, which must surface rather than be swallowed.
"""

from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path

# generous ceiling — a long PDF through a per-page VLM can take a while
_VLM_TIMEOUT = 7200
_RUNNER = Path(__file__).resolve().parent / "_glm_runner.py"


class VlmBackendError(RuntimeError):
    """An expected, operational failure of a VLM backend (missing uv, model
    download/network failure, timeout, subprocess crash, empty output)."""


def is_apple_silicon() -> bool:
    return platform.system() == "Darwin" and platform.machine() == "arm64"


def _select_backend(use_mlx: bool) -> str:
    """Single source of truth for which backend the VLM path uses, so dispatch
    and the displayed name can never diverge."""
    return "glm-ocr" if (use_mlx and is_apple_silicon()) else "marker"


def _require_uv() -> None:
    if shutil.which("uv") is None:
        raise VlmBackendError(
            "The --vlm backend runs in an isolated environment and requires "
            "'uv' on PATH. Install uv (https://docs.astral.sh/uv/) or run "
            "paper-siphon via 'uvx paper-siphon'."
        )


def _run_isolated(cmd: list[str], backend: str) -> subprocess.CompletedProcess:
    """Run an isolated `uv run` backend command, normalizing failures/timeouts
    to VlmBackendError with a useful stderr tail."""
    try:
        proc = subprocess.run(
            # errors="replace" so a stray non-UTF-8 byte in stdout/stderr can
            # never raise UnicodeDecodeError mid-capture — that would escape the
            # VlmBackendError contract and abort auto-escalation instead of
            # falling back to the standard output.
            cmd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=_VLM_TIMEOUT,
        )
    except subprocess.TimeoutExpired as e:
        # TimeoutExpired.stderr is bytes even under text=True; decode it so the
        # diagnostic tail is not silently dropped.
        err = e.stderr
        if isinstance(err, (bytes, bytearray)):
            err = err.decode("utf-8", "replace")
        tail = (err or "")[-1200:] if isinstance(err, str) else ""
        raise VlmBackendError(
            f"{backend} backend timed out after {_VLM_TIMEOUT}s"
            + (f":\n{tail}" if tail else "")
        ) from e
    except OSError as e:  # exec failure, etc. — an operational backend failure
        raise VlmBackendError(f"{backend} backend could not start: {e}") from e
    if proc.returncode != 0:
        raise VlmBackendError(f"{backend} backend failed:\n{proc.stderr[-1200:]}")
    return proc


def glm_ocr_convert(pdf_path: Path) -> str:
    """GLM-OCR via an isolated uv env (mlx-vlm + pymupdf). Returns raw Markdown.

    First run provisions the ephemeral env and downloads the model (~2 GB);
    both are cached for subsequent runs.
    """
    _require_uv()
    proc = _run_isolated(
        [
            # Pin to a known-good interpreter (uv fetches it if absent) so the
            # ephemeral env is reproducible rather than tracking whatever
            # interpreter uv would otherwise pick (possibly too new for the
            # mlx-vlm/torch stack).
            "uv", "run", "--isolated", "--no-project", "--python", "3.12",
            "--with", "mlx-vlm>=0.3.11,<0.7", "--with", "pymupdf",
            "python", str(_RUNNER), str(pdf_path),
        ],
        backend="GLM-OCR",
    )
    if not proc.stdout.strip():
        raise VlmBackendError("GLM-OCR backend produced no output")
    return proc.stdout


def marker_convert(pdf_path: Path) -> str:
    """marker via an isolated uv env. Returns raw Markdown."""
    import tempfile

    _require_uv()
    with tempfile.TemporaryDirectory() as td:
        _run_isolated(
            [
                # Same known-good-interpreter pin as the GLM path for
                # reproducibility of the isolated marker/torch env.
                "uv", "run", "--isolated", "--no-project", "--python", "3.12",
                "--with", "marker-pdf>=1.0,<2",
                "marker_single", str(pdf_path),
                "--output_dir", td,
                "--output_format", "markdown",
                "--disable_image_extraction",
                # The VLM path is invoked precisely when the fast pipeline
                # produced bad text (garbled encoding) or the user forced it;
                # force OCR so marker re-reads the page instead of reusing the
                # same corrupted embedded text. (marker's own guidance.)
                "--force_ocr",
            ],
            backend="marker",
        )
        stem = Path(pdf_path).stem
        out = Path(td) / stem / f"{stem}.md"
        if not out.exists():
            mds = sorted(Path(td).rglob("*.md"), key=lambda p: -p.stat().st_size)
            if not mds:
                raise VlmBackendError("marker backend produced no Markdown output")
            out = mds[0]
        md = out.read_text(encoding="utf-8")
        # An empty result must be an operational failure (like GLM's empty-stdout
        # guard) so auto-escalation falls back to the standard output instead of
        # silently overwriting it with nothing.
        if not md.strip():
            raise VlmBackendError("marker backend produced empty Markdown")
        return md


def vlm_convert(pdf_path: Path, use_mlx: bool = True) -> str:
    """Dispatch the VLM path: GLM-OCR on Apple Silicon (unless disabled),
    marker otherwise. Returns raw Markdown."""
    if _select_backend(use_mlx) == "glm-ocr":
        return glm_ocr_convert(pdf_path)
    return marker_convert(pdf_path)


def vlm_backend_name(use_mlx: bool = True) -> str:
    return "GLM-OCR (MLX)" if _select_backend(use_mlx) == "glm-ocr" else "marker"
