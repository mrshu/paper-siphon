"""Generic transformers VLM → Markdown runner, executed in an isolated
`uv run --with transformers torch ...` env (native transformers/MPS path).

This is the path that worked for LightOnOCR-2 where the mlx-vlm generic server
failed for the Qwen-family models. Parameterized by model id so it can drive
olmOCR-2, Nanonets-OCR2, dots.ocr, etc. via the same AutoModelForImageTextToText
+ apply_chat_template flow.

Usage: python _hf_vlm_runner.py <model_id> <pdf_path>
"""

import sys
import tempfile
from pathlib import Path

DPI = 150
CAP = 30
PROMPT = (
    "Convert this document page image to clean GitHub-flavored Markdown. "
    "Preserve headings, paragraphs, lists, tables (as Markdown or HTML), and "
    "mathematics (as LaTeX). Output ONLY the Markdown for the page content."
)


def main() -> None:
    model_id = sys.argv[1]
    pdf_path = sys.argv[2]

    import pypdfium2 as pdfium
    import torch
    from transformers import AutoModelForImageTextToText, AutoProcessor

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    dtype = torch.float32 if device == "mps" else torch.bfloat16
    model = AutoModelForImageTextToText.from_pretrained(
        model_id, torch_dtype=dtype, trust_remote_code=True
    ).to(device)
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    pdf = pdfium.PdfDocument(pdf_path)
    n = min(len(pdf), CAP)
    parts: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            img = Path(td) / f"p{i + 1:04d}.png"
            pdf[i].render(scale=DPI / 72.0).to_pil().save(str(img))
            conversation = [{
                "role": "user",
                "content": [
                    {"type": "image", "url": str(img)},
                    {"type": "text", "text": PROMPT},
                ],
            }]
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
