"""LightOnOCR-2-1B corpus runner: load the model ONCE (fp16 on MPS) and OCR
every corpus PDF, writing bench/outputs/<paper>/lightonocr2.md per paper.

Speed levers vs the per-paper runner: (1) fp16 on MPS (~2x faster, half memory;
MPS supports fp16, just not bf16), (2) one model load for the whole corpus
instead of 14. Resumable: skips papers whose output already exists.

Usage: python _lighton2_corpus.py <pdf1> <pdf2> ...
"""

import sys
import tempfile
import time
from pathlib import Path

MODEL = "lightonai/LightOnOCR-2-1B"
DPI = 150
CAP = 30
REPO = Path(__file__).resolve().parents[2]


def main() -> None:
    pdfs = [Path(p) for p in sys.argv[1:]]

    import pypdfium2 as pdfium
    import torch
    from transformers import LightOnOcrForConditionalGeneration, LightOnOcrProcessor

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    # MPS needs float32: bf16 is unsupported and fp16 overflows to NaN during
    # generation for this model. float32 is the practical floor here.
    dtype = torch.float32 if device == "mps" else torch.bfloat16
    print(f"[lighton2] device={device} dtype={dtype}", flush=True)
    model = LightOnOcrForConditionalGeneration.from_pretrained(
        MODEL, torch_dtype=dtype
    ).to(device)
    processor = LightOnOcrProcessor.from_pretrained(MODEL)

    for pdf in pdfs:
        paper = pdf.stem
        out = REPO / "bench" / "outputs" / paper / "lightonocr2.md"
        if out.exists() and out.stat().st_size > 0:
            print(f"[lighton2] {paper}: cached", flush=True)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        doc = pdfium.PdfDocument(str(pdf))
        n = min(len(doc), CAP)
        parts = []
        with tempfile.TemporaryDirectory() as td:
            for i in range(n):
                img = Path(td) / f"p{i + 1:04d}.png"
                doc[i].render(scale=DPI / 72.0).to_pil().save(str(img))
                conversation = [
                    {"role": "user", "content": [{"type": "image", "url": str(img)}]}
                ]
                inputs = processor.apply_chat_template(
                    conversation, add_generation_prompt=True, tokenize=True,
                    return_dict=True, return_tensors="pt",
                )
                inputs = {
                    k: (v.to(device=device, dtype=dtype) if v.is_floating_point() else v.to(device))
                    for k, v in inputs.items()
                }
                gen_out = model.generate(**inputs, max_new_tokens=4096)
                gen = gen_out[0, inputs["input_ids"].shape[1]:]
                parts.append(processor.decode(gen, skip_special_tokens=True).strip())
        out.write_bytes("\n\n".join(parts).encode("utf-8"))
        dt = time.time() - t0
        print(f"[lighton2] {paper}: OK {dt:.0f}s ({dt / max(n,1):.1f}s/pg, {n} pages, "
              f"{out.stat().st_size} chars)", flush=True)


if __name__ == "__main__":
    main()
