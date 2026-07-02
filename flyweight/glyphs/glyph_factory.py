"""GlyphFactory — the FlyweightFactory of the pattern.

The factory is the gatekeeper that makes sharing actually happen:
clients ask it for "the glyph for '1'", and it either hands back the
instance it already has or creates one, caches it, and hands that back.
As long as everyone goes through the factory, there can never be two
``Glyph`` objects for the same character.
"""


from .glyph import Glyph


class GlyphFactory:
    """Creates :class:`Glyph` instances — at most one per character."""

    def __init__(self) -> None:
        self._pool: dict[str, Glyph] = {}

    def get(self, char: str) -> Glyph:
        """Return THE glyph for ``char``, creating it only on first request.

        This get-or-create step is the heart of the Flyweight pattern.
        Note the pattern's implicit contract: shared objects must be
        treated as immutable, because a change made through one holder
        would be visible to every other holder of the same instance.
        """
        if char not in self._pool:
            self._pool[char] = Glyph(char)
        return self._pool[char]

    @property
    def pool_size(self) -> int:
        """How many distinct glyphs this factory has created so far."""
        return len(self._pool)
