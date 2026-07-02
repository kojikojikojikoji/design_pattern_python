"""Demo client for the Bridge pattern.

Run from the repository root:

    python -m bridge.main

The point to notice: 3 shapes x 3 renderers = 9 behaviours, produced by
only 3 + 3 concrete classes. With inheritance alone you would need nine
classes (VectorCircle, RasterCircle, ...), and a fourth renderer would
cost three more; here it costs exactly one.
"""

from .renderers.ascii_renderer import AsciiRenderer
from .renderers.raster_renderer import RasterRenderer
from .renderers.renderer import Renderer
from .renderers.vector_renderer import VectorRenderer
from .shapes.bordered_circle import BorderedCircle
from .shapes.circle import Circle
from .shapes.shape import Shape
from .shapes.square import Square


def main() -> None:
    renderers: list[Renderer] = [VectorRenderer(), RasterRenderer(), AsciiRenderer()]

    for renderer in renderers:
        print(f"--- {type(renderer).__name__} ---")
        # The SAME shape classes are reused with every renderer.
        shapes: list[Shape] = [
            Circle(renderer, 5),
            Square(renderer, 4),
            BorderedCircle(renderer, 3),
        ]
        for shape in shapes:
            print(shape.draw())
        print()

    print("9 combinations from 3 shape classes + 3 renderer classes (n + m, not n * m).")


if __name__ == "__main__":
    main()
