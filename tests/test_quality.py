"""Tests for the escalation heuristics."""

from paper_siphon.quality import (
    dropped_math,
    looks_garbled,
    needs_escalation,
)

CLEAN = (
    "## Attention Is All You Need\n\n"
    "The dominant sequence transduction models are based on complex recurrent "
    "or convolutional neural networks. We propose the Transformer, a model "
    "architecture relying entirely on attention mechanisms.\n\n"
    "| Layer | Complexity |\n|---|---|\n| Self-Attention | O(n^2) |\n"
) * 5

# The RoboCup TIGERs font-decode failure: dominated by dingbat/symbol glyphs.
GARBLED = (
    "## ❚■●❊❘/a115 ▼❛♥♥❤❡✐♠\n\n"
    "❊①/a116❡♥❞❡❞ ❚❡❛♠ ❉❡/a115❝/a114✐♣/a116✐♦♥ ❢♦/a114 ❘♦❜♦❈✉♣ ✷✵✷✵\n\n"
    "❆♥❞/a114❡ ❘②❧❧✱ ❙❛❜♦❧❝ ❏✉/a116 ❉❡♣❛/a114/a116♠❡♥/a116\n"
) * 20


def test_clean_output_does_not_escalate():
    assert looks_garbled(CLEAN) is False
    assert dropped_math(CLEAN) is False
    should, _ = needs_escalation(CLEAN)
    assert should is False


def test_garbled_output_escalates():
    assert looks_garbled(GARBLED) is True
    should, reason = needs_escalation(GARBLED)
    assert should is True
    assert "garbled" in reason


def test_pervasive_dropped_math_escalates():
    md = CLEAN + "\n\n" + "The loss is <!-- formula-not-decoded -->\n" * 3
    assert dropped_math(md) is True
    should, reason = needs_escalation(md)
    assert should is True
    assert "equation" in reason


def test_stray_dropped_math_does_not_escalate():
    # a couple of incidental undecoded formulas must not trigger a full VLM run
    md = CLEAN + "\n\n" + "inline <!-- formula-not-decoded -->\n" * 2
    assert dropped_math(md) is False
    assert needs_escalation(md)[0] is False


def test_leaked_glyph_names_escalate():
    md = "Some text " + ("the value glyph[epsilon1] appears here. " * 6)
    assert looks_garbled(md) is True


def test_short_output_never_garbled():
    # a couple of stray symbols in a tiny string must not false-positive
    assert looks_garbled("Fig. 3 ▼ shows the result") is False


def test_empty_output_is_safe():
    assert looks_garbled("") is False
    assert dropped_math("") is False
    assert needs_escalation("")[0] is False


def test_math_symbols_in_normal_text_do_not_escalate():
    # legitimate inline math / arrows should not trip the garble detector
    md = (
        "We minimize the loss $L = \\sum_i (y_i - \\hat{y}_i)^2$ where "
        "x → y denotes the mapping and α, β ∈ ℝ are parameters. "
    ) * 20
    assert looks_garbled(md) is False
    assert needs_escalation(md)[0] is False
