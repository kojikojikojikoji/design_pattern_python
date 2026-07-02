"""StringDisplay — a ConcreteClass.

Renders a string five times inside a character frame sized to fit:

    +-------------+
    |Hello, world.|
    |Hello, world.|
    |Hello, world.|
    |Hello, world.|
    |Hello, world.|
    +-------------+

Same inherited skeleton as ``CharDisplay``, radically different output —
that contrast is the pattern's point.
"""

from ..framework.abstract_display import AbstractDisplay


class StringDisplay(AbstractDisplay):
    """Displays a string five times inside a ``+---+`` frame."""

    def __init__(self, string: str) -> None:
        self._string = string
        self._width = len(string)

    def open(self) -> None:
        """Top edge of the frame."""
        self._print_line()

    def print(self) -> None:
        """One framed body line (the template calls this five times)."""
        print(f"|{self._string}|")

    def close(self) -> None:
        """Bottom edge of the frame."""
        self._print_line()

    def _print_line(self) -> None:
        """Helper shared by open() and close(): ``+`` + dashes + ``+``."""
        print("+" + "-" * self._width + "+")
