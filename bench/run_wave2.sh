#!/bin/bash
# Wave 2: remaining candidates, SEQUENTIAL to avoid MPS/GPU thrash.
# - glm_ocr_mlx: smoke first (untested server path), then FULL corpus (key candidate).
# - mineru: smoke, then subset (speed unknown).
# - chandra / paddleocr_vl: SUBSET only — proven CPU-bound (>5-7 min/page on this
#   Mac), so full corpus is impractical; subset gives a quality + speed signal.
set -u
cd /Users/mrshu/work/dev/mrshu/paper-siphon
PY=.venv/bin/python
LOG=/private/tmp/claude-501/-Users-mrshu-work-dev-mrshu-paper-siphon/18aa9848-fe64-45e0-9950-189e2f9e0baa/scratchpad
SUBSET="arxiv_attention arxiv_bert ssl_2020_tigers"   # math+tables, table-heavy, glyph-scramble discriminator

echo "=== wave2 start $(date) ==="

echo "--- glm smoke ---"
$PY bench/run.py smoke --backend glm_ocr_mlx --paper arxiv_attention > $LOG/glm_smoke.log 2>&1
tail -4 $LOG/glm_smoke.log
echo "--- glm full ---"
$PY bench/run.py convert --backend glm_ocr_mlx > $LOG/glm.log 2>&1
echo "glm: $(grep -cE 'OK|ERROR' $LOG/glm.log) papers, $(grep -c ERROR $LOG/glm.log) errors"

echo "--- mineru smoke ---"
$PY bench/run.py smoke --backend mineru --paper arxiv_attention > $LOG/mineru_smoke.log 2>&1
tail -4 $LOG/mineru_smoke.log
echo "--- mineru subset ---"
for p in $SUBSET; do $PY bench/run.py convert --backend mineru --paper $p >> $LOG/mineru.log 2>&1; done
echo "mineru: $(grep -cE 'OK|ERROR' $LOG/mineru.log) papers"

echo "--- chandra subset ---"
for p in $SUBSET; do $PY bench/run.py convert --backend chandra --paper $p >> $LOG/chandra.log 2>&1; done
echo "chandra: $(grep -cE 'OK|ERROR' $LOG/chandra.log) papers"

echo "--- paddleocr_vl subset ---"
for p in $SUBSET; do $PY bench/run.py convert --backend paddleocr_vl --paper $p >> $LOG/paddle.log 2>&1; done
echo "paddle: $(grep -cE 'OK|ERROR' $LOG/paddle.log) papers"

echo "=== wave2 done $(date) ==="
