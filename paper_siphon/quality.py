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
    (0x1D400, 0x1D7FF),  # mathematical alphanumeric symbols
)

# Above this fraction of non-space characters being "garble glyphs" on a
# document with real content, the output is a font-decode failure.
_GARBLE_THRESHOLD = 0.05
_MIN_LEN = 500

_FORMULA_MARKER = "formula-not-decoded"
_GLYPH_LEAK = "glyph["


def _garble_ratio(markdown: str) -> float:
    chars = [c for c in markdown if not c.isspace()]
    if not chars:
        return 0.0
    hits = sum(
        any(lo <= ord(c) <= hi for lo, hi in _GARBLE_RANGES) for c in chars
    )
    return hits / len(chars)


def looks_garbled(markdown: str) -> bool:
    """True when the output is dominated by symbol/dingbat glyphs or leaked
    glyph names — the font-decoding failure mode."""
    # Leaked glyph names (e.g. "glyph[epsilon1]") are a strong, specific signal
    # — real Markdown does not repeat "glyph[" — so this is not length-gated.
    if markdown.count(_GLYPH_LEAK) >= 5:
        return True
    # The symbol-ratio signal needs a length gate to avoid false positives on
    # short snippets that legitimately contain a few symbols.
    if len(markdown) < _MIN_LEN:
        return False
    return _garble_ratio(markdown) > _GARBLE_THRESHOLD


def dropped_math(markdown: str) -> bool:
    """True when Docling left undecoded formula markers."""
    return _FORMULA_MARKER in markdown


def needs_escalation(markdown: str) -> tuple[bool, str]:
    """Whether the default output warrants re-running with the VLM backend.

    Returns (should_escalate, human-readable reason).
    """
    if looks_garbled(markdown):
        return True, "output looks garbled (font-decoding failure)"
    if dropped_math(markdown):
        return True, "equations were not decoded"
    return False, ""
