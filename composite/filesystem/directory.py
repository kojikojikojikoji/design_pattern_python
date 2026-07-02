"""Composite — a node that contains other Entry nodes.

The Composite implements the same interface as the Leaf, but realises
each operation by **delegating to its children**: a directory's size is
the sum of its children's sizes, and its tree rendering is its own label
plus the (indented) rendering of every child.

Because children are typed as ``Entry`` — not ``File`` or ``Directory`` —
a directory can hold files and other directories without distinguishing
them. That single decision is what makes arbitrarily deep trees work
with no extra code.
"""

from typing import final

from .entry import Entry


@final
class Directory(Entry):
    """A directory that can contain files and other directories."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[Entry] = []

    @property
    def size(self) -> int:
        """Recursive aggregation: ask each child, whatever it is."""
        return sum(child.size for child in self._children)

    @property
    def children(self) -> tuple[Entry, ...]:
        """The direct children, in insertion order (read-only view)."""
        return tuple(self._children)

    def add(self, *entries: Entry) -> "Directory":
        """Add one or more entries; returns ``self`` so calls can chain.

        Raises ``ValueError`` if adding an entry would create a cycle
        (a directory placed inside itself or inside one of its own
        descendants) — a tree must stay a tree.
        """
        for entry in entries:
            if entry is self or (isinstance(entry, Directory) and entry._contains(self)):
                raise ValueError(
                    f"cannot add {entry.name!r} into {self.name!r}: it would create a cycle"
                )
            self._children.append(entry)
        return self

    def _contains(self, target: Entry) -> bool:
        """True if ``target`` is anywhere in this directory's subtree."""
        return any(
            child is target
            or (isinstance(child, Directory) and child._contains(target))
            for child in self._children
        )

    def _label(self) -> str:
        return f"{self.name}/ ({self.size})"

    def _tree_lines(self) -> list[str]:
        lines = [self._label()]
        for index, child in enumerate(self._children):
            last = index == len(self._children) - 1
            connector = "`-- " if last else "|-- "
            continuation = "    " if last else "|   "
            child_lines = child._tree_lines()
            lines.append(connector + child_lines[0])
            lines.extend(continuation + line for line in child_lines[1:])
        return lines
