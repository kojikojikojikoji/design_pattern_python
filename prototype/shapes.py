"""Concrete Prototypes — the shapes that actually get cloned.

``Circle`` and ``Rectangle`` are ordinary classes. They implement
``describe()`` and inherit ``clone()`` from :class:`~prototype.shape.Shape`
unchanged — a concrete prototype rarely needs custom cloning logic when
the base class clones deeply.
"""

from typing import Sequence

from .shape import Shape


class Circle(Shape):
    """A circle prototype, e.g. a badge or a status dot in a diagram tool."""

    def __init__(self, label: str, radius: int, tags: Sequence[str]) -> None:
        super().__init__(label, tags)
        self.radius = radius

    def describe(self) -> str:
        return (
            f"Circle '{self._label}' "
            f"(radius {self.radius}, tags: {', '.join(self.tags)})"
        )

    def __repr__(self) -> str:
        return f"Circle(label={self._label!r}, radius={self.radius}, tags={self.tags})"


class Rectangle(Shape):
    """A rectangle prototype, e.g. a banner or a text box in a diagram tool."""

    def __init__(
        self, label: str, width: int, height: int, tags: Sequence[str]
    ) -> None:
        super().__init__(label, tags)
        self.width = width
        self.height = height

    def describe(self) -> str:
        return (
            f"Rectangle '{self._label}' "
            f"({self.width}x{self.height}, tags: {', '.join(self.tags)})"
        )

    def __repr__(self) -> str:
        return (
            f"Rectangle(label={self._label!r}, width={self.width}, "
            f"height={self.height}, tags={self.tags})"
        )
