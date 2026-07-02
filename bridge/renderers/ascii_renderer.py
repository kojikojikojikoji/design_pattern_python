"""ConcreteImplementor #3 — draws shapes as terminal-friendly characters."""

from typing import final

from .renderer import Renderer


@final
class AsciiRenderer(Renderer):
    """Renders geometry as plain ASCII art tokens."""

    def render_circle(self, radius: float) -> str:
        return f"[ascii] circle(radius={radius:g}) drawn as ( )"

    def render_square(self, side: float) -> str:
        return f"[ascii] square(side={side:g}) drawn as [ ]"
