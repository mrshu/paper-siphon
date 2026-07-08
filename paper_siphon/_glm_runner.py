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


def main() -> None:
    pdf_path = sys.argv[1]

    import fitz  # PyMuPDF
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
    from mlx_vlm.utils import load_config

    model, processor = load(MODEL)
    config = load_config(MODEL)

    doc = fitz.open(pdf_path)
    zoom = DPI / 72.0
    parts: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        for i in range(doc.page_count):
            img = Path(td) / f"p{i + 1:04d}.png"
            doc.load_page(i).get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(str(img))
            formatted = apply_chat_template(processor, config, PROMPT, num_images=1)
            # Isolate generate()'s own stdout: stdout carries the Markdown result
            # back to the parent, so any stray prints from the library must not
            # leak into it. (verbose=False already suppresses stats; belt-and-braces.)
            with contextlib.redirect_stdout(io.StringIO()):
                result = generate(
                    model, processor, formatted, image=[str(img)],
                    max_tokens=MAX_TOKENS, verbose=False,
                )
            text = result if isinstance(result, str) else getattr(result, "text", str(result))
            parts.append(text.strip())
    doc.close()

    sys.stdout.write("\n\n".join(parts))


if __name__ == "__main__":
    main()
