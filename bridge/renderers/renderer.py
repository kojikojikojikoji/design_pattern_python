"""Implementor — the interface for the "how do I draw?" axis.

In the Bridge pattern the *Implementor* declares the primitive operations
the abstraction is built on. Note how small this interface is: shapes ask
for a rendered circle or square and get back a string. Everything else —
what a "shape" is, borders, composition of primitives — lives on the
abstraction side, in ``bridge/shapes/``.

Neither this module nor its concrete subclasses import anything from
``bridge/shapes/``. The two hierarchies meet only through the bridge:
the ``renderer`` attribute held by every ``Shape``.
"""

from abc import ABC, abstractmethod


class Renderer(ABC):
    """Primitive drawing operations every rendering backend must provide.

    Concrete renderers (vector, raster, ASCII, ...) decide what "drawing"
    means; shapes decide *which* primitives to call and with *what*
    geometry. Adding a new backend means one new subclass here — zero
    changes to any shape.
    """

    @abstractmethod
    def render_circle(self, radius: float) -> str:
        """Return a rendering of a circle with the given ``radius``."""
        raise NotImplementedError

    @abstractmethod
    def render_square(self, side: float) -> str:
        """Return a rendering of an axis-aligned square with side ``side``."""
        raise NotImplementedError
