"""Tests for the Flyweight example.

Run from the repository root:

    python -m unittest discover -s flyweight -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from flyweight.banner import Banner
from flyweight.glyphs.glyph import Glyph
from flyweight.glyphs.glyph_factory import GlyphFactory


class TestSharing(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = GlyphFactory()

    def test_same_character_yields_the_same_object(self) -> None:
        """The factory returns THE glyph for a character, not A glyph —
        identity (is), not mere equality."""
        self.assertIs(self.factory.get("1"), self.factory.get("1"))

    def test_different_characters_yield_different_objects(self) -> None:
        """Sharing happens per intrinsic state, not globally."""
        self.assertIsNot(self.factory.get("1"), self.factory.get("2"))

    def test_object_count_grows_with_unique_chars_not_text_length(self) -> None:
        """The flyweight economy: 28 characters of text, 3 objects."""
        before = Glyph.instances_created
        Banner("1212123321212312312321313212", self.factory)
        self.assertEqual(Glyph.instances_created - before, 3)
        self.assertEqual(self.factory.pool_size, 3)

    def test_flyweights_are_shared_across_clients(self) -> None:
        """Different banners built via the same factory hold the very
        same glyph instances."""
        banner_a = Banner("123", self.factory)
        banner_b = Banner("321", self.factory)
        self.assertIs(banner_a.glyphs[0], banner_b.glyphs[2])


class TestIntrinsicVsExtrinsic(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = GlyphFactory()

    def test_glyph_holds_only_intrinsic_state(self) -> None:
        """A glyph knows its shape, never its position or its banner —
        that context is extrinsic and lives in the client."""
        glyph = self.factory.get("1")
        self.assertEqual(set(vars(glyph)), {"_char", "_rows"})

    def test_intrinsic_state_is_exposed_immutably(self) -> None:
        """Shared objects must be safe to share: the shape comes back
        as an immutable tuple, identical on every call."""
        glyph = self.factory.get("2")
        self.assertIsInstance(glyph.rows, tuple)
        self.assertIs(glyph.rows, glyph.rows)

    def test_unsupported_character_is_rejected_eagerly(self) -> None:
        """The factory can't cache garbage: unknown characters fail
        fast with a helpful error instead of polluting the pool."""
        with self.assertRaises(ValueError):
            self.factory.get("X")
        self.assertEqual(self.factory.pool_size, 0)

    def test_banner_renders_with_shared_glyphs(self) -> None:
        """Sharing is invisible in the output — rendering works purely
        on references plus extrinsic state (order, row index)."""
        banner = Banner("1-1", self.factory)
        self.assertEqual(
            banner.render(),
            "  #           #\n"
            " ##          ##\n"
            "  #    ###    #\n"
            "  #           #\n"
            " ###         ###",
        )


if __name__ == "__main__":
    unittest.main()
