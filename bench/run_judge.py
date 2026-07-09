"""Build blinded packets across the working backends and run the codex judge.

The Claude judge is run separately by the main agent (subagents read packet.json
and write verdict.claude.json). This script:
  1. build_packet() for every paper across BACKENDS (writes packet.json+keymap.json)
  2. codex_judge() for every paper (writes verdict.codex.json)

Usage: python run_judge.py [--packets-only]
"""

from __future__ import annotations

import sys

from judge import build_packet, codex_judge
from lib import OUTPUTS, load_manifest, log

# Final working set (Qwen2.5-VL OCR finetunes nanonets2/olmocr2 excluded — they
# don't produce valid output via mlx-vlm on Apple Silicon).
BACKENDS = [
    "docling_standard",
    "granite_docling_mlx",
    "marker",
    "glm_ocr_mlx",
    "lightonocr2",
    "dots_ocr",
    "paddleocr_vl_mlx",
    "paddleocr_vl_16",
]


def main() -> None:
    packets_only = "--packets-only" in sys.argv
    papers = load_manifest()
    for p in papers:
        avail = [b for b in BACKENDS if (OUTPUTS / p.id / f"{b}.clean.md").exists()]
        packet = build_packet(p, BACKENDS)
        if packet is None:
            log(f"{p.id}: <2 outputs, skipped")
            continue
        log(f"{p.id}: packet built ({len(avail)} backends: {','.join(avail)})")
        if packets_only:
            continue
        v = codex_judge(p)
        if v and v.get("scores"):
            log(f"{p.id}: codex verdict ok ({len(v['scores'])} scored)")
        else:
            log(f"{p.id}: codex verdict FAILED/empty")


if __name__ == "__main__":
    main()
