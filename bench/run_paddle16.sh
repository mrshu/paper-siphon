#!/bin/bash
# Add PaddleOCR-VL-1.6 (the current version; the base repo we ran is marked
# superseded by it). Same 0.9B arch/license, higher OmniDocBench score. Download
# + convert with --trust-remote-code (CPU/network — safe alongside a GPU run),
# then run the corpus AFTER the nano+olm finisher frees the GPU, as backend
# paddleocr_vl_16. The _mlx_corpus.py fixes (idempotent sanitize + greedy) apply
# to any paddleocr_vl* backend.
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
S=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
V=bench/.venvs/glm_ocr_mlx
NANO_OLM_PID="${1:-85107}"
mlxdir="$S/paddleocr_vl_16-mlx"
log(){ echo "[p16 $(date +%H:%M)] $*"; }

# 1) convert (download happens here; independent of the GPU)
if [ ! -f "$mlxdir/config.json" ]; then
  log "converting PaddleOCR-VL-1.6"
  $V/bin/python -m mlx_vlm convert --hf-path PaddlePaddle/PaddleOCR-VL-1.6 \
    --mlx-path "$mlxdir" --dtype bfloat16 --trust-remote-code \
    > "$S/convert_paddleocr_vl_16.log" 2>&1
  if [ ! -f "$mlxdir/config.json" ]; then
    log "CONVERT FAILED — see $S/convert_paddleocr_vl_16.log"; exit 1
  fi
fi
log "1.6 converted; waiting for nano+olm ($NANO_OLM_PID) to free the GPU"

# 2) wait for the nano+olm finisher so we don't thrash the GPU
until ! kill -0 "$NANO_OLM_PID" 2>/dev/null; do sleep 30; done
log "GPU free; running PaddleOCR-VL-1.6 corpus"

uv run --isolated --no-project --python 3.12 \
  --with "mlx-vlm>=0.3.11,<0.7" --with pypdfium2 --with pillow \
  python bench/backends/_mlx_corpus.py "$mlxdir" paddleocr_vl_16 bench/corpus/pdfs/*.pdf \
  > "$S/run_paddleocr_vl_16.log" 2>&1
n=$(find bench/outputs -name "paddleocr_vl_16.clean.md" -size +0c | wc -l | tr -d ' ')
log "paddleocr_vl_16: $n/14 non-empty"
log "=== PADDLE16 DONE ==="
