"""Abstract Visitor — one operation over the whole element hierarchy.

In GoF terms this is the **Visitor** participant: it declares one
``visit_*`` method per concrete element type. A subclass of this class is
a complete *operation* (list the tree, total the sizes, count the files…)
kept in one place instead of being smeared across the element classes.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # imported for type hints only — no runtime dependency
    from ..filesystem.directory import Directory
    from ..filesystem.file import File


class Visitor(ABC):
    """The interface every operation over the file-system tree implements.

    One abstract method per concrete element type. This is the pattern's
    contract: if a new element type were ever added, a new ``visit_*``
    method would appear here and every visitor would be forced (by
    ``abc``) to handle it — no case can be silently forgotten.
    """

    @abstractmethod
    def visit_file(self, file: File) -> None:
        """Handle a :class:`File` leaf."""
        raise NotImplementedError

    @abstractmethod
    def visit_directory(self, directory: Directory) -> None:
        """Handle a :class:`Directory` composite (including traversal)."""
        raise NotImplementedError
