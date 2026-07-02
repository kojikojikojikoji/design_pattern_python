"""Leaf — a node with no children.

A leaf implements the Component interface directly: its size is simply
its own size, and its tree rendering is a single line. It has **no**
``add`` method — in the "safe" Composite design chosen here, only
directories manage children (see ``entry.py`` for the trade-off).
"""

from typing import final

from .entry import Entry


@final
class File(Entry):
    """A file with a fixed size in bytes — the Leaf of the tree."""

    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self._size = size

    @property
    def size(self) -> int:
        """A leaf's size is its own size — no recursion needed."""
        return self._size
