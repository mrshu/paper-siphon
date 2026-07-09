#!/bin/bash
# Convert every MLX-convertible candidate to MLX (bf16, or 4-bit for the 7B) and
# run it over the full 14-paper corpus via the fast MLX path. Sequential to
# avoid GPU thrash. Each step logs and continues on failure (don't give up).
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
S=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
V=bench/.venvs/glm_ocr_mlx
log(){ echo "[mlx-all $(date +%H:%M)] $*"; }

# wait for the LightOnOCR-2 MLX corpus run to free the GPU
until ! pgrep -f "_lighton2_mlx_corpus.py" >/dev/null; do sleep 30; done
log "LightOnOCR-2 done; converting + running the rest"

convert_and_run(){
  hf="$1"; backend="$2"; shift 2; flags="$*"
  mlxdir="$S/${backend}-mlx"
  log "$backend: converting ($hf) $flags"
  if [ ! -f "$mlxdir/config.json" ]; then
    $V/bin/python -m mlx_vlm convert --hf-path "$hf" --mlx-path "$mlxdir" $flags > "$S/convert_${backend}.log" 2>&1
    if [ ! -f "$mlxdir/config.json" ]; then log "$backend: CONVERT FAILED — see $S/convert_${backend}.log"; return; fi
  fi
  log "$backend: running corpus"
  uv run --isolated --no-project --python 3.12 \
    --with "mlx-vlm>=0.3.11,<0.7" --with pypdfium2 --with pillow \
    python bench/backends/_mlx_corpus.py "$mlxdir" "$backend" bench/corpus/pdfs/*.pdf > "$S/run_${backend}.log" 2>&1
  n=$(ls bench/outputs/*/${backend}.clean.md 2>/dev/null | wc -l | tr -d ' ')
  log "$backend: $n/14 papers done"
}

# smallest / most promising first
convert_and_run "rednote-hilab/dots.ocr"      dots_ocr        --dtype bfloat16
convert_and_run "PaddlePaddle/PaddleOCR-VL"   paddleocr_vl_mlx --dtype bfloat16
convert_and_run "nanonets/Nanonets-OCR2-3B"   nanonets2       --dtype bfloat16
convert_and_run "allenai/olmOCR-2-7B-1025"    olmocr2         -q --q-bits 4

log "=== MLX-ALL DONE ==="
