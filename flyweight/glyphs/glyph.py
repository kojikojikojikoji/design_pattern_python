"""Glyph — the Flyweight of the pattern.

A ``Glyph`` holds the big ASCII-art shape of ONE character. That shape
is **intrinsic state**: it depends only on which character the glyph
represents, never on where or how often the character appears in a
banner. Because intrinsic state is context-free and immutable, one
``Glyph('1')`` can safely be shared by every '1' in every banner in
the whole program.

What a glyph deliberately does NOT store is **extrinsic state**: its
position in a banner, which banner it belongs to, how many times it is
used. That information varies per occurrence and therefore lives in the
client (:class:`flyweight.banner.Banner`), which passes it in — here as
the row index argument to :meth:`Glyph.get_row`.

The class also counts how many instances have ever been constructed
(:attr:`Glyph.instances_created`) so the demo and the tests can *prove*
sharing happens instead of just asserting it.
"""

from typing import ClassVar

# The "font": 5-row ASCII art for each supported character.
# In Hiroshi Yuki's book these shapes are loaded from big?.txt files;
# inlining them keeps this tutorial dependency- and I/O-free.
_FONT: dict[str, tuple[str, ...]] = {
    "1": (
        "  #  ",
        " ##  ",
        "  #  ",
        "  #  ",
        " ### ",
    ),
    "2": (
        " ### ",
        "#   #",
        "   # ",
        "  #  ",
        "#####",
    ),
    "3": (
        "#### ",
        "    #",
        " ### ",
        "    #",
        "#### ",
    ),
    "-": (
        "     ",
        "     ",
        " ### ",
        "     ",
        "     ",
    ),
}

#: Number of text rows every glyph is tall.
GLYPH_HEIGHT = 5


class Glyph:
    """The ASCII-art shape of one character — heavy, immutable, shareable.

    Client code should not call this constructor directly; ask
    :class:`~flyweight.glyphs.glyph_factory.GlyphFactory` instead, which
    guarantees at most one instance per character. (Pretend each glyph
    is expensive — a loaded texture, a parsed font file, megabytes of
    pixel data. Sharing is what keeps 10,000 characters affordable.)
    """

    #: How many Glyph objects have EVER been constructed — the evidence
    #: that the factory shares instances instead of re-creating them.
    instances_created: ClassVar[int] = 0

    def __init__(self, char: str) -> None:
        if char not in _FONT:
            raise ValueError(
                f"no glyph for character {char!r}; supported: {sorted(_FONT)}"
            )
        self._char = char
        self._rows = _FONT[char]  # intrinsic state: the shape itself
        Glyph.instances_created += 1

    @property
    def char(self) -> str:
        """The character this glyph draws."""
        return self._char

    @property
    def rows(self) -> tuple[str, ...]:
        """The glyph's shape, one string per row (immutable tuple)."""
        return self._rows

    def get_row(self, row: int) -> str:
        """Return row ``row`` of the shape.

        ``row`` is *extrinsic* — it is supplied by the caller at use
        time, not stored in the glyph. The same shared glyph can be
        rendering row 0 for one banner and row 4 for another.
        """
        return self._rows[row]

    def __repr__(self) -> str:
        return f"Glyph({self._char!r})"
