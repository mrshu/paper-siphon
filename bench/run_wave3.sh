#!/bin/bash
# Wave 3: two additional small local MLX backends (olmOCR-2 4-bit, LightOnOCR-1B
# 4-bit), served via the same mlx-vlm OpenAI-compatible server path as GLM-OCR.
# Sequential to avoid GPU thrash. Smoke first, then full corpus.
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
PY=.venv/bin/python
LOG=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad

echo "=== wave3 start $(date) ==="
for b in olmocr2_mlx lightonocr_mlx; do
  echo "--- $b smoke ---"
  $PY bench/run.py smoke --backend $b --paper arxiv_attention > $LOG/${b}_smoke.log 2>&1
  tail -3 $LOG/${b}_smoke.log
  if grep -q "OK" $LOG/${b}_smoke.log; then
    echo "--- $b full ---"
    $PY bench/run.py convert --backend $b > $LOG/${b}.log 2>&1
    echo "$b: $(grep -cE 'OK|ERROR' $LOG/${b}.log) papers, $(grep -c ERROR $LOG/${b}.log) errors"
  else
    echo "$b smoke failed; skipping full run"
  fi
done
echo "=== wave3 done $(date) ==="
