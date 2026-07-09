#!/bin/bash
# Run nanonets2 and olmocr2 from KNOWN-GOOD pre-converted mlx-community builds
# (self-conversion of the base produced empty output), each with its documented
# prompt (baked into _mlx_corpus.py's PROMPTS). Waits for the dots+paddle runner
# to free the GPU first — running >1 VLM at once thrashes memory (220s/pg vs
# ~30s/pg). Validates page 1 before committing the full corpus.
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
S=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
DP_PID="${1:-74761}"
log(){ echo "[no $(date +%H:%M)] $*"; }

until ! kill -0 "$DP_PID" 2>/dev/null; do sleep 30; done
log "dots+paddle done; GPU free — running nanonets2 + olmocr2"

# backend | community repo (used as the mlx_path arg to _mlx_corpus.py)
MODELS=(
  "nanonets2|mlx-community/Nanonets-OCR2-3B-bf16"
  "olmocr2|mlx-community/olmOCR-2-7B-1025-4bit"
)

for spec in "${MODELS[@]}"; do
  IFS='|' read -r backend repo <<< "$spec"
  n=$(find bench/outputs -name "${backend}.clean.md" -size +0c | wc -l | tr -d ' ')
  if [ "$n" -ge 14 ]; then log "$backend: already $n/14, skip"; continue; fi
  log "$backend: running corpus from $repo"
  uv run --isolated --no-project --python 3.12 \
    --with "mlx-vlm>=0.3.11,<0.7" --with pypdfium2 --with pillow \
    python bench/backends/_mlx_corpus.py "$repo" "$backend" bench/corpus/pdfs/*.pdf \
    > "$S/run_${backend}_community.log" 2>&1
  n=$(find bench/outputs -name "${backend}.clean.md" -size +0c | wc -l | tr -d ' ')
  log "$backend: $n/14 non-empty papers"
done

log "=== NANO-OLM DONE ==="
