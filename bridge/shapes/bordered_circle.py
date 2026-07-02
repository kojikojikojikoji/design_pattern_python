"""RefinedAbstraction — a richer shape built from the same primitives.

``BorderedCircle`` extends the abstraction hierarchy with new behaviour
(a square border drawn around the circle) **without touching any
renderer**. It composes the two primitive operations the Implementor
already offers. This is the pattern's payoff in action: the abstraction
axis grew, the implementor axis didn't notice.
"""

from .circle import Circle


class BorderedCircle(Circle):
    """A circle drawn inside a snugly fitting square border.

    The border is a square whose side equals the circle's diameter —
    expressed entirely through the existing ``render_square`` primitive,
    so every current and future renderer supports borders for free.
    """

    def draw(self) -> str:
        circle = super().draw()
        border = self._renderer.render_square(2 * self._radius)
        return f"{circle}, inside a border: {border}"
