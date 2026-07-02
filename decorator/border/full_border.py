"""FullBorder — a ConcreteDecorator.

Draws a complete frame around the wrapped display: ``+---+`` lines on
top and bottom, ``|`` on the sides. Like every decorator it talks to
the wrapped object only through the abstract ``Display`` interface, so
it works equally well around a bare string or around a stack of other
borders.
"""

from ..display.display import Display
from .border import Border


class FullBorder(Border):
    """Decorates a display with a full rectangular frame."""

    def __init__(self, display: Display) -> None:
        super().__init__(display)

    def get_columns(self) -> int:
        # '|' on each side
        return 1 + self._display.get_columns() + 1

    def get_rows(self) -> int:
        # top and bottom frame lines
        return 1 + self._display.get_rows() + 1

    def get_row_text(self, row: int) -> str:
        if row == 0 or row == self.get_rows() - 1:
            return "+" + "-" * self._display.get_columns() + "+"
        if not 0 < row < self.get_rows() - 1:
            raise IndexError(f"row {row} out of range for {self.get_rows()} rows")
        return f"|{self._display.get_row_text(row - 1)}|"
