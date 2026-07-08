"""Heuristics to decide when the fast default pipeline produced bad output and
the tool should escalate to the VLM backend.

All checks operate on the produced Markdown string alone — no extra
dependencies, no access to the source PDF — so they are cheap and always
available. They target the two failure modes the backend benchmark surfaced:

1. Font-decoding collapse: Docling emits runs of dingbat/symbol glyphs
   (e.g. ``❚■●❊❘``) or leaked glyph names when a PDF uses a custom encoding,
   even though the page text is perfectly readable.
2. Dropped mathematics: Docling leaves ``formula-not-decoded`` markers instead
   of the equation on math-heavy pages.
"""

from __future__ import annotations

# Unicode ranges dominated by the glyph-decode failure: arrows, box drawing,
# geometric shapes, miscellaneous symbols, dingbats, and math alphanumerics.
_GARBLE_RANGES = (
    (0x2190, 0x21FF),   # arrows
    (0x2300, 0x23FF),   # misc technical
    (0x2500, 0x257F),   # box drawing
    (0x2580, 0x259F),   # block elements
    (0x25A0, 0x25FF),   # geometric shapes
    (0x2600, 0x26FF),   # miscellaneous symbols
    (0x2700, 0x27BF),   # dingbats
    (0x2B00, 0x2BFF),   # miscellaneous symbols and arrows
)
# NB: Mathematical Alphanumeric Symbols (U+1D400-1D7FF: 𝔼, 𝒩, 𝓛, …) are
# deliberately NOT counted as garble — they are legitimate notation in the
# math-heavy papers this tool targets.

# Above this fraction of non-space characters being "garble glyphs" on a
# document with real content, the output is a font-decode failure.
_GARBLE_THRESHOLD = 0.05
_MIN_LEN = 500
# A short output that is overwhelmingly garble is still a decode failure, even
# below _MIN_LEN — a high ratio can't be incidental symbols in real prose.
_SHORT_GARBLE_RATIO = 0.5

_FORMULA_MARKER = "formula-not-decoded"
_GLYPH_LEAK = "glyph["
# The default pipeline leaves a formula-not-decoded marker for every equation it
# does not decode (expected when --enrich-formula is off). A stray undecoded
# formula is not worth a full VLM re-run; only escalate when math is pervasively
# dropped, i.e. the paper is genuinely math-heavy and the default is failing it.
_MIN_DROPPED_FORMULAS = 3


# Below this ASCII-letter density (letters / non-space chars) a document is not
# normal prose — a font-decode failure replaces words with glyphs and collapses
# letter density, whereas legitimate symbol-heavy notation still sits in mostly
# ASCII-letter text.
_MIN_LETTER_RATIO = 0.5


def _garble_ratio(markdown: str) -> float:
    chars = [c for c in markdown if not c.isspace()]
    if not chars:
        return 0.0
    hits = sum(
        any(lo <= ord(c) <= hi for lo, hi in _GARBLE_RANGES) for c in chars
    )
    return hits / len(chars)


def _ascii_letter_ratio(markdown: str) -> float:
    chars = [c for c in markdown if not c.isspace()]
    if not chars:
        return 0.0
    return sum(c.isascii() and c.isalpha() for c in chars) / len(chars)


def looks_garbled(markdown: str) -> bool:
    """True when the output is dominated by symbol/dingbat glyphs or leaked
    glyph names — the font-decoding failure mode."""
    # Leaked glyph names (e.g. "glyph[epsilon1]") are a strong, specific signal
    # — real Markdown does not repeat "glyph[" — so this is not length-gated.
    if markdown.count(_GLYPH_LEAK) >= 5:
        return True
    ratio = _garble_ratio(markdown)
    # A short output that is overwhelmingly garble is still a decode failure.
    if markdown.strip() and ratio >= _SHORT_GARBLE_RATIO:
        return True
    # Otherwise the symbol-ratio signal needs a length gate to avoid false
    # positives on short snippets that legitimately contain a few symbols.
    if len(markdown) < _MIN_LEN:
        return False
    # Require BOTH a high garble ratio and collapsed letter density, so
    # legitimate symbol-heavy notation (arrows, proof boxes, stars in math
    # prose) that clears the ratio does not trigger escalation on its own.
    return ratio > _GARBLE_THRESHOLD and _ascii_letter_ratio(markdown) < _MIN_LETTER_RATIO


def dropped_math(markdown: str) -> bool:
    """True when Docling left undecoded formula markers pervasively (>= the
    threshold), i.e. the document has substantial math the fast pipeline could
    not decode. A stray marker or two does not escalate.

    Note: the default pipeline emits these markers for every formula whenever
    --enrich-formula is off, so a genuinely math-heavy paper will escalate to
    the VLM backend by default. That is intentional — the benchmark showed the
    fast pipeline is poor at math and the VLM recovers it — and is disclosed via
    the escalation notice and README. Use --no-escalate or --enrich-formula to
    opt out of the VLM re-run for math papers.
    """
    return markdown.count(_FORMULA_MARKER) >= _MIN_DROPPED_FORMULAS


def needs_escalation(markdown: str) -> tuple[bool, str]:
    """Whether the default output warrants re-running with the VLM backend.

    Returns (should_escalate, human-readable reason).
    """
    if looks_garbled(markdown):
        return True, "output looks garbled (font-decoding failure)"
    if dropped_math(markdown):
        return True, "equations were not decoded"
    return False, ""
