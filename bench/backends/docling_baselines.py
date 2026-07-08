"""The two current paper-siphon backends — the baseline to beat.

Run via `uvx paper-siphon` so they use paper-siphon's OWN resolved dependency
set in isolation (exactly what a user gets), rather than the benchmark's venv
whose deps are perturbed by other backends. Output is already cleaned by
paper-siphon; the harness re-applies clean_markdown() uniformly (idempotent).
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

TIMEOUT = 1800


def _run_siphon(extra_with: list[str], flags: list[str], pdf_path: Path) -> str:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out.md"
        cmd = ["uvx"]
        for w in extra_with:
            cmd += ["--with", w]
        cmd += ["paper-siphon", *flags, str(pdf_path), "-o", str(out)]
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=TIMEOUT)
        return out.read_text()


class DoclingStandard:
    name = "docling_standard"

    def is_available(self) -> tuple[bool, str]:
        if shutil.which("uvx") is None:
            return False, "uvx not on PATH"
        return True, ""

    def convert(self, pdf_path: Path) -> str:
        return _run_siphon([], [], pdf_path)


class GraniteDoclingMLX:
    name = "granite_docling_mlx"

    def is_available(self) -> tuple[bool, str]:
        if shutil.which("uvx") is None:
            return False, "uvx not on PATH"
        if not (platform.system() == "Darwin" and platform.machine() == "arm64"):
            return False, "requires Apple Silicon (arm64 macOS)"
        return True, ""

    def convert(self, pdf_path: Path) -> str:
        return _run_siphon(["paper-siphon[mlx]"], ["--vlm"], pdf_path)
