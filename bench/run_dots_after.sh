#!/bin/bash
# dots.ocr needs --trust-remote-code to convert (custom modeling code), which the
# main orchestrator omitted. Its weights are already cached, so conversion is
# fast. Run its corpus AFTER the main orchestrator (PID passed in) frees the GPU,
# to avoid MPS thrash. The convert step is kicked off separately (CPU-bound) and
# this script just waits for the MLX dir, then runs the corpus.
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
S=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
MAIN_PID="${1:-13040}"
mlxdir="$S/dots_ocr-mlx"
log(){ echo "[dots-after $(date +%H:%M)] $*"; }

# wait for the main orchestrator to finish (frees the GPU)
until ! kill -0 "$MAIN_PID" 2>/dev/null; do sleep 30; done
log "main orchestrator done"

# wait for the (concurrent, CPU-bound) conversion to land the MLX weights
until [ -f "$mlxdir/config.json" ]; do
  if ! pgrep -f "mlx_vlm convert --hf-path rednote-hilab/dots.ocr" >/dev/null; then
    log "convert process gone and no config.json — CONVERT FAILED, see $S/convert_dots_ocr2.log"
    exit 1
  fi
  sleep 20
done
log "dots.ocr MLX weights present; running corpus"

uv run --isolated --no-project --python 3.12 \
  --with "mlx-vlm>=0.3.11,<0.7" --with pypdfium2 --with pillow \
  python bench/backends/_mlx_corpus.py "$mlxdir" dots_ocr bench/corpus/pdfs/*.pdf \
  > "$S/run_dots_ocr.log" 2>&1
n=$(ls bench/outputs/*/dots_ocr.clean.md 2>/dev/null | wc -l | tr -d ' ')
log "dots_ocr: $n/14 papers done"
log "=== DOTS-AFTER DONE ==="
