# GLM-OCR VLM backend + auto-escalation — design

**Date:** 2026-07-09
**Goal:** Make `--vlm` use GLM-OCR (the benchmark winner) on Apple Silicon and
marker elsewhere, and auto-escalate the fast default pipeline to the VLM path
when its output looks garbled or drops math.

## Motivation

The backend benchmark (`bench/`, 2026-07-08) showed GLM-OCR beats paper-siphon's
current `--vlm` (GraniteDocling) on both quality (7.62 vs 5.93 /10) and speed
(7 vs 17 s/page on M4 Max), and that the fast default pipeline fails badly on
two real cases: math-heavy papers (drops equations as `formula-not-decoded`)
and pathological font-encoding (emits scrambled glyphs, e.g. the RoboCup TIGERs
TDP). GLM-OCR recovers both. So: upgrade the VLM path, and make the tool
self-heal when the default output is bad.

## Decisions (confirmed with user)

- `--vlm` → GLM-OCR on Apple Silicon; marker on other platforms. GraniteDocling
  is retired.
- Non-Apple-Silicon VLM path uses marker (cross-platform, benchmark runner-up).
- Auto-escalation is on by default.

## Architecture

### `paper_siphon/backends.py` (new)
Backend functions returning **raw** markdown; `main()` applies `clean_markdown`
uniformly (unchanged from today). All heavy imports are lazy so the base install
(`click` + `docling`) is untouched.

- `vlm_convert(pdf, use_mlx) -> str`: dispatches to GLM-OCR (Apple Silicon and
  `use_mlx`) or marker (otherwise).
- `glm_ocr_convert(pdf) -> str`: render pages (PyMuPDF, 150 dpi, cap 30) →
  GLM-OCR via `mlx-vlm` **in-process** (`mlx_vlm.generate`); if in-process fails
  at load/inference, fall back to the mlx-vlm OpenAI-compatible server (the path
  proven in the benchmark). Model `mlx-community/GLM-OCR-bf16` (~2 GB), lazy
  first-run download. Per-page OCR prompt → concatenated markdown.
- `marker_convert(pdf) -> str`: `marker-pdf` via `marker_single`, MPS/CPU. Raises
  a clear "install paper-siphon[marker]" error if unavailable.
- `is_apple_silicon() -> bool`.

### `paper_siphon/quality.py` (new)
Dependency-free heuristics on the default pipeline's markdown (no PyMuPDF
needed — operate on the docling output string alone):

- `looks_garbled(md) -> bool`: fraction of characters in "symbol/dingbat"
  Unicode ranges (the `❚■●❊❘` glyph-decode failure) over a threshold, on a
  document that has substantial text.
- `dropped_math(md) -> bool`: presence of Docling's `formula-not-decoded`
  markers (or `<!-- formula-not-decoded -->`).
- `needs_escalation(md) -> (bool, reason)`: OR of the above.

### `cli.py` changes
- `--vlm`: standard → `vlm_convert`.
- `--mlx/--no-mlx`: `--no-mlx` forces the marker path even on Apple Silicon.
- `--no-escalate`: disable auto-escalation.
- Retire `create_vlm_converter` (GraniteDocling); keep `create_standard_converter`.
- Flow: if `--vlm`, convert via `vlm_convert`. Else convert via standard
  pipeline; if escalation enabled and `needs_escalation` and a VLM path is
  available, print a notice and re-run via `vlm_convert`, using that output.
- Always clean + write, as today.

## Dependencies (`pyproject.toml`)
- `[project.optional-dependencies] mlx` gains `pymupdf` (page rendering).
- New `marker = ["marker-pdf"]` extra.
- Base dependencies unchanged.

## Testing
Fast, dep-free unit tests (heavy backends mocked):
- `quality.py`: garbled/dropped-math strings escalate; clean markdown does not;
  edge cases (empty, all-symbols-but-tiny) don't false-positive.
- backend selection: Apple Silicon+mlx → GLM; non-Mac or `--no-mlx` → marker.
- CLI: `--vlm` routes to `vlm_convert`; escalation path triggers on garbled
  standard output and is skipped with `--no-escalate`; output still cleaned.

## Docs
- README options table: `--vlm` (GLM-OCR / marker), add `--no-escalate`.
- SKILL.md decision guide: default self-heals; `--vlm` forces GLM-OCR.

## Non-goals / risks
- Not bundling MinerU/Chandra/PaddleOCR-VL/olmOCR-2 (benchmark: non-viable on
  Apple Silicon).
- GLM-OCR in-process generate is preferred but unverified for this arch; the
  benchmark verified the *server* path, which is the fallback.
- First `--vlm` run downloads ~2 GB (GLM-OCR weights); acceptable and lazy.
- Escalation detectors are heuristic; `--no-escalate` and explicit `--vlm`
  remain as manual overrides.
