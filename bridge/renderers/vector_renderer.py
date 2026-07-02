"""ConcreteImplementor #1 — draws shapes as resolution-independent curves."""

from typing import final

from .renderer import Renderer


@final
class VectorRenderer(Renderer):
    """Renders geometry as smooth, infinitely scalable curves."""

    def render_circle(self, radius: float) -> str:
        return f"[vector] circle(radius={radius:g}) drawn with smooth curves"

    def render_square(self, side: float) -> str:
        return f"[vector] square(side={side:g}) drawn with smooth curves"
