#!/bin/bash
# Self-healing finisher for the four new MLX backends. Runs AFTER the main
# orchestrator (PID arg) frees the GPU, then for each backend still short of
# 14/14 it ensures an MLX checkpoint exists (converting with --trust-remote-code
# if the orchestrator's flag-less convert failed) and runs the corpus with the
# fixed runner (paddle sanitize patch + greedy decoding). Idempotent: the corpus
# runner caches per-paper, and conversion is skipped when config.json exists.
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
S=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
V=bench/.venvs/glm_ocr_mlx
MAIN_PID="${1:-13040}"
log(){ echo "[finish $(date +%H:%M)] $*"; }

until ! kill -0 "$MAIN_PID" 2>/dev/null; do sleep 30; done
log "main orchestrator done; healing leftovers"

# backend | hf-path | convert-flags
MODELS=(
  "dots_ocr|rednote-hilab/dots.ocr|--dtype bfloat16"
  "paddleocr_vl_mlx|PaddlePaddle/PaddleOCR-VL|--dtype bfloat16"
  "nanonets2|nanonets/Nanonets-OCR2-3B|--dtype bfloat16"
  "olmocr2|allenai/olmOCR-2-7B-1025|-q --q-bits 4"
)

for spec in "${MODELS[@]}"; do
  IFS='|' read -r backend hf flags <<< "$spec"
  n=$(ls bench/outputs/*/${backend}.clean.md 2>/dev/null | wc -l | tr -d ' ')
  if [ "$n" -ge 14 ]; then log "$backend: already $n/14, skip"; continue; fi
  mlxdir="$S/${backend}-mlx"
  if [ ! -f "$mlxdir/config.json" ]; then
    log "$backend: converting with --trust-remote-code ($hf) $flags"
    $V/bin/python -m mlx_vlm convert --hf-path "$hf" --mlx-path "$mlxdir" \
      --trust-remote-code $flags > "$S/convert_${backend}_fix.log" 2>&1
    if [ ! -f "$mlxdir/config.json" ]; then
      log "$backend: CONVERT FAILED — see $S/convert_${backend}_fix.log"; continue
    fi
  fi
  log "$backend: running corpus"
  uv run --isolated --no-project --python 3.12 \
    --with "mlx-vlm>=0.3.11,<0.7" --with pypdfium2 --with pillow \
    python bench/backends/_mlx_corpus.py "$mlxdir" "$backend" bench/corpus/pdfs/*.pdf \
    > "$S/run_${backend}_fix.log" 2>&1
  n=$(ls bench/outputs/*/${backend}.clean.md 2>/dev/null | wc -l | tr -d ' ')
  log "$backend: $n/14 papers done"
done

log "=== FINISH-MLX DONE ==="
for spec in "${MODELS[@]}"; do
  IFS='|' read -r backend hf flags <<< "$spec"
  n=$(ls bench/outputs/*/${backend}.clean.md 2>/dev/null | wc -l | tr -d ' ')
  log "final: $backend $n/14"
done
