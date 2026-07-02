"""A concrete Abstraction: a square, renderer-agnostic."""

from ..renderers.renderer import Renderer
from .shape import Shape


class Square(Shape):
    """An axis-aligned square defined by its side length."""

    def __init__(self, renderer: Renderer, side: float) -> None:
        super().__init__(renderer)
        self._side = side

    @property
    def side(self) -> float:
        return self._side

    def draw(self) -> str:
        return self._renderer.render_square(self._side)
