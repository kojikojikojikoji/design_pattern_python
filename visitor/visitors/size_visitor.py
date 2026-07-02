"""SizeVisitor — a ConcreteVisitor that totals file sizes.

The pattern's payoff made visible: a second, completely different
operation over the same tree — and not one line of ``File`` or
``Directory`` had to change to support it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .visitor import Visitor

if TYPE_CHECKING:
    from ..filesystem.directory import Directory
    from ..filesystem.file import File


class SizeVisitor(Visitor):
    """Accumulates the total size, in bytes, of every file it visits."""

    def __init__(self) -> None:
        self._total = 0

    @property
    def total(self) -> int:
        """Total bytes accumulated so far."""
        return self._total

    def visit_file(self, file: File) -> None:
        self._total += file.size

    def visit_directory(self, directory: Directory) -> None:
        # Directories weigh nothing themselves; recurse into children.
        for child in directory:
            child.accept(self)
