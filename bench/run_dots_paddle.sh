#!/bin/bash
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
S=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
log(){ echo "[dp $(date +%H:%M)] $*"; }
for spec in "dots_ocr|$S/dots_ocr-mlx" "paddleocr_vl_mlx|$S/paddleocr_vl_mlx-mlx"; do
  IFS='|' read -r backend mlxdir <<< "$spec"
  log "$backend: running corpus"
  uv run --isolated --no-project --python 3.12 \
    --with "mlx-vlm>=0.3.11,<0.7" --with pypdfium2 --with pillow \
    python bench/backends/_mlx_corpus.py "$mlxdir" "$backend" bench/corpus/pdfs/*.pdf \
    > "$S/run_${backend}_full.log" 2>&1
  n=$(find bench/outputs -name "${backend}.clean.md" -size +0c | wc -l | tr -d ' ')
  log "$backend: $n/14 non-empty"
done
log "=== DOTS+PADDLE DONE ==="
