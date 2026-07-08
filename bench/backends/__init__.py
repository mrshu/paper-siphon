"""Backend adapter registry.

Each adapter converts a PDF to *raw* markdown. The orchestrator applies
paper-siphon's clean_markdown() uniformly afterwards, so adapters must NOT clean.

An adapter is any object with:
    name: str
    is_available() -> tuple[bool, str]   # (ok, reason-if-not)
    convert(pdf_path: Path) -> str        # raw markdown; may raise
"""

from __future__ import annotations

from .docling_baselines import DoclingStandard, GraniteDoclingMLX
from .subprocess_backends import (
    Chandra, GlmOcrMlx, LightOnOcrMlx, Marker, MinerU, OlmOcr2Mlx, PaddleOcrVl,
)

ALL = [
    DoclingStandard(),
    GraniteDoclingMLX(),
    Marker(),
    Chandra(),
    MinerU(),
    GlmOcrMlx(),
    OlmOcr2Mlx(),
    LightOnOcrMlx(),
    PaddleOcrVl(),
]

BY_NAME = {b.name: b for b in ALL}
