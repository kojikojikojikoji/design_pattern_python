"""SideBorder — a ConcreteDecorator.

Adds one decoration character to the left and right of every row of
the wrapped display. Note that it never looks *inside* the wrapped
display — it only calls the public ``Display`` interface and adds its
own two characters around whatever comes back.
"""

from ..display.display import Display
from .border import Border


class SideBorder(Border):
    """Decorates a display with a character on both sides of each row."""

    def __init__(self, display: Display, border_char: str) -> None:
        if len(border_char) != 1:
            raise ValueError("border_char must be a single character")
        super().__init__(display)
        self._border_char = border_char

    def get_columns(self) -> int:
        # one border character on each side
        return 1 + self._display.get_columns() + 1

    def get_rows(self) -> int:
        # side decoration adds no rows
        return self._display.get_rows()

    def get_row_text(self, row: int) -> str:
        return f"{self._border_char}{self._display.get_row_text(row)}{self._border_char}"
