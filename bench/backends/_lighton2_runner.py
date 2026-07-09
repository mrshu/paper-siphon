"""Standalone LightOnOCR-2-1B runner for the benchmark, executed in an isolated
`uv run --with transformers torch ...` env (native transformers/MPS path — NOT
mlx-vlm, which degenerated on LightOnOCR v1).

Renders each PDF page and OCRs it, printing the concatenated Markdown as UTF-8
to stdout. Imports only transformers/torch/pypdfium2/PIL + stdlib.

Usage: python _lighton2_runner.py <pdf_path>
"""

import sys
import tempfile
from pathlib import Path

MODEL = "lightonai/LightOnOCR-2-1B"
DPI = 150
CAP = 30  # match the GLM runner's page cap for a fair comparison


def main() -> None:
    pdf_path = sys.argv[1]

    import pypdfium2 as pdfium
    import torch
    from transformers import LightOnOcrForConditionalGeneration, LightOnOcrProcessor

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float32 if device == "mps" else torch.bfloat16
    model = LightOnOcrForConditionalGeneration.from_pretrained(
        MODEL, torch_dtype=dtype
    ).to(device)
    processor = LightOnOcrProcessor.from_pretrained(MODEL)

    pdf = pdfium.PdfDocument(pdf_path)
    n = min(len(pdf), CAP)
    parts: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            img_path = Path(td) / f"p{i + 1:04d}.png"
            pdf[i].render(scale=DPI / 72.0).to_pil().save(str(img_path))
            conversation = [
                {"role": "user", "content": [{"type": "image", "url": str(img_path)}]}
            ]
            inputs = processor.apply_chat_template(
                conversation, add_generation_prompt=True, tokenize=True,
                return_dict=True, return_tensors="pt",
            )
            inputs = {
                k: (v.to(device=device, dtype=dtype) if v.is_floating_point() else v.to(device))
                for k, v in inputs.items()
            }
            out = model.generate(**inputs, max_new_tokens=4096)
            gen = out[0, inputs["input_ids"].shape[1]:]
            parts.append(processor.decode(gen, skip_special_tokens=True).strip())

    sys.stdout.buffer.write("\n\n".join(parts).encode("utf-8"))


if __name__ == "__main__":
    main()
