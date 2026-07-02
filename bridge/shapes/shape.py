"""Abstraction — the interface for the "what is drawn?" axis.

In the Bridge pattern the *Abstraction* is the high-level interface
clients use. Crucially, it does **not** implement drawing itself: it holds
a reference to a :class:`~bridge.renderers.renderer.Renderer` (the
Implementor) and delegates the primitive work to it.

That single attribute — ``self._renderer`` — *is* the bridge. Shapes vary
along one axis (circle, square, bordered...), renderers along another
(vector, raster, ASCII...), and any shape can be paired with any renderer
at construction time.
"""

from abc import ABC, abstractmethod

from ..renderers.renderer import Renderer


class Shape(ABC):
    """Base of the shape hierarchy; delegates rendering to a ``Renderer``.

    Subclasses implement :meth:`draw` in terms of the renderer's primitive
    operations only. They never know (or care) which concrete renderer
    they are holding.
    """

    def __init__(self, renderer: Renderer) -> None:
        # HAS-A, not IS-A: the shape *uses* a renderer instead of
        # inheriting from one. This is what keeps the two hierarchies
        # independent (compare with a CircleVectorShape explosion).
        self._renderer = renderer

    @property
    def renderer(self) -> Renderer:
        """The rendering backend this shape delegates to."""
        return self._renderer

    @abstractmethod
    def draw(self) -> str:
        """Return this shape rendered by the attached renderer."""
        raise NotImplementedError
