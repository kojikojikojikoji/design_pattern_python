"""Demo client for the Flyweight pattern.

Run from the repository root:

    python -m flyweight.main

The point to notice: the demo renders 13 big characters but constructs
only 3 Glyph objects — and it *proves* it with counters, rather than
asking you to take sharing on faith.
"""

from .banner import Banner
from .glyphs.glyph import Glyph
from .glyphs.glyph_factory import GlyphFactory


def main() -> None:
    factory = GlyphFactory()

    text1 = "1212123"
    banner1 = Banner(text1, factory)
    print(f'Banner 1: "{text1}" ({len(text1)} characters)')
    banner1.show()
    print()

    text2 = "332211"
    banner2 = Banner(text2, factory)
    print(f'Banner 2: "{text2}" ({len(text2)} characters)')
    banner2.show()
    print()

    print("--- proof of sharing ---")
    total_chars = len(text1) + len(text2)
    print(f"Characters rendered across both banners: {total_chars}")
    print(f"Glyph objects created by the factory:    {factory.pool_size}")
    print(f"Glyph objects created in this process:   {Glyph.instances_created}")
    shared = banner1.glyphs[0] is banner2.glyphs[4]
    print(f"banner1's first '1' is banner2's last '1': {shared}")


if __name__ == "__main__":
    main()
