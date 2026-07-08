"""Standalone GLM-OCR runner, executed in an isolated ``uv run --with`` env.

Renders each PDF page and OCRs it with GLM-OCR via mlx-vlm, printing the
concatenated Markdown to stdout. Imports ONLY mlx_vlm, fitz (PyMuPDF), and the
stdlib — never ``paper_siphon`` — so it runs in an ephemeral environment that
has mlx-vlm + pymupdf but not paper-siphon (and, crucially, not the docling
transformers pin it would conflict with).

Usage: python _glm_runner.py <pdf_path>
"""

import contextlib
import io
import sys
import tempfile
from pathlib import Path

MODEL = "mlx-community/GLM-OCR-bf16"
DPI = 150
# Per-page generation cap. Dense two-column pages with tables + LaTeX can exceed
# a few thousand tokens; keep this generous so a page is not silently truncated.
MAX_TOKENS = 8192
PROMPT = (
    "Convert this document page image to clean GitHub-flavored Markdown. "
    "Preserve headings, paragraphs, lists, tables (as Markdown or HTML), and "
    "mathematics (as LaTeX, inline $..$ or display $$..$$). Output ONLY the "
    "Markdown for the page content; no commentary, no code fences around the whole page."
)


def _extract_text(result) -> str:
    """Normalize mlx_vlm.generate's return across the supported version range.

    Accept a plain string or an object with a str ``.text``; anything else is an
    unexpected contract change and must fail loudly rather than be written to
    the output as a Python repr. Kept import-free so it is unit-testable without
    mlx-vlm installed.
    """
    if isinstance(result, str):
        return result
    if isinstance(getattr(result, "text", None), str):
        return result.text
    raise RuntimeError(
        f"unexpected mlx_vlm.generate result type: {type(result).__name__}"
    )


def main() -> None:
    pdf_path = sys.argv[1]
    real_stdout = sys.stdout

    # Everything the VLM stack does (model load, config, generation) runs with
    # stdout redirected to a sink, so no library banner or stray print can
    # contaminate the Markdown — which we emit to the *saved* real stdout at the
    # end as UTF-8 bytes (round-trips regardless of the child's locale encoding).
    parts: list[str] = []
    with contextlib.redirect_stdout(io.StringIO()):
        import fitz  # PyMuPDF
        from mlx_vlm import generate, load
        from mlx_vlm.prompt_utils import apply_chat_template
        from mlx_vlm.utils import load_config

        model, processor = load(MODEL)
        config = load_config(MODEL)

        doc = fitz.open(pdf_path)
        zoom = DPI / 72.0
        with tempfile.TemporaryDirectory() as td:
            for i in range(doc.page_count):
                img = Path(td) / f"p{i + 1:04d}.png"
                doc.load_page(i).get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(str(img))
                formatted = apply_chat_template(processor, config, PROMPT, num_images=1)
                result = generate(
                    model, processor, formatted, image=[str(img)],
                    max_tokens=MAX_TOKENS, verbose=False,
                )
                # Fail loudly if a page was truncated at the token cap rather
                # than saving a silently-incomplete page as if it were whole;
                # the parent turns the nonzero exit into a VlmBackendError so
                # auto-escalation keeps the standard output.
                if getattr(result, "finish_reason", None) == "length":
                    raise RuntimeError(
                        f"page {i + 1} hit the {MAX_TOKENS}-token cap (truncated)"
                    )
                parts.append(_extract_text(result).strip())
        doc.close()

    real_stdout.buffer.write("\n\n".join(parts).encode("utf-8"))


if __name__ == "__main__":
    main()
