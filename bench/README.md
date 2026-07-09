# paper-siphon backend benchmark — results

Corpus: **14 public PDFs** (a *selection*, not a representative benchmark). Judged papers: **14**. Two blinded LLM judges (Claude + codex/GPT) scored anonymized, order-randomized outputs on four anchored axes (0–10) and ranked them best→worst. Every backend's raw Markdown was uniformly cleaned with paper-siphon's `clean_markdown` before judging.

Judge page sample: first 6 pages + up to 10 total incl. table/math pages, rendered at 150 dpi. Judges score only shown pages.

## Bottom line

**`lightonocr2` wins on quality** — overall 8.18/10 (mean of both blinded judges), winning **95%** of head-to-head comparisons across 14 papers — **but it is slow** (~76.9 s/page median). Its lead is on prose fidelity and math; it captures full pages cleanly where the pipeline backends drop equations.

**`glm_ocr_mlx` is the practical pick.** It is a close second on quality (7.43/10) at **~7.0 s/page** — roughly **11× faster** than the winner — with MIT weights and an 0.9B footprint that fits in 8 GB. `marker` is a viable cross-platform third (GPL, slower cold-start). `dots_ocr` is a solid MIT specialist but ~25 s/page.

**Notable failures.** Both `paddleocr_vl` versions score near the bottom **despite topping OmniDocBench**: on this mlx-vlm path they collapse into repetition loops, and 1.6 additionally floods the output with raw `<|LOC_..|>` layout-coordinate tokens — a cautionary example that leaderboard rank does not survive an unofficial Apple-Silicon runtime. `nanonets2` and `olmocr2` (both Qwen2.5-VL OCR finetunes) were attempted across three integration paths (MLX bf16, MLX 4-bit, native float32) and produce empty or gibberish output via mlx-vlm/torch-MPS — they need their official vLLM/CUDA toolchains. `docling_standard` remains far the fastest (~0.6 s/page) and the right default when speed dominates and papers are simple.

## Ranked results (mean of both judges)

| rank | backend | overall | text | tables | math | structure | win-rate | Borda | s/page |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `lightonocr2` | **8.18** | 9.04 | 6.41 | 8.7 | 8.56 | 0.949 | 0.949 | 76.9 |
| 2 | `glm_ocr_mlx` | **7.43** | 8.81 | 4.78 | 8.15 | 7.96 | 0.796 | 0.796 | 7.5 |
| 3 | `marker` | **7.21** | 8.15 | 5.11 | 7.89 | 7.67 | 0.694 | 0.694 | 20.4 |
| 4 | `dots_ocr` | **6.25** | 7.07 | 5.41 | 7.22 | 5.3 | 0.449 | 0.449 | 25.0 |
| 5 | `granite_docling_mlx` | **6.08** | 7.33 | 4.26 | 5.93 | 6.81 | 0.474 | 0.474 | 16.8 |
| 6 | `docling_standard` | **4.87** | 6.7 | 4.48 | 2.59 | 5.7 | 0.327 | 0.327 | 0.6 |
| 7 | `paddleocr_vl_mlx` | **4.42** | 6.26 | 3.07 | 3.37 | 4.96 | 0.291 | 0.291 | 17.2 |
| 8 | `paddleocr_vl_16` | **2.31** | 2.41 | 2.3 | 2.7 | 1.81 | 0.02 | 0.02 | 17.0 |
| 9 | `chandra` | **—** | — | — | — | — | — | — | — |
| 10 | `lightonocr_mlx` | **—** | — | — | — | — | — | — | 23.0 |
| 11 | `mineru` | **—** | — | — | — | — | — | — | — |
| 12 | `olmocr2_mlx` | **—** | — | — | — | — | — | — | 26.8 |
| 13 | `paddleocr_vl` | **—** | — | — | — | — | — | — | — |

*Caveat on the **tables** axis: it reads low for every backend because many judged page-samples (first ~6-10 pages) contain no table, and the two judges handled 'no table visible' differently — codex scored 0, Claude scored a neutral ~5 (see the disagreements list). Treat absolute table scores with caution; the relative ordering still holds.*


## Per-judge overall (bias check)

| backend | Claude | codex |
|---|---|---|
| `lightonocr2` | 8.35 | 8.02 |
| `glm_ocr_mlx` | 7.77 | 7.11 |
| `marker` | 7.63 | 6.8 |
| `dots_ocr` | 6.33 | 6.18 |
| `granite_docling_mlx` | 6.6 | 5.61 |
| `docling_standard` | 5.27 | 4.5 |
| `paddleocr_vl_mlx` | 4.71 | 4.14 |
| `paddleocr_vl_16` | 2.48 | 2.14 |
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
| `lightonocr_mlx` | **15.2** | 23.0 | 914.0 | 5483.7 | 6 |
| `granite_docling_mlx` | **16.8** | 16.8 | 304.4 | 4261.0 | 14 |
| `paddleocr_vl_16` | **17.0** | 17.0 | 338.8 | 4743.0 | 14 |
| `paddleocr_vl_mlx` | **17.2** | 17.2 | 342.8 | 4798.8 | 14 |
| `dots_ocr` | **25.0** | 25.0 | 498.2 | 6975.0 | 14 |
| `olmocr2_mlx` | **25.1** | 26.8 | 421.6 | 1686.3 | 4 |
| `lightonocr2` | **76.9** | 76.9 | 1532.5 | 21455.1 | 14 |

*Median s/page is the fairer per-page figure; the mean is inflated for backends that reload models per document (e.g. marker cold-starts). Per-page times >60 s were excluded as wall-clock artifacts of the host sleeping during the unattended run (compute pauses, `time.time()` does not) — this is why some backends show fewer than 14 timed docs.*


## Auto-metrics (reference-free)

| backend | ref-word-recall | leaked-linenum-frac | dup-line-frac | chars/page |
|---|---|---|---|---|
| `lightonocr2` | 0.89 | 0.0 | 0.053 | 3196.921 |
| `glm_ocr_mlx` | 0.868 | 0.0 | 0.006 | 2699.329 |
| `marker` | 0.914 | 0.0 | 0.004 | 3277.071 |
| `dots_ocr` | 0.871 | 0.0 | 0.056 | 3085.1 |
| `granite_docling_mlx` | 0.88 | 0.0 | 0.005 | 3135.543 |
| `docling_standard` | 0.843 | 0.0 | 0.047 | 3173.436 |
| `paddleocr_vl_mlx` | 0.861 | 0.0 | 0.053 | 2720.829 |
| `paddleocr_vl_16` | 0.786 | 0.0 | 0.217 | 6712.407 |
| `chandra` | — | — | — | — |
| `lightonocr_mlx` | 0.008 | 0.0 | 0.871 | 3258.8 |
| `mineru` | — | — | — | — |
| `olmocr2_mlx` | 0.001 | 0.0 | 0.0 | 181.475 |
| `paddleocr_vl` | — | — | — | — |

## Per-tag overall (where does an edge concentrate?)

| backend | algorithm-blocks | dense-math | engineering | figures | math | math-heavy | multi-column | older-typesetting | real-run | table-heavy | tables |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `lightonocr2` | 8.62 | 8.75 | 8.36 | 6.62 | 8.12 | 8.5 | 8.3 | 7.25 | 8.48 | 7.75 | 8.04 |
| `glm_ocr_mlx` | 7.88 | 7.25 | 7.83 | 7.12 | 7.5 | 6.62 | 7.61 | 6.62 | 8.0 | 7.0 | 7.59 |
| `marker` | 8.25 | 7.25 | 7.56 | 6.62 | 7.68 | 7.5 | 6.77 | 6.62 | 7.66 | 4.88 | 7.29 |
| `dots_ocr` | 7.88 | 5.38 | 6.03 | 6.88 | 6.83 | 6.12 | 6.45 | 5.38 | 6.32 | 6.88 | 6.21 |
| `granite_docling_mlx` | 5.75 | 5.12 | 6.0 | 5.62 | 6.38 | 6.88 | 6.14 | 6.25 | 6.18 | 5.75 | 6.14 |
| `docling_standard` | 5.38 | 4.0 | 4.58 | 4.62 | 5.25 | 4.0 | 5.93 | 3.38 | 4.86 | 5.5 | 4.96 |
| `paddleocr_vl_mlx` | 3.12 | 1.38 | 5.22 | 4.5 | 4.03 | 3.62 | 4.86 | 4.75 | 4.89 | 5.75 | 4.55 |
| `paddleocr_vl_16` | 2.75 | 4.12 | 2.0 | 4.5 | 2.42 | 1.88 | 2.05 | 1.88 | 2.0 | 2.25 | 1.91 |
| `chandra` | — | — | — | — | — | — | — | — | — | — | — |
| `lightonocr_mlx` | — | — | — | — | — | — | — | — | — | — | — |
| `mineru` | — | — | — | — | — | — | — | — | — | — | — |
| `olmocr2_mlx` | — | — | — | — | — | — | — | — | — | — | — |
| `paddleocr_vl` | — | — | — | — | — | — | — | — | — | — | — |

## Availability & errors

- `lightonocr_mlx`: 8 failures — e.g. ssl_2025_first_order: not viable via mlx-vlm 0.6.4: 4-bit MLX quant emits degenerate repeated-newline 
- `olmocr2_mlx`: 10 failures — e.g. ssl_2020_zjunlict: RuntimeError: mlx_generate_runner produced no output
- `mineru`: 3 failures — e.g. ssl_2020_tigers: excluded: TimeoutExpired >1800s on 2 pages (model download + CPU inference)
- `paddleocr_vl`: 3 failures — e.g. ssl_2020_tigers: excluded: >5 min/page (CPU-only wheel on Mac), smoke unfinished after 10 min
- `chandra`: 3 failures — e.g. ssl_2020_tigers: excluded: >7 min/page, 2-page smoke unfinished after 15 min (9.9GB model, CPU fa

## Operational fit

| backend | license | model size | Apple Silicon | note |
|---|---|---|---|---|
| `lightonocr2` | Apache-2.0 | 1B | native MLX (bf16) | v2 works (v1 was degenerate); slow ~77 s/pg |
| `glm_ocr_mlx` | MIT weights / Apache code | 0.9B | native MLX (direct-server path) | best-Mac candidate |
| `marker` | GPL-3.0 code / model license | ~few 100 MB | MPS | table/math LLM opt-in |
| `dots_ocr` | MIT | 1.7B | native MLX (bf16, --trust-remote-code) | strong specialist; ~25 s/pg |
| `granite_docling_mlx` | Apache-2.0 | 258M | native MLX | current --vlm |
| `docling_standard` | MIT | small (docling models) | native | current default |
| `paddleocr_vl_mlx` | Apache-2.0 | 0.9B | native MLX (bf16) | base PaddleOCR-VL; MLX fixes: idempotent sanitize + greedy decode |
| `paddleocr_vl_16` | Apache-2.0 | 0.9B | native MLX (bf16) | current 1.6 release; higher OmniDocBench, ~fast |
| `chandra` | modified OpenRAIL-M (research/personal/<$2M) | 9.9 GB (hf) | MPS w/ heavy CPU fallback — SLOW | opt-in; subset only |
| `lightonocr_mlx` | Apache-2.0 | 1B (4-bit) | MLX BROKEN (degenerate) | attempted; emits repeated-newline garbage via mlx-vlm |
| `mineru` | AGPL-3.0 | ~1.2B (vlm) or pipeline | macOS/MPS | GPU-class quality |
| `olmocr2_mlx` | Apache-2.0 | 7B (4-bit) | MLX BROKEN (Qwen2.5-VL) | attempted; server crashes, generate empty — needs official olmocr pipeline |
| `paddleocr_vl` | Apache-2.0 | 0.9B | CPU wheel on Mac — SLOW (>5 min/pg) | top leaderboard; subset only |

## Judge disagreements (>2 pts, for spot-check)

| paper | backend | axis | Claude | codex |
|---|---|---|---|---|
| ssl_2020_zjunlict | `glm_ocr_mlx` | tables | 5 | 0 |
| ssl_2020_zjunlict | `dots_ocr` | tables | 5 | 0 |
| ssl_2020_zjunlict | `paddleocr_vl_mlx` | tables | 5 | 0 |
| ssl_2020_zjunlict | `paddleocr_vl_16` | tables | 5 | 0 |
| ssl_2020_zjunlict | `lightonocr2` | tables | 5 | 0 |
| ssl_2020_zjunlict | `marker` | tables | 5 | 0 |
| ssl_2020_zjunlict | `docling_standard` | tables | 5 | 0 |
| ssl_2020_zjunlict | `granite_docling_mlx` | tables | 5 | 0 |
| ssl_2020_tigers | `docling_standard` | structure | 1 | 4 |
| ssl_2025_delft | `lightonocr2` | tables | 5 | 10 |
| ssl_2025_delft | `marker` | tables | 5 | 10 |
| ssl_2025_delft | `docling_standard` | tables | 5 | 10 |
| ssl_2025_delft | `glm_ocr_mlx` | tables | 5 | 10 |
| ssl_2025_delft | `paddleocr_vl_16` | tables | 5 | 10 |
| ssl_2025_delft | `paddleocr_vl_16` | math | 2 | 6 |
| ssl_2025_delft | `dots_ocr` | tables | 5 | 10 |
| ssl_2025_delft | `paddleocr_vl_mlx` | tables | 5 | 10 |
| ssl_2025_delft | `granite_docling_mlx` | tables | 5 | 10 |
| arxiv_attention | `paddleocr_vl_16` | tables | 5 | 0 |
| arxiv_ddpm | `marker` | tables | 6 | 3 |
| arxiv_bert | `paddleocr_vl_16` | tables | 3 | 0 |
| arxiv_bert | `paddleocr_vl_mlx` | tables | 5 | 0 |
| arxiv_bert | `docling_standard` | tables | 5 | 0 |
| arxiv_bert | `granite_docling_mlx` | tables | 5 | 0 |
| arxiv_bert | `dots_ocr` | tables | 5 | 0 |
| arxiv_bert | `glm_ocr_mlx` | tables | 5 | 0 |
| arxiv_bert | `lightonocr2` | tables | 8 | 2 |
| arxiv_bert | `marker` | tables | 5 | 0 |
| arxiv_resnet | `glm_ocr_mlx` | tables | 5 | 0 |
| arxiv_resnet | `lightonocr2` | tables | 5 | 1 |
| arxiv_resnet | `lightonocr2` | structure | 5 | 8 |
| arxiv_resnet | `dots_ocr` | tables | 5 | 0 |
| arxiv_resnet | `paddleocr_vl_mlx` | tables | 5 | 0 |
| arxiv_resnet | `docling_standard` | tables | 5 | 0 |
| arxiv_resnet | `marker` | tables | 5 | 0 |
| arxiv_resnet | `paddleocr_vl_16` | tables | 5 | 0 |
| arxiv_resnet | `granite_docling_mlx` | tables | 5 | 0 |
| arxiv_adam | `lightonocr2` | tables | 5 | 9 |
| arxiv_adam | `glm_ocr_mlx` | tables | 5 | 8 |
| arxiv_adam | `marker` | tables | 5 | 8 |

… and 27 more.

## Limitations

- Judges see a page *sample* and the *start* of each Markdown; full per-page-aligned judging was deferred.
- Corpus is a 14–15 PDF *selection* (mostly born-digital arXiv + RoboCup TDPs); not representative of scans/appendices.
- Uniform cleaning is paper-siphon-shaped and may help/hurt backends unevenly; recommendation is on cleaned (shipping) output.

