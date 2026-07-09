"""Generic MLX-model corpus runner (backend name parameterized).

Loads the locally-converted MLX model once and OCRs every corpus PDF through
mlx-vlm (~5 s/page vs ~40 s/page for torch-MPS float32). Writes both raw and
cleaned Markdown per paper, matching the bench's other backends.

Usage: python _mlx_corpus.py <mlx_model_path> <backend_name> <pdf1> <pdf2> ...
"""

import sys
import tempfile
import time
from pathlib import Path

DPI = 150
CAP = 30
REPO = Path(__file__).resolve().parents[2]
PROMPT = "Convert this document page to clean Markdown. Preserve headings, tables, and math as LaTeX."

# Some models are finetuned around a specific instruction and emit almost
# nothing (immediate EOS) under a generic prompt. Use each model's documented
# prompt so it produces meaningful output.
NANONETS_PROMPT = (
    "Extract the text from the above document as if you were reading it "
    "naturally. Return the tables in html format. Return the equations in LaTeX "
    "representation. If there is an image in the document and image caption is "
    "not present, add a small description of the image inside the <img></img> "
    "tag; otherwise, add the image caption inside <img></img>. Watermarks should "
    "be wrapped in brackets. Ex: <watermark>OFFICIAL COPY</watermark>. Page "
    "numbers should be wrapped in brackets. Ex: <page_number>14</page_number>. "
    "Prefer using ☐ and ☑ for check boxes."
)
# olmOCR-2 no-anchoring prompt (the model outputs YAML front matter + text).
OLMOCR_PROMPT = (
    "Attached is one page of a document that you must process. Just return the "
    "plain text representation of this document as if you were reading it "
    "naturally.\nConvert equations to LateX and tables to markdown.\nReturn your "
    "output as markdown, with a front matter section on top specifying values "
    "for the primary_language, is_rotation_valid, rotation_correction, is_table, "
    "and is_diagram parameters."
)
PROMPTS = {
    "nanonets2": NANONETS_PROMPT,
    "olmocr2": OLMOCR_PROMPT,
}


def main() -> None:
    mlx_path = sys.argv[1]
    backend = sys.argv[2]
    pdfs = [Path(p) for p in sys.argv[3:]]

    import pypdfium2 as pdfium
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
    from mlx_vlm.utils import load_config

    # PaddleOCR-VL: mlx-vlm 0.6.x's sanitize() is not idempotent — it does a
    # naive key.replace("model", "language_model.model"), so loading an
    # already-converted MLX checkpoint (whose keys are already
    # "language_model.model.*") double-prefixes them to
    # "language_language_model.model.language_model.model.*" and 165 params fail
    # to bind. The saved weights are already in final form, so re-sanitizing
    # should be identity: short-circuit when keys are already prefixed.
    if backend.startswith("paddleocr_vl"):
        from mlx_vlm.models.paddleocr_vl import paddleocr_vl as _pmod

        _orig = _pmod.Model.sanitize

        def _idempotent(self, weights):
            if any(k.startswith("language_model.model") for k in weights):
                drop = ("packing_position_embedding", "vision_model.head")
                return {k: v for k, v in weights.items()
                        if not any(d in k for d in drop)}
            return _orig(self, weights)

        _pmod.Model.sanitize = _idempotent

    # clean_markdown is pure regex (no docling import) — safe to import here.
    sys.path.insert(0, str(REPO))
    from paper_siphon.cleaning import clean_markdown

    # trust_remote_code is required by custom-processor models (e.g. dots.ocr)
    # and harmless for the rest.
    model, processor = load(mlx_path, trust_remote_code=True)
    config = load_config(mlx_path)
    print("[mlx] model loaded", flush=True)

    for pdf in pdfs:
        paper = pdf.stem
        raw = REPO / "bench" / "outputs" / paper / f"{backend}.md"
        clean = REPO / "bench" / "outputs" / paper / f"{backend}.clean.md"
        if clean.exists() and clean.stat().st_size > 0:
            print(f"[mlx] {paper}: cached", flush=True)
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
                prompt = PROMPTS.get(backend, PROMPT)
                formatted = apply_chat_template(processor, config, prompt, num_images=1)
                # Greedy decoding (temperature=0.0): deterministic transcription
                # and, for PaddleOCR-VL, the difference between clean output and
                # a mid-page collapse into one-character-per-line garbage under
                # mlx-vlm's default sampler.
                r = generate(model, processor, formatted, image=[str(img)],
                             max_tokens=4096, verbose=False, temperature=0.0)
                text = r if isinstance(r, str) else getattr(r, "text", str(r))
                parts.append(text.strip())
        md = "\n\n".join(parts)
        raw.write_text(md, encoding="utf-8")
        clean.write_text(clean_markdown(md), encoding="utf-8")
        dt = time.time() - t0
        print(f"[mlx] {paper}: OK {dt:.0f}s ({dt / max(n,1):.1f}s/pg, "
              f"{n} pages, {len(md)} chars)", flush=True)


if __name__ == "__main__":
    main()
