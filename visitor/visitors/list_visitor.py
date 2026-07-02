"""ListVisitor — a ConcreteVisitor that renders the tree as text.

One complete operation ("produce a listing") in one class. It carries its
own working state — the current path during traversal and the lines
collected so far — which is exactly the kind of state you could *not*
cleanly keep if this logic were scattered over ``File`` and ``Directory``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .visitor import Visitor

if TYPE_CHECKING:
    from ..filesystem.directory import Directory
    from ..filesystem.file import File


class ListVisitor(Visitor):
    """Builds an indented, full-path listing of a file-system tree."""

    def __init__(self) -> None:
        self._current_path = ""
        self._lines: list[str] = []

    def visit_file(self, file: File) -> None:
        self._lines.append(
            f"{self._current_path}/{file.name} ({file.size} bytes)"
        )

    def visit_directory(self, directory: Directory) -> None:
        path = f"{self._current_path}/{directory.name}"
        self._lines.append(f"{path} (dir)")

        # The visitor owns the traversal: descend depth-first, keeping
        # track of where we are, then restore the path on the way out.
        saved = self._current_path
        self._current_path = path
        for child in directory:
            child.accept(self)
        self._current_path = saved

    def report(self) -> str:
        """The finished listing, one element per line."""
        return "\n".join(self._lines)
