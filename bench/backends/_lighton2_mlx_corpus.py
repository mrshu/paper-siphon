"""LightOnOCR-2-1B corpus runner via the MLX-converted model (bf16, fast path).

Loads the locally-converted MLX model once and OCRs every corpus PDF through
mlx-vlm (~5 s/page vs ~40 s/page for torch-MPS float32). Writes both raw and
cleaned Markdown per paper, matching the bench's other backends.

Usage: python _lighton2_mlx_corpus.py <mlx_model_path> <pdf1> <pdf2> ...
"""

import sys
import tempfile
import time
from pathlib import Path

DPI = 150
CAP = 30
REPO = Path(__file__).resolve().parents[2]
PROMPT = "Convert this document page to clean Markdown. Preserve headings, tables, and math as LaTeX."


def main() -> None:
    mlx_path = sys.argv[1]
    pdfs = [Path(p) for p in sys.argv[2:]]

    import pypdfium2 as pdfium
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
    from mlx_vlm.utils import load_config

    # clean_markdown is pure regex (no docling import) — safe to import here.
    sys.path.insert(0, str(REPO))
    from paper_siphon.cleaning import clean_markdown

    model, processor = load(mlx_path)
    config = load_config(mlx_path)
    print("[lighton2-mlx] model loaded", flush=True)

    for pdf in pdfs:
        paper = pdf.stem
        raw = REPO / "bench" / "outputs" / paper / "lightonocr2.md"
        clean = REPO / "bench" / "outputs" / paper / "lightonocr2.clean.md"
        if clean.exists() and clean.stat().st_size > 0:
            print(f"[lighton2-mlx] {paper}: cached", flush=True)
            continue
        raw.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        doc = pdfium.PdfDocument(str(pdf))
        n = min(len(doc), CAP)
        parts = []
        with tempfile.TemporaryDirectory() as td:
            for i in range(n):
                img = Path(td) / f"p{i + 1:04d}.png"
                doc[i].render(scale=DPI / 72.0).to_pil().save(str(img))
                formatted = apply_chat_template(processor, config, PROMPT, num_images=1)
                r = generate(model, processor, formatted, image=[str(img)],
                             max_tokens=4096, verbose=False)
                text = r if isinstance(r, str) else getattr(r, "text", str(r))
                parts.append(text.strip())
        md = "\n\n".join(parts)
        raw.write_text(md, encoding="utf-8")
        clean.write_text(clean_markdown(md), encoding="utf-8")
        dt = time.time() - t0
        print(f"[lighton2-mlx] {paper}: OK {dt:.0f}s ({dt / max(n,1):.1f}s/pg, "
              f"{n} pages, {len(md)} chars)", flush=True)


if __name__ == "__main__":
    main()
