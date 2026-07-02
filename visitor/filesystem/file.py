"""File — a leaf ConcreteElement.

A file knows its name and size, and one more thing: which visitor method
corresponds to files. It knows nothing about what any visitor *does*.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .element import Element

if TYPE_CHECKING:
    from ..visitors.visitor import Visitor


class File(Element):
    """A leaf node with a name and a size in bytes."""

    def __init__(self, name: str, size: int) -> None:
        self._name = name
        self._size = size

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        """Size in bytes."""
        return self._size

    def accept(self, visitor: Visitor) -> None:
        """Second dispatch: 'I am a File, so call your File method.'"""
        visitor.visit_file(self)

    def __repr__(self) -> str:
        return f"File(name={self._name!r}, size={self._size})"
