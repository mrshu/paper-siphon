# paper-siphon backend benchmark — design

**Date:** 2026-07-08
**Goal:** Decide which new PDF→Markdown backend(s) to add to paper-siphon by
empirically comparing candidate backends on a reproducible corpus of academic
PDFs, using a semi-automatic dual-LLM-judge evaluation.

## Motivation

paper-siphon currently uses Docling: a standard pipeline (default) and a
GraniteDocling-258M MLX VLM pipeline (`--vlm`). Deep research (2026-07-08)
showed small specialist document VLMs (GLM-OCR, MinerU 2.5, PaddleOCR-VL,
Chandra 2) now lead document-parsing benchmarks by a wide margin, but
GraniteDocling itself has never been scored on those leaderboards, so the real
gap for *our* use case (academic PDFs, Apple Silicon) is unmeasured. This
benchmark measures it directly.

## Corpus (all public URLs, reproducible)

14 papers, `bench/corpus/manifest.yaml`. Core = the 6 public PDFs actually run
through paper-siphon (from shell history); expansion = 8 public arXiv papers
chosen for axis coverage.

| id | source | tags |
|----|--------|------|
| ssl_2025_first_order | https://ssl.robocup.org/wp-content/uploads/2025/04/2025_TDP_First-Order.pdf | real-run, multi-column, tables |
| ssl_2025_the_bots | https://ssl.robocup.org/wp-content/uploads/2025/04/2025_TDP_The-Bots.pdf | real-run, multi-column |
| ssl_2020_zjunlict | https://ssl.robocup.org/wp-content/uploads/2020/03/2020_ETDP_ZJUNlict.pdf | real-run, tables |
| ssl_2020_tigers | https://ssl.robocup.org/wp-content/uploads/2020/03/2020_ETDP_TIGERS.pdf | real-run, tables |
| ssl_2025_delft | https://ssl.robocup.org/wp-content/uploads/2025/04/2025_TDP_Delft-Mercurians.pdf | real-run, multi-column |
| arxiv_attention | https://arxiv.org/pdf/1706.03762 | real-run, math, tables, multi-column |
| arxiv_ddpm | https://arxiv.org/pdf/2006.11239 | math-heavy |
| arxiv_bert | https://arxiv.org/pdf/1810.04805 | table-heavy, multi-column |
| arxiv_resnet | https://arxiv.org/pdf/1512.03385 | figures, tables, math |
| arxiv_adam | https://arxiv.org/pdf/1412.6980 | algorithm-blocks, math |
| arxiv_vit | https://arxiv.org/pdf/2010.11929 | math, tables |
| arxiv_batchnorm | https://arxiv.org/pdf/1502.03167 | dense-math |
| arxiv_instructgpt | https://arxiv.org/pdf/2203.02155 | tables, multi-column |
| arxiv_bahdanau | https://arxiv.org/pdf/1409.0473 | older-typesetting, math |

## Architecture

`bench/` is self-contained and **content-addressed / resumable**: any backend
output or judge verdict already cached on disk is skipped, so partial runs
continue cheaply.

```
bench/
  corpus/manifest.yaml        # 14 entries; PDFs downloaded to corpus/pdfs/ (gitignored)
  backends/                   # one adapter module per backend
  outputs/<paper>/<backend>.md    # raw conversion, then uniformly cleaned
  judge/<paper>/pages/*.png   # rendered page images (cached, gitignored)
  judge/<paper>/<backend>.<judge>.json   # per-judge verdicts
  report/README.md            # final ranked tables + recommendation
  run.py                      # orchestrator (download, convert, render, judge, aggregate)
```

### Backends (pluggable adapters)

Each adapter: `name`, `is_available() -> (bool, reason)`, `convert(pdf, out) ->
markdown`. Adapters shell out to **isolated environments** (uv/uvx or dedicated
venvs) to avoid dependency conflicts (docling vs marker vs mineru vs mlx-vlm's
`transformers>=5.0`). A backend that fails `is_available()` is recorded as
**unavailable with reason** and skipped loudly — never silently dropped.

**Fairness:** every backend produces *raw* markdown, then the harness applies
paper-siphon's own `paper_siphon.cleaning.clean_markdown()` uniformly to all
outputs. This isolates backend quality and reflects what shipping the backend
would actually look like.

| adapter | invocation | risk |
|---------|-----------|------|
| docling_standard | docling standard pipeline (repo venv) | baseline |
| granite_docling_mlx | docling VlmPipeline GRANITEDOCLING_MLX (repo venv) | baseline |
| marker | marker-pdf `marker_single`, MPS (uvx/venv) | low |
| chandra | chandra-ocr CLI, HF/MPS (venv) | low |
| mineru | mineru CLI, Apple Silicon backend (venv) | medium |
| glm_ocr_mlx | mlx-vlm OpenAI-compatible server + client (venv) | high |
| paddleocr_vl | PaddleOCR-VL pipeline (venv) | high (Paddle MPS weak) |

High-risk adapters (glm_ocr_mlx, paddleocr_vl) are **prototyped before full
integration**; if they can't run cleanly on the M4 Max in reasonable time they
are recorded unavailable and the benchmark proceeds.

### Evaluation — dual LLM-judge + auto-metrics

1. **Render** each PDF to page PNGs once (PyMuPDF), cached. Judge on a capped
   sample of pages (first N plus any pages detected to contain tables/formulas);
   the cap is recorded in the report (no silent truncation).
2. **Auto-metrics** (reference-free, cheap): output/page length ratio, heading
   count, table count, `$…$`/equation count, and leaked-line-number fraction
   (a known paper-siphon artifact). Catches gross failures automatically.
3. **Judge A — Claude**: one subagent per paper reads that paper's page images
   once, then scores every backend's cleaned markdown on four axes (text
   fidelity, tables, math/formulas, structure/reading-order), 0–10 each with a
   one-line justification. JSON out.
4. **Judge B — codex/GPT** via `codex exec -i <page images>`: same rubric, same
   inputs, independent. (Image support confirmed in codex-cli 0.142.5.)
5. **Aggregate**: per-backend mean per axis, overall, win-rate; flag any
   (paper×backend) where the two judges differ by >2 on any axis for human
   spot-check. This is the semi-automatic step — human reviews only flagged
   disputes.

### Deliverable

`bench/report/README.md`: ranked backend×axis table, per-tag breakdown (does a
leader's edge concentrate in math/tables?), speed (s/page), judge-disagreement
list, and a bottom-line recommendation on which backend(s) to add to
paper-siphon.

## Execution order (guarantees an early complete result)

1. Harness + corpus download + render + auto-metrics + **both baselines** +
   uniform clean + Claude judge + aggregator + report → a complete result with
   baselines only.
2. Add low-risk candidates (marker, chandra), then mineru, then high-risk
   (glm_ocr_mlx, paddleocr_vl). Each backend extends the existing results.
3. Add codex judge as the second judge.

## Non-goals

- Not reproducing OmniDocBench/olmOCR-Bench scoring (no shared ground truth).
- Not shipping any backend in this task — only producing the recommendation.
- Not benchmarking paid APIs (Mistral OCR 4) — local + free only per decision.

## Revisions after codex-exec review (2026-07-08)

Folded in from an independent GPT-5.5 review of this spec:

- **Blind judging.** Judges never see backend names. Per paper, outputs are
  relabeled to random letters in randomized order; the mapping is stored
  separately and only re-joined at aggregation. Removes Claude-judges-Claude and
  order bias.
- **Anti-saturation scoring.** Keep 0–10 per axis as *anchored diagnostics*
  (rubric names concrete error types: missing paragraphs, duplicated headers,
  column-order inversion, malformed tables, math-token loss, hallucinated
  captions; judges must cite page evidence), AND add a **pairwise best→worst
  ranking per paper** → Borda/win-rate that is robust to score saturation.
- **Corrected adapter invocations.** marker: `TORCH_DEVICE=mps marker_single
  … --output_format markdown --disable_image_extraction` (no `--use_llm`).
  chandra: `chandra-ocr[hf]`, `PYTORCH_ENABLE_MPS_FALLBACK=1 chandra <pdf> <out>
  --method hf` (reclassified medium risk). mineru: `mineru -p <pdf> -o <out>`
  with `-b pipeline` fallback. **paddleocr_vl reclassified medium** — docs verify
  Apple M4; `paddleocr[doc-parser]` + CPU paddlepaddle, `paddleocr doc_parser`.
  glm_ocr_mlx stays high-risk and is reported honestly if the generic mlx-vlm
  server can't reproduce GLM-OCR's two-stage pipeline.
- **Smoke test first.** Every backend is smoke-tested on 2 pages with a hard
  timeout, recording s/page + peak RSS, before running the full corpus.
- **Stronger auto-metrics.** Added: char-containment overlap vs PyMuPDF text
  (born-digital), duplicate-line rate, and page-coverage — beyond raw counts.
- **Operational-fit table** in the report: license, package/model size, Apple
  Silicon path, offline cacheability, output shape.
- **Deferred (documented as limitations):** full per-page-sharded judge
  alignment (mitigated: judges are told they see a page *sample* and must judge
  only shown regions); large adversarial corpus (one scanned PDF added; the
  14–15 set is labeled a *selection*, not a representative benchmark).

## Risks

- Local model downloads are several GB each (time, not blockers on 128 GB M4 Max).
- GLM-OCR MLX needs a server + has a `transformers` version conflict (two envs).
- PaddleOCR-VL's Apple-Silicon (MPS) support is weak; may be CPU-slow → may be
  recorded unavailable.
- First full run is ~1–2 h of local compute; mitigated by resumability.
