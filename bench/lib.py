"""Shared helpers for the paper-siphon backend benchmark.

Everything here is deterministic and content-addressed: rendered pages, backend
outputs, and metrics are cached on disk so partial runs resume cheaply.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import yaml

BENCH = Path(__file__).resolve().parent
REPO = BENCH.parent
PDFS = BENCH / "corpus" / "pdfs"
OUTPUTS = BENCH / "outputs"
JUDGE = BENCH / "judge"
REPORT = BENCH  # the generated report lives at bench/README.md

# Render/judge parameters (recorded in the report — no silent knobs).
RENDER_DPI = 150
# Pages judged per paper: the first N, plus any page whose text suggests a table
# or formula, capped so long papers stay tractable. Cap is surfaced in report.
JUDGE_FIRST_PAGES = 6
JUDGE_MAX_PAGES = 10

AXES = ["text", "tables", "math", "structure"]


@dataclass(frozen=True)
class Paper:
    id: str
    url: str
    tags: list[str]

    @property
    def pdf_path(self) -> Path:
        return PDFS / f"{self.id}.pdf"


def load_manifest() -> list[Paper]:
    data = yaml.safe_load((BENCH / "corpus" / "manifest.yaml").read_text())
    return [Paper(id=p["id"], url=p["url"], tags=p.get("tags", [])) for p in data["papers"]]


def log(msg: str) -> None:
    print(f"[bench] {msg}", flush=True)


# --------------------------------------------------------------------------- #
# Download
# --------------------------------------------------------------------------- #
def download(paper: Paper) -> Path:
    PDFS.mkdir(parents=True, exist_ok=True)
    if paper.pdf_path.exists() and paper.pdf_path.stat().st_size > 1000:
        return paper.pdf_path
    log(f"downloading {paper.id} <- {paper.url}")
    req = urllib.request.Request(paper.url, headers={"User-Agent": "Mozilla/5.0 paper-siphon-bench"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    if not data[:5] == b"%PDF-":
        raise RuntimeError(f"{paper.id}: downloaded content is not a PDF (starts {data[:8]!r})")
    paper.pdf_path.write_bytes(data)
    return paper.pdf_path


# --------------------------------------------------------------------------- #
# Rendering (PyMuPDF)
# --------------------------------------------------------------------------- #
def _looks_tabular_or_math(text: str) -> bool:
    if text.count("|") >= 6:
        return True
    # many short numeric-heavy lines => table; math symbols => formula page
    digits = sum(c.isdigit() for c in text)
    if digits > 40 and text.count("\n") > 8:
        return True
    if re.search(r"[∑∫√≤≥≈∈∝⊗∇πλμσθ]|\\frac|\\sum|\\int|=\s*\d", text):
        return True
    return False


def render_pages(paper: Paper) -> list[Path]:
    """Render a capped, representative sample of pages to PNGs. Cached."""
    import fitz  # PyMuPDF

    out_dir = JUDGE / paper.id / "pages"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = out_dir / "pages.json"
    if manifest.exists():
        return [out_dir / name for name in json.loads(manifest.read_text())]

    doc = fitz.open(paper.pdf_path)
    n = doc.page_count
    chosen: list[int] = list(range(min(JUDGE_FIRST_PAGES, n)))
    # add later pages that look like tables/math until the cap
    for i in range(JUDGE_FIRST_PAGES, n):
        if len(chosen) >= JUDGE_MAX_PAGES:
            break
        if _looks_tabular_or_math(doc.load_page(i).get_text()):
            chosen.append(i)
    chosen = sorted(set(chosen))[:JUDGE_MAX_PAGES]

    names: list[str] = []
    zoom = RENDER_DPI / 72.0
    for i in chosen:
        pix = doc.load_page(i).get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        name = f"p{i + 1:03d}.png"
        pix.save(str(out_dir / name))
        names.append(name)
    doc.close()
    manifest.write_text(json.dumps(names))
    log(f"rendered {paper.id}: {len(names)}/{n} pages -> {out_dir}")
    return [out_dir / name for name in names]


def render_all_pages(pdf_path: Path, out_dir: Path, dpi: int = 150, cap: int = 30) -> list[Path]:
    """Render up to `cap` pages of a PDF to PNGs for full-document conversion."""
    import fitz

    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    paths = []
    for i in range(min(doc.page_count, cap)):
        dst = out_dir / f"p{i + 1:03d}.png"
        if not dst.exists():
            doc.load_page(i).get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(str(dst))
        paths.append(dst)
    doc.close()
    return paths


def page_count(paper: Paper) -> int:
    import fitz

    doc = fitz.open(paper.pdf_path)
    n = doc.page_count
    doc.close()
    return n


# --------------------------------------------------------------------------- #
# Uniform cleaning (paper-siphon's own post-processing, applied to every backend)
# --------------------------------------------------------------------------- #
def clean(markdown: str) -> str:
    sys.path.insert(0, str(REPO))
    from paper_siphon.cleaning import clean_markdown

    return clean_markdown(markdown)


# --------------------------------------------------------------------------- #
# Auto-metrics (reference-free, cheap gross-failure detectors)
# --------------------------------------------------------------------------- #
_LEAKED_NUM = re.compile(r"(?m)^\s*\d{1,4}\s*$")
_HEADING = re.compile(r"(?m)^#{1,6}\s+\S")
_TABLE_ROW = re.compile(r"(?m)^\s*\|.*\|\s*$")
_EQ = re.compile(r"\$[^$\n]+\$|\\\[|\\begin\{(equation|align|array)")


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def pdf_text(paper: Paper) -> str:
    """Full born-digital text of the PDF (empty for scans)."""
    import fitz

    doc = fitz.open(paper.pdf_path)
    text = "\n".join(doc.load_page(i).get_text() for i in range(doc.page_count))
    doc.close()
    return text


def auto_metrics(markdown: str, pages: int, ref_text: str = "") -> dict:
    lines = markdown.splitlines()
    nonblank = [ln.strip() for ln in lines if ln.strip()]
    leaked = len(_LEAKED_NUM.findall(markdown))

    # duplicate-line rate: repeated substantial lines signal loops/duplication
    long_lines = [ln for ln in nonblank if len(ln) > 25]
    dup_frac = 0.0
    if long_lines:
        dup_frac = round(1 - len(set(long_lines)) / len(long_lines), 4)

    m = {
        "chars": len(markdown),
        "chars_per_page": round(len(markdown) / max(pages, 1), 1),
        "nonblank_lines": len(nonblank),
        "headings": len(_HEADING.findall(markdown)),
        "table_rows": len(_TABLE_ROW.findall(markdown)),
        "equations": len(_EQ.findall(markdown)),
        "leaked_line_numbers": leaked,
        "leaked_frac": round(leaked / max(len(nonblank), 1), 4),
        "dup_line_frac": dup_frac,
    }

    # Reference-based (born-digital only): fraction of reference word-bigrams
    # recovered = recall proxy; catches truncation and dropped sections.
    if ref_text and len(ref_text) > 200:
        ref_set = set(_words(ref_text))
        out_words = set(_words(markdown))
        recall = len(ref_set & out_words) / max(len(ref_set), 1)
        m["ref_word_recall"] = round(recall, 4)
        m["len_ratio_vs_pdftext"] = round(len(markdown) / max(len(ref_text), 1), 3)
    return m


# --------------------------------------------------------------------------- #
# JSON helpers
# --------------------------------------------------------------------------- #
def read_json(path: Path) -> dict | None:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return None
    return None


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))


def run_cmd(cmd: list[str], timeout: int, env: dict | None = None) -> tuple[int, str]:
    """Run a subprocess, capturing combined output. Returns (rc, output)."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=env
        )
        return proc.returncode, (proc.stdout + proc.stderr)
    except subprocess.TimeoutExpired as e:
        return 124, f"TIMEOUT after {timeout}s\n{e.stdout or ''}{e.stderr or ''}"
    except FileNotFoundError as e:
        return 127, str(e)
