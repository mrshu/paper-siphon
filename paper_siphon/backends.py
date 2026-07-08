"""VLM backends for the ``--vlm`` path.

- GLM-OCR (``mlx-community/GLM-OCR-bf16``) on Apple Silicon — the backend
  benchmark winner.
- marker (``marker-pdf``) on other platforms.

Both run in an **isolated** ``uv run --with`` environment rather than the main
process. This is deliberate: mlx-vlm and marker pull a newer ``transformers``
that breaks Docling's default-pipeline layout model on MPS, so they must not
share paper-siphon's environment. Isolation keeps the fast default pipeline
working while still offering a high-quality VLM path. The ``--vlm`` path
therefore requires ``uv`` on PATH (every ``uvx paper-siphon`` user has it).

Backends return *raw* Markdown; the CLI applies ``clean_markdown`` uniformly.
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

# generous ceiling — a long PDF through a per-page VLM can take a while
_VLM_TIMEOUT = 7200
_RUNNER = Path(__file__).resolve().parent / "_glm_runner.py"


def is_apple_silicon() -> bool:
    return platform.system() == "Darwin" and platform.machine() == "arm64"


def _require_uv() -> None:
    if shutil.which("uv") is None:
        raise ImportError(
            "The --vlm backend runs in an isolated environment and requires "
            "'uv' on PATH. Install uv (https://docs.astral.sh/uv/) or run "
            "paper-siphon via 'uvx paper-siphon'."
        )


def glm_ocr_convert(pdf_path: Path) -> str:
    """GLM-OCR via an isolated uv env (mlx-vlm + pymupdf). Returns raw Markdown.

    First run provisions the ephemeral env and downloads the model (~2 GB);
    both are cached for subsequent runs.
    """
    _require_uv()
    proc = subprocess.run(
        [
            "uv", "run", "--no-project", "--python", "3.12",
            "--with", "mlx-vlm>=0.3.11", "--with", "pymupdf",
            "python", str(_RUNNER), str(pdf_path),
        ],
        capture_output=True, text=True, timeout=_VLM_TIMEOUT,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"GLM-OCR backend failed:\n{proc.stderr[-1200:]}")
    if not proc.stdout.strip():
        raise RuntimeError("GLM-OCR backend produced no output")
    return proc.stdout


def marker_convert(pdf_path: Path) -> str:
    """marker via an isolated uv env. Returns raw Markdown."""
    _require_uv()
    with tempfile.TemporaryDirectory() as td:
        proc = subprocess.run(
            [
                "uv", "run", "--no-project",
                "--with", "marker-pdf",
                "marker_single", str(pdf_path),
                "--output_dir", td,
                "--output_format", "markdown",
                "--disable_image_extraction",
            ],
            capture_output=True, text=True, timeout=_VLM_TIMEOUT,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"marker backend failed:\n{proc.stderr[-1200:]}")
        stem = Path(pdf_path).stem
        out = Path(td) / stem / f"{stem}.md"
        if out.exists():
            return out.read_text()
        mds = sorted(Path(td).rglob("*.md"), key=lambda p: -p.stat().st_size)
        if not mds:
            raise RuntimeError("marker backend produced no Markdown output")
        return mds[0].read_text()


def vlm_convert(pdf_path: Path, use_mlx: bool = True) -> str:
    """Dispatch the VLM path: GLM-OCR on Apple Silicon (unless disabled),
    marker otherwise. Returns raw Markdown."""
    if use_mlx and is_apple_silicon():
        return glm_ocr_convert(pdf_path)
    return marker_convert(pdf_path)


def vlm_backend_name(use_mlx: bool = True) -> str:
    return "GLM-OCR (MLX)" if (use_mlx and is_apple_silicon()) else "marker"
