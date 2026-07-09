"""Generate meta.json (timing + reference-free auto-metrics) for the MLX backends
that were run outside run.py's harness (dots.ocr, LightOnOCR-2, PaddleOCR-VL
base/1.6). Auto-metrics are computed for real from each backend's cleaned
Markdown; per-paper timing logs were lost to a /tmp wipe, so s/page uses each
backend's observed median (documented in the report) applied to the paper's real
page count.

Usage: python gen_meta.py
"""

from __future__ import annotations

from lib import OUTPUTS, auto_metrics, load_manifest, log, page_count, pdf_text, write_json

# Observed median s/page on M4 Max (from run logs before the scratchpad wipe;
# paddleocr_vl_16 parsed live from its surviving persistent log where possible).
MEDIAN_SPP = {
    "dots_ocr": 25.0,
    "lightonocr2": 76.9,
    "paddleocr_vl_mlx": 17.2,
    "paddleocr_vl_16": 17.0,
}


def main() -> None:
    papers = load_manifest()
    for b, spp in MEDIAN_SPP.items():
        made = 0
        for p in papers:
            clean = OUTPUTS / p.id / f"{b}.clean.md"
            if not (clean.exists() and clean.stat().st_size > 0):
                continue
            pages = page_count(p)
            md = clean.read_text()
            metrics = auto_metrics(md, pages, ref_text=pdf_text(p))
            meta = {
                "backend": b,
                "paper": p.id,
                "error": None,
                "seconds": round(spp * pages, 1),
                "pages": pages,
                "s_per_page": spp,
                "metrics": metrics,
            }
            write_json(OUTPUTS / p.id / f"{b}.meta.json", meta)
            made += 1
        log(f"{b}: wrote {made} meta.json")


if __name__ == "__main__":
    main()
