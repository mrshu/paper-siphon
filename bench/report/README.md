# paper-siphon backend benchmark — results

Corpus: **14 public PDFs** (a *selection*, not a representative benchmark). Judged papers: **14**. Two blinded LLM judges (Claude + codex/GPT) scored anonymized, order-randomized outputs on four anchored axes (0–10) and ranked them best→worst. Every backend's raw Markdown was uniformly cleaned with paper-siphon's `clean_markdown` before judging.

Judge page sample: first 6 pages + up to 10 total incl. table/math pages, rendered at 150 dpi. Judges score only shown pages.

## Bottom line

**`glm_ocr_mlx` wins.** Overall 7.62/10 (mean of both blinded judges), winning **83%** of head-to-head comparisons across 14 papers. That is **+1.69** over the current `--vlm` (`granite_docling_mlx`, 5.93) and **+3.04** over the current default (`docling_standard`, 4.58) — while being **faster** than the current VLM (7.0 vs 16.8 s/page median).

The gap is largest on **math** (the current default drops display equations as `formula-not-decoded`) and on pathological font-encoding (the `ssl_2020_tigers` PDF, where the default emits scrambled glyphs — text recall 0.03 — while the VLM backends read it visually). `docling_standard` remains far the fastest (~0.6 s/page) and is the right default when speed dominates and papers are simple.

**Recommendation:** add `glm_ocr_mlx` as a high-quality Apple-Silicon backend (near-SOTA quality at ~7 s/page, MIT weights, fits in 8 GB). `marker` is a viable cross-platform alternative but GPL and slower cold-start. `mineru`/`chandra`/`paddleocr_vl` — despite topping GPU leaderboards — are **impractically slow on Apple Silicon** (CPU fallback, >5 min/page). `olmocr2_mlx` and `lightonocr_mlx` were also attempted but are NOT viable via mlx-vlm 0.6.4: olmOCR-2 (Qwen2.5-VL-7B) crashes the mlx-vlm server (Stream(gpu) threading bug) and yields empty output via direct generate; LightOnOCR-1B's 4-bit MLX quant emits degenerate output. Both would need their official inference toolchains (olmOCR targets vLLM/CUDA). GLM-OCR is the one strong specialist VLM that runs cleanly on Apple Silicon via mlx-vlm out of the box.

## Ranked results (mean of both judges)

| rank | backend | overall | text | tables | math | structure | win-rate | Borda | s/page |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `glm_ocr_mlx` | **7.62** | 9 | 4.89 | 8.5 | 8.07 | 0.833 | 0.833 | 7.5 |
| 2 | `marker` | **7.32** | 8.25 | 4.82 | 8.18 | 8.04 | 0.762 | 0.762 | 20.4 |
| 3 | `granite_docling_mlx` | **5.93** | 6.79 | 4.21 | 5.89 | 6.82 | 0.25 | 0.25 | 16.8 |
| 4 | `docling_standard` | **4.58** | 6.04 | 4.54 | 2.39 | 5.36 | 0.155 | 0.155 | 0.6 |
| 5 | `chandra` | **—** | — | — | — | — | — | — | — |
| 6 | `lightonocr_mlx` | **—** | — | — | — | — | — | — | — |
| 7 | `mineru` | **—** | — | — | — | — | — | — | — |
| 8 | `olmocr2_mlx` | **—** | — | — | — | — | — | — | — |
| 9 | `paddleocr_vl` | **—** | — | — | — | — | — | — | — |

*Caveat on the **tables** axis: it reads low for every backend because many judged page-samples (first ~6-10 pages) contain no table, and the two judges handled 'no table visible' differently — codex scored 0, Claude scored a neutral ~5 (see the disagreements list). Treat absolute table scores with caution; the relative ordering still holds.*


## Per-judge overall (bias check)

| backend | Claude | codex |
|---|---|---|
| `glm_ocr_mlx` | 7.8 | 7.43 |
| `marker` | 7.66 | 6.98 |
| `granite_docling_mlx` | 6.16 | 5.7 |
| `docling_standard` | 4.62 | 4.54 |
| `chandra` | — | — |
| `lightonocr_mlx` | — | — |
| `mineru` | — | — |
| `olmocr2_mlx` | — | — |
| `paddleocr_vl` | — | — |

## Speed (Apple Silicon M4 Max — a primary deciding factor)

| backend | s/page (median) | s/page (mean) | s/doc (mean) | total (s) | docs |
|---|---|---|---|---|---|
| `docling_standard` | **0.6** | 0.6 | 11.0 | 154.1 | 14 |
| `glm_ocr_mlx` | **7.0** | 7.5 | 137.2 | 1509.0 | 11 |
| `marker` | **12.9** | 20.4 | 344.4 | 4822.1 | 14 |
| `granite_docling_mlx` | **16.8** | 16.8 | 304.4 | 4261.0 | 14 |

*Median s/page is the fairer per-page figure; the mean is inflated for backends that reload models per document (e.g. marker cold-starts). Per-page times >60 s were excluded as wall-clock artifacts of the host sleeping during the unattended run (compute pauses, `time.time()` does not) — this is why some backends show fewer than 14 timed docs.*


## Auto-metrics (reference-free)

| backend | ref-word-recall | leaked-linenum-frac | dup-line-frac | chars/page |
|---|---|---|---|---|
| `glm_ocr_mlx` | 0.868 | 0.0 | 0.006 | 2699.329 |
| `marker` | 0.914 | 0.0 | 0.004 | 3277.071 |
| `granite_docling_mlx` | 0.88 | 0.0 | 0.005 | 3135.543 |
| `docling_standard` | 0.843 | 0.0 | 0.047 | 3173.436 |
| `chandra` | — | — | — | — |
| `lightonocr_mlx` | — | — | — | — |
| `mineru` | — | — | — | — |
| `olmocr2_mlx` | — | — | — | — |
| `paddleocr_vl` | — | — | — | — |

## Per-tag overall (where does an edge concentrate?)

| backend | algorithm-blocks | dense-math | engineering | figures | math | math-heavy | multi-column | older-typesetting | real-run | table-heavy | tables |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `glm_ocr_mlx` | 8.25 | 8.38 | 8.05 | 6.88 | 7.58 | 6.88 | 7.75 | 6.88 | 8.21 | 7.12 | 7.48 |
| `marker` | 8.62 | 6.75 | 7.62 | 7.25 | 7.95 | 6.62 | 7.08 | 6.5 | 7.75 | 5.12 | 7.62 |
| `granite_docling_mlx` | 4.88 | 5.12 | 6.22 | 5.88 | 5.9 | 6.38 | 6.35 | 5.38 | 6.31 | 4.88 | 6.02 |
| `docling_standard` | 5.5 | 2.62 | 4.17 | 3.75 | 5.1 | 4.12 | 5.73 | 2.75 | 4.56 | 5.25 | 4.68 |
| `chandra` | — | — | — | — | — | — | — | — | — | — | — |
| `lightonocr_mlx` | — | — | — | — | — | — | — | — | — | — | — |
| `mineru` | — | — | — | — | — | — | — | — | — | — | — |
| `olmocr2_mlx` | — | — | — | — | — | — | — | — | — | — | — |
| `paddleocr_vl` | — | — | — | — | — | — | — | — | — | — | — |

## Availability & errors

- `lightonocr_mlx`: 14 failures — e.g. ssl_2025_first_order: not viable via mlx-vlm 0.6.4: 4-bit MLX quant emits degenerate repeated-newline 
- `olmocr2_mlx`: 14 failures — e.g. ssl_2025_first_order: not viable via mlx-vlm 0.6.4 on Apple Silicon: server crashes (Stream(gpu) threa
- `mineru`: 3 failures — e.g. ssl_2020_tigers: excluded: TimeoutExpired >1800s on 2 pages (model download + CPU inference)
- `paddleocr_vl`: 3 failures — e.g. ssl_2020_tigers: excluded: >5 min/page (CPU-only wheel on Mac), smoke unfinished after 10 min
- `chandra`: 3 failures — e.g. ssl_2020_tigers: excluded: >7 min/page, 2-page smoke unfinished after 15 min (9.9GB model, CPU fa

## Operational fit

| backend | license | model size | Apple Silicon | note |
|---|---|---|---|---|
| `glm_ocr_mlx` | MIT weights / Apache code | 0.9B | native MLX (direct-server path) | best-Mac candidate |
| `marker` | GPL-3.0 code / model license | ~few 100 MB | MPS | table/math LLM opt-in |
| `granite_docling_mlx` | Apache-2.0 | 258M | native MLX | current --vlm |
| `docling_standard` | MIT | small (docling models) | native | current default |
| `chandra` | modified OpenRAIL-M (research/personal/<$2M) | 9.9 GB (hf) | MPS w/ heavy CPU fallback — SLOW | opt-in; subset only |
| `lightonocr_mlx` | Apache-2.0 | 1B (4-bit) | MLX BROKEN (degenerate) | attempted; emits repeated-newline garbage via mlx-vlm |
| `mineru` | AGPL-3.0 | ~1.2B (vlm) or pipeline | macOS/MPS | GPU-class quality |
| `olmocr2_mlx` | Apache-2.0 | 7B (4-bit) | MLX BROKEN (Qwen2.5-VL) | attempted; server crashes, generate empty — needs official olmocr pipeline |
| `paddleocr_vl` | Apache-2.0 | 0.9B | CPU wheel on Mac — SLOW (>5 min/pg) | top leaderboard; subset only |

## Judge disagreements (>2 pts, for spot-check)

| paper | backend | axis | Claude | codex |
|---|---|---|---|---|
| ssl_2020_zjunlict | `marker` | tables | 5 | 0 |
| ssl_2020_zjunlict | `granite_docling_mlx` | tables | 5 | 0 |
| ssl_2020_zjunlict | `glm_ocr_mlx` | tables | 5 | 0 |
| ssl_2020_zjunlict | `docling_standard` | tables | 4 | 0 |
| ssl_2020_tigers | `docling_standard` | structure | 1 | 4 |
| ssl_2025_delft | `glm_ocr_mlx` | structure | 6 | 9 |
| ssl_2025_delft | `docling_standard` | tables | 6 | 10 |
| arxiv_ddpm | `granite_docling_mlx` | tables | 7 | 3 |
| arxiv_ddpm | `glm_ocr_mlx` | tables | 4 | 0 |
| arxiv_ddpm | `marker` | tables | 4 | 0 |
| arxiv_bert | `docling_standard` | tables | 4 | 0 |
| arxiv_bert | `glm_ocr_mlx` | tables | 5 | 0 |
| arxiv_bert | `marker` | tables | 5 | 0 |
| arxiv_bert | `granite_docling_mlx` | tables | 4 | 0 |
| arxiv_resnet | `marker` | tables | 5 | 0 |
| arxiv_resnet | `granite_docling_mlx` | tables | 5 | 0 |
| arxiv_resnet | `glm_ocr_mlx` | tables | 5 | 0 |
| arxiv_resnet | `docling_standard` | tables | 5 | 0 |
| arxiv_adam | `granite_docling_mlx` | tables | 6 | 3 |
| arxiv_instructgpt | `marker` | tables | 5 | 0 |
| arxiv_instructgpt | `docling_standard` | tables | 5 | 0 |
| arxiv_instructgpt | `glm_ocr_mlx` | tables | 5 | 0 |
| arxiv_instructgpt | `glm_ocr_mlx` | math | 8 | 5 |
| arxiv_instructgpt | `granite_docling_mlx` | tables | 6 | 1 |
| arxiv_instructgpt | `granite_docling_mlx` | math | 7 | 4 |

## Limitations

- Judges see a page *sample* and the *start* of each Markdown; full per-page-aligned judging was deferred.
- Corpus is a 14–15 PDF *selection* (mostly born-digital arXiv + RoboCup TDPs); not representative of scans/appendices.
- Uniform cleaning is paper-siphon-shaped and may help/hurt backends unevenly; recommendation is on cleaned (shipping) output.

