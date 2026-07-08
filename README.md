# Paper Siphon

**Extract clean Markdown from academic PDFs** - like drinking through a straw.

Academic papers come with artifacts: awkward page breaks, mangled tables, or even line numbers.
Paper Siphon filters them out, leaving you with clean, readable Markdown.

```
paper-siphon paper.pdf
```

That's it. Your paper is now `paper.md`.

---

## Features

- **Smart whitespace** - Collapses excessive blank lines, normalizes spacing
- **Table preservation** - Keeps your data tables intact and formatted
- **Formula support** - Optional enrichment for mathematical expressions
- **Line number removal** - Automatically strips the margin numbers (when present)
- **VLM backend** - `--vlm` uses GLM-OCR on Apple Silicon (marker elsewhere) for
  complex layouts, heavy math, and broken encodings — see [the benchmark](bench/README.md)
- **Self-healing** - Auto-escalates to the VLM backend when the fast default
  output looks garbled or drops equations

## Installation

```bash
# With uv (recommended)
uv pip install paper-siphon

# With pip
pip install paper-siphon
```

The `--vlm` backend (GLM-OCR on Apple Silicon, marker elsewhere) needs no extra
install — it runs in an isolated environment provisioned on demand, and only
requires [`uv`](https://docs.astral.sh/uv/) on your PATH (already true if you
use `uvx`). The first `--vlm` run downloads the model (~2 GB), then caches it.

## Usage

### Quick start (no install)

```bash
uvx paper-siphon paper.pdf                # Run directly with uvx
```

### Basic

```bash
paper-siphon paper.pdf                    # Creates paper.md
paper-siphon paper.pdf -o notes.md        # Custom output path
```

### From URL (including arXiv)

```bash
paper-siphon https://arxiv.org/pdf/1706.03762.pdf
```

**Tip:** For arXiv papers, just change `/abs/` to `/pdf/` in the URL:
```
https://arxiv.org/abs/1706.03762  →  https://arxiv.org/pdf/1706.03762.pdf
```

(That's "Attention Is All You Need" - the Transformer paper)

### Advanced

```bash
paper-siphon --vlm paper.pdf              # Force the VLM backend (GLM-OCR / marker)
paper-siphon --no-escalate paper.pdf      # Don't auto-retry with the VLM backend
paper-siphon --enrich-formula paper.pdf   # Formula enrichment on the default pipeline
paper-siphon --no-mlx --vlm paper.pdf     # Force the marker backend even on a Mac
paper-siphon -v paper.pdf                 # Verbose logging
```

By default, the fast pipeline runs first and paper-siphon **automatically
re-runs with the VLM backend** if that output looks garbled (a font-decoding
failure) or dropped its equations. Use `--vlm` to force the VLM backend from the
start, or `--no-escalate` to keep the fast output as-is.

## How It Works

Paper Siphon uses [Docling](https://github.com/DS4SD/docling) for PDF parsing, then applies
post-processing to clean up common academic paper artifacts:

1. **PDF parsing** - Extracts structure, text, and tables (fast Docling pipeline)
2. **Quality check** - Detects font-decoding failures (garbled glyphs) and
   dropped equations; escalates to the VLM backend when needed
3. **Line number filtering** - Removes standalone 1-4 digit numbers (common in journal formats)
4. **Whitespace normalization** - Collapses multiple blank lines

The VLM backend (`--vlm` or auto-escalation) runs GLM-OCR on Apple Silicon and
marker elsewhere, in an isolated environment so its dependencies never interfere
with the fast default pipeline. See [`bench/README.md`](bench/README.md) for how
these backends were chosen.

## Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output file path (default: input with `.md` extension) |
| `--vlm` | Force the VLM backend (GLM-OCR on Apple Silicon, marker elsewhere) |
| `--mlx/--no-mlx` | Use GLM-OCR/MLX on Apple Silicon; `--no-mlx` forces marker |
| `--escalate/--no-escalate` | Auto-retry with the VLM backend on garbled/math-dropping output (default: on) |
| `--enrich-formula` | Enable formula enrichment on the default pipeline (slow, CPU-bound) |
| `-v, --verbose` | Enable debug logging |

## Development

```bash
# Clone and install
git clone https://github.com/mrshu/paper-siphon.git
cd paper-siphon
uv sync --dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=paper_siphon
```

## License

MIT

---

*Stop wrestling with PDFs. Just siphon the good stuff.*
