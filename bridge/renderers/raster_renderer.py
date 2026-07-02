"""ConcreteImplementor #2 — draws shapes as a grid of pixels."""

import math
from typing import final

from .renderer import Renderer


@final
class RasterRenderer(Renderer):
    """Renders geometry as pixels; reports how many pixels get coloured."""

    def render_circle(self, radius: float) -> str:
        pixels = round(math.pi * radius * radius)
        return f"[raster] circle(radius={radius:g}) drawn as {pixels} pixels"

    def render_square(self, side: float) -> str:
        pixels = round(side * side)
        return f"[raster] square(side={side:g}) drawn as {pixels} pixels"
