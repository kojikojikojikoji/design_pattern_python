"""Directory — a composite ConcreteElement.

A directory holds child elements (files or other directories) and exposes
them through iteration. Deliberately, ``accept`` does **not** traverse the
children — it only announces "I am a Directory". Whether and how to walk
into children is each visitor's decision, which lets different operations
choose different traversals without the tree changing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from .element import Element

if TYPE_CHECKING:
    from ..visitors.visitor import Visitor


class Directory(Element):
    """A composite node: a named, ordered collection of child elements."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._children: list[Element] = []

    @property
    def name(self) -> str:
        return self._name

    def add(self, element: Element) -> Directory:
        """Add a child and return ``self`` so calls can be chained."""
        self._children.append(element)
        return self

    def __iter__(self) -> Iterator[Element]:
        """Yield children in insertion order (visitors traverse via this)."""
        return iter(self._children)

    def __len__(self) -> int:
        return len(self._children)

    def accept(self, visitor: Visitor) -> None:
        """Second dispatch: 'I am a Directory, so call your Directory
        method.' Traversal into children is the visitor's job."""
        visitor.visit_directory(self)

    def __repr__(self) -> str:
        return f"Directory(name={self._name!r}, children={len(self._children)})"
