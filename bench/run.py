#!/usr/bin/env python
"""Orchestrator for the paper-siphon backend benchmark.

Everything is resumable: a step whose output already exists on disk is skipped.

Subcommands:
  list                      show backends and availability
  download                  fetch all corpus PDFs
  render                    render sampled page images for judging
  smoke   --backend B       2-page smoke test (time / s-per-page) before full run
  convert --backend B [--paper P]   run a backend across the corpus (cached)
  metrics                   (re)compute auto-metrics for all cached outputs
  packets                   build blinded judge packets
  judge-codex [--paper P]   run the codex judge
  aggregate                 compute results from verdicts + metrics
  report                    write report/README.md
"""

from __future__ import annotations

import argparse
import sys
import time
import traceback
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))

from lib import (  # noqa: E402
    OUTPUTS, REPORT, Paper, auto_metrics, clean, download, load_manifest, log,
    page_count, pdf_text, read_json, render_pages, write_json,
)


def _papers(args) -> list[Paper]:
    papers = load_manifest()
    if getattr(args, "paper", None):
        papers = [p for p in papers if p.id == args.paper]
        if not papers:
            sys.exit(f"no such paper: {args.paper}")
    return papers


def _backends():
    from backends import ALL, BY_NAME
    return ALL, BY_NAME


# --------------------------------------------------------------------------- #
def cmd_list(args) -> None:
    ALL, _ = _backends()
    for b in ALL:
        ok, reason = b.is_available()
        log(f"{b.name:22s} available={ok!s:5s} {reason}")


def cmd_download(args) -> None:
    for p in _papers(args):
        path = download(p)
        log(f"{p.id}: {path.stat().st_size // 1024} KB, {page_count(p)} pages")


def cmd_render(args) -> None:
    for p in _papers(args):
        download(p)
        render_pages(p)


def _truncate_pdf(src: Path, n: int) -> Path:
    import fitz

    dst = BENCH / "outputs" / "_smoke" / f"{src.stem}_first{n}.pdf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return dst
    doc = fitz.open(src)
    out = fitz.open()
    out.insert_pdf(doc, from_page=0, to_page=min(n, doc.page_count) - 1)
    out.save(str(dst))
    out.close(); doc.close()
    return dst


def cmd_smoke(args) -> None:
    _, BY_NAME = _backends()
    b = BY_NAME[args.backend]
    ok, reason = b.is_available()
    log(f"smoke {b.name}: available={ok} {reason}")
    papers = _papers(args)[:2]
    for p in papers:
        download(p)
        small = _truncate_pdf(p.pdf_path, 2)
        t0 = time.time()
        try:
            raw = b.convert(small)
            dt = time.time() - t0
            log(f"  {p.id}: OK {dt:.1f}s ({dt/2:.1f}s/page), {len(raw)} chars")
        except Exception as e:
            dt = time.time() - t0
            log(f"  {p.id}: FAIL after {dt:.1f}s: {type(e).__name__}: {str(e)[:300]}")


def cmd_convert(args) -> None:
    _, BY_NAME = _backends()
    b = BY_NAME[args.backend]
    ok, reason = b.is_available()
    for p in _papers(args):
        pdir = OUTPUTS / p.id
        meta_path = pdir / f"{b.name}.meta.json"
        clean_path = pdir / f"{b.name}.clean.md"
        prev = read_json(meta_path)
        if clean_path.exists() and prev and not prev.get("error"):
            log(f"{p.id}/{b.name}: cached, skip")
            continue
        if not ok:
            write_json(meta_path, {"backend": b.name, "paper": p.id,
                                   "error": f"unavailable: {reason}"})
            log(f"{p.id}/{b.name}: unavailable ({reason})")
            continue
        download(p)
        pdir.mkdir(parents=True, exist_ok=True)
        log(f"{p.id}/{b.name}: converting…")
        t0 = time.time()
        try:
            raw = b.convert(p.pdf_path)
        except Exception as e:
            write_json(meta_path, {
                "backend": b.name, "paper": p.id,
                "error": f"{type(e).__name__}: {str(e)[:500]}",
                "trace": traceback.format_exc()[-1500:],
                "seconds": round(time.time() - t0, 1),
            })
            log(f"{p.id}/{b.name}: ERROR {type(e).__name__}: {str(e)[:200]}")
            continue
        dt = time.time() - t0
        cleaned = clean(raw)
        (pdir / f"{b.name}.md").write_text(raw)
        clean_path.write_text(cleaned)
        pages = page_count(p)
        met = auto_metrics(cleaned, pages, ref_text=pdf_text(p))
        write_json(meta_path, {
            "backend": b.name, "paper": p.id, "error": None,
            "seconds": round(dt, 1), "pages": pages,
            "s_per_page": round(dt / max(pages, 1), 2), "metrics": met,
        })
        log(f"{p.id}/{b.name}: OK {dt:.1f}s ({dt/max(pages,1):.1f}s/pg) "
            f"recall={met.get('ref_word_recall','-')} leaked={met['leaked_frac']}")


def cmd_metrics(args) -> None:
    for p in _papers(args):
        ref = pdf_text(p)
        pages = page_count(p)
        pdir = OUTPUTS / p.id
        for meta_path in pdir.glob("*.meta.json"):
            meta = read_json(meta_path)
            if not meta or meta.get("error"):
                continue
            clean_path = pdir / f"{meta['backend']}.clean.md"
            if clean_path.exists():
                meta["metrics"] = auto_metrics(clean_path.read_text(), pages, ref)
                write_json(meta_path, meta)
    log("metrics recomputed")


def cmd_packets(args) -> None:
    from judge import build_packet

    _, BY_NAME = _backends()
    names = list(BY_NAME.keys())
    for p in _papers(args):
        pk = build_packet(p, names)
        n = len(pk["labels"]) if pk else 0
        log(f"{p.id}: packet with {n} outputs")


def cmd_judge_codex(args) -> None:
    from judge import codex_judge

    for p in _papers(args):
        v = codex_judge(p)
        log(f"{p.id}: codex verdict {'ok' if v and v.get('scores') else 'FAILED'}")


def cmd_aggregate(args) -> None:
    from aggregate import aggregate
    aggregate()


def cmd_report(args) -> None:
    from aggregate import aggregate, write_report
    write_report(aggregate())
    log(f"report -> {REPORT / 'README.md'}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ["list", "download", "render", "metrics", "packets",
                 "judge-codex", "aggregate", "report"]:
        s = sub.add_parser(name)
        s.add_argument("--paper")
    for name in ["smoke", "convert"]:
        s = sub.add_parser(name)
        s.add_argument("--backend", required=True)
        s.add_argument("--paper")
    args = ap.parse_args()
    {
        "list": cmd_list, "download": cmd_download, "render": cmd_render,
        "smoke": cmd_smoke, "convert": cmd_convert, "metrics": cmd_metrics,
        "packets": cmd_packets, "judge-codex": cmd_judge_codex,
        "aggregate": cmd_aggregate, "report": cmd_report,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
