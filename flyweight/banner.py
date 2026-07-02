"""Banner — the Client of the Flyweight pattern.

A banner renders a string as large ASCII art. It holds the **extrinsic
state**: which characters appear and in what order. The heavy shape
data (intrinsic state) stays in the shared :class:`Glyph` flyweights —
a banner never copies it, it only *refers* to it.

Render a 10,000-character banner and you still hold at most a handful
of Glyph objects; what grows is only the list of references.
"""

from .glyphs.glyph import GLYPH_HEIGHT, Glyph
from .glyphs.glyph_factory import GlyphFactory


class Banner:
    """A string rendered with big shared glyphs."""

    def __init__(self, text: str, factory: GlyphFactory) -> None:
        self._text = text
        # Extrinsic state: the SEQUENCE of glyph references. The same
        # Glyph object may appear here many times — that's the sharing.
        self._glyphs: list[Glyph] = [factory.get(char) for char in text]

    @property
    def text(self) -> str:
        return self._text

    @property
    def glyphs(self) -> tuple[Glyph, ...]:
        """The glyph references, in text order (read-only view)."""
        return tuple(self._glyphs)

    def render(self) -> str:
        """Return the banner as ``GLYPH_HEIGHT`` lines of ASCII art.

        The row index is passed INTO each shared glyph at use time —
        extrinsic state supplied by the client, exactly as GoF
        prescribes for flyweight operations.
        """
        lines = []
        for row in range(GLYPH_HEIGHT):
            line = " ".join(glyph.get_row(row) for glyph in self._glyphs)
            lines.append(line.rstrip())  # no invisible trailing spaces
        return "\n".join(lines)

    def show(self) -> None:
        """Print the rendered banner."""
        print(self.render())
