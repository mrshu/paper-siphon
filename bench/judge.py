"""Blinded dual-LLM judging.

Per paper we build a *blinded packet*: each available backend's cleaned markdown
is relabeled to a random letter (deterministic per paper) in randomized order,
with the label->backend keymap stored separately so judges never see backend
names. Both judges receive the same packet + the same sampled page images and
must (a) score each labeled output 0-10 on four anchored axes with page
evidence, and (b) rank the outputs best->worst (pairwise signal robust to score
saturation).

- codex_judge(): pure subprocess (`codex exec -i <images>`), implemented here.
- The Claude judge is orchestrated by the main agent via subagents that read
  packet.json; this module only builds packets and stores verdicts.
"""

from __future__ import annotations

import json
import random
import re
import string
import subprocess
from pathlib import Path

from lib import AXES, JUDGE, Paper, read_json, write_json

# Judge on the first ~18k chars of each output, to better cover the ~6-10 page
# images shown (tables/math often appear a few pages in). Both judges flagged
# that an 8k cap only reached ~page 5.
MD_JUDGE_CHARS = 18000

RUBRIC = f"""\
You are grading how faithfully several PDF->Markdown converters reproduced an
academic paper. You are shown a SAMPLE of the paper's page images (not all
pages) and, for each converter, the START of its Markdown output (labeled with a
letter). Judge ONLY the content visible in the shown page images; do not penalize
a converter for content from pages you were not shown.

Score each labeled output on four axes, integer 0-10, using these anchors:
- text: prose fidelity. Deduct for missing/dropped paragraphs, garbled words,
  merged line-numbers into text, duplicated or repeated lines, hallucinated text.
- tables: are tables present and structurally correct (rows/cols/headers as
  Markdown or HTML)? 0 if tables in the images are missing or mangled.
- math: are equations/inline math captured as usable LaTeX/text? Deduct for lost
  symbols, dropped equations, OCR gibberish where math should be.
- structure: reading order and hierarchy — headings, section order, column order.
  Deduct for column-order inversion, wrong heading levels, jumbled order.

Anchors: 10=faithful, minor nits; 8=good, small errors; 5=usable but clear
damage; 2=largely broken; 0=absent/unusable. Cite concrete evidence (e.g.
"Table 2 header row missing", "eq. 3 symbols dropped") in one line per output.

Then produce a ranking of all labels from BEST to WORST overall.

Return ONLY minified JSON, no prose, exactly:
{{"scores":{{"<LABEL>":{{"text":int,"tables":int,"math":int,"structure":int,"evidence":"..."}}, ...}},"ranking":["<LABEL best>", ...]}}
Axes keys must be exactly: {AXES}.
"""


def _labels(n: int) -> list[str]:
    return list(string.ascii_uppercase[:n])


def build_packet(paper: Paper, backend_names: list[str]) -> dict | None:
    """Blind the available outputs for one paper. Deterministic per paper id."""
    from lib import OUTPUTS

    avail = []
    for b in backend_names:
        md = OUTPUTS / paper.id / f"{b}.clean.md"
        if md.exists():
            avail.append((b, md))
    if len(avail) < 2:
        return None

    rng = random.Random(f"blind::{paper.id}")
    rng.shuffle(avail)
    labels = _labels(len(avail))
    keymap = {lab: b for lab, (b, _) in zip(labels, avail)}
    packet = {
        "paper": paper.id,
        "labels": {
            lab: (md.read_text()[:MD_JUDGE_CHARS]) for lab, (_, md) in zip(labels, avail)
        },
    }
    pdir = JUDGE / paper.id
    write_json(pdir / "keymap.json", keymap)
    write_json(pdir / "packet.json", packet)
    return packet


def page_images(paper: Paper) -> list[Path]:
    pdir = JUDGE / paper.id / "pages"
    names = read_json(pdir / "pages.json") or []
    return [pdir / n for n in names]


def _balanced_objects(text: str):
    """Yield every balanced {...} substring (brace-matched, string-aware)."""
    starts = [i for i, c in enumerate(text) if c == "{"]
    for start in starts:
        depth = 0
        in_str = False
        esc = False
        for j in range(start, len(text)):
            c = text[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        yield text[start:j + 1]
                        break


def _parse_verdict(text: str, labels: list[str]) -> dict | None:
    # Prefer the LAST valid object that carries scores+ranking (the model's
    # final answer), ignoring any JSON-looking content echoed earlier.
    best = None
    for cand in _balanced_objects(text):
        if '"scores"' not in cand or '"ranking"' not in cand:
            continue
        try:
            obj = json.loads(cand)
        except json.JSONDecodeError:
            continue
        if isinstance(obj.get("scores"), dict) and isinstance(obj.get("ranking"), list):
            best = obj
    return best


def codex_judge(paper: Paper, timeout: int = 900) -> dict | None:
    pdir = JUDGE / paper.id
    out_path = pdir / "verdict.codex.json"
    cached = read_json(out_path)
    if cached:
        return cached
    packet = read_json(pdir / "packet.json")
    if not packet:
        return None
    labels = list(packet["labels"].keys())
    imgs = page_images(paper)

    body = [RUBRIC, "", "## Converter outputs (Markdown, start of each):"]
    for lab in labels:
        body.append(f"\n### Output {lab}\n```markdown\n{packet['labels'][lab]}\n```")
    prompt = "\n".join(body)

    cmd = ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only"]
    for img in imgs:
        cmd += ["-i", str(img)]
    cmd += ["-"]
    try:
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        write_json(out_path, {"error": "timeout", "scores": {}, "ranking": []})
        return None

    verdict = _parse_verdict(proc.stdout + proc.stderr, labels)
    if verdict is None:
        (pdir / "verdict.codex.raw.txt").write_text(proc.stdout + proc.stderr)
        write_json(out_path, {"error": "unparseable", "scores": {}, "ranking": []})
        return None
    verdict["judge"] = "codex"
    write_json(out_path, verdict)
    return verdict
