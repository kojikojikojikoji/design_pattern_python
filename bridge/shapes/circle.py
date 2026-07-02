"""A concrete Abstraction: a circle, renderer-agnostic."""

from ..renderers.renderer import Renderer
from .shape import Shape


class Circle(Shape):
    """A circle defined by its radius.

    Note what is *absent*: any drawing code. ``draw`` merely forwards the
    geometry to whichever renderer was injected.
    """

    def __init__(self, renderer: Renderer, radius: float) -> None:
        super().__init__(renderer)
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    def draw(self) -> str:
        return self._renderer.render_circle(self._radius)
