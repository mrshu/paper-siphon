#!/bin/bash
# Fix-up runner: get every previously-failed model to produce meaningful output,
# each via a CORRECTED integration path, on a 4-page representative sample
# (attention: math+tables+multicol). Runs after LightOnOCR-2 frees the GPU.
# Sequential to avoid MPS thrash. Each result cached under bench/outputs/_fixup/.
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
S=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
SAMPLE=bench/outputs/_fixup/arxiv_attention_4pg.pdf
HF=bench/backends/_hf_vlm_runner.py
OUT=bench/outputs/_fixup
log(){ echo "[fixup $(date +%H:%M)] $*"; }

# wait for the LightOnOCR-2 corpus run to finish (avoid GPU contention)
until ! pgrep -f "_lighton2_corpus.py" >/dev/null; do sleep 60; done
log "LightOnOCR-2 done; starting fix-up attempts"

# 1) olmOCR-2 (Qwen2.5-VL) via NATIVE transformers (the mlx-vlm path crashed).
log "olmOCR-2 via native transformers..."
uv run --isolated --no-project --python 3.12 \
  --with "transformers==5.0.0" --with torch --with torchvision --with pillow --with pypdfium2 --with accelerate \
  python "$HF" "allenai/olmOCR-2-7B-1025" "$SAMPLE" > "$OUT/olmocr2_native.md" 2> "$S/fixup_olmocr2.err"
log "olmOCR-2: rc=$? chars=$(wc -c < "$OUT/olmocr2_native.md" 2>/dev/null)"

# 2) Nanonets-OCR2-3B via native transformers (a fresh candidate on the same path).
log "Nanonets-OCR2-3B via native transformers..."
uv run --isolated --no-project --python 3.12 \
  --with "transformers==5.0.0" --with torch --with torchvision --with pillow --with pypdfium2 --with accelerate \
  python "$HF" "nanonets/Nanonets-OCR2-3B" "$SAMPLE" > "$OUT/nanonets2_native.md" 2> "$S/fixup_nanonets.err"
log "Nanonets-OCR2: rc=$? chars=$(wc -c < "$OUT/nanonets2_native.md" 2>/dev/null)"

# 3) chandra via hf (works but slow) — patient, on the small sample.
log "chandra via hf..."
uv run --isolated --no-project --python 3.12 --with "chandra-ocr[hf]" \
  bash -c "PYTORCH_ENABLE_MPS_FALLBACK=1 chandra '$SAMPLE' '$OUT/chandra_out' --method hf" > "$S/fixup_chandra.log" 2> "$S/fixup_chandra.err"
log "chandra: rc=$? md=$(ls $OUT/chandra_out/*.md 2>/dev/null | head -1)"

# 4) mineru via the pipeline backend (CPU OCR — lighter than the vlm backend that timed out).
log "mineru via pipeline backend..."
uv run --isolated --no-project --python 3.12 --with "mineru[core]" \
  mineru -p "$SAMPLE" -o "$OUT/mineru_out" -b pipeline > "$S/fixup_mineru.log" 2> "$S/fixup_mineru.err"
log "mineru: rc=$? md=$(find $OUT/mineru_out -name '*.md' 2>/dev/null | head -1)"

# 5) paddleocr-vl via doc_parser (CPU) — patient, on the small sample.
log "paddleocr-vl via doc_parser..."
uv run --isolated --no-project --python 3.12 \
  --with "paddlepaddle==3.2.1" --with "paddleocr[doc-parser]" \
  paddleocr doc_parser --input "$SAMPLE" --save_path "$OUT/paddle_out" > "$S/fixup_paddle.log" 2> "$S/fixup_paddle.err"
log "paddle: rc=$? md=$(find $OUT/paddle_out -name '*.md' 2>/dev/null | head -1)"

log "=== FIXUP RUN DONE ==="
