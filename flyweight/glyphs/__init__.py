"""glyphs — the shared (Flyweight) side of the Flyweight example."""

from .glyph import Glyph
from .glyph_factory import GlyphFactory

__all__ = ["Glyph", "GlyphFactory"]
