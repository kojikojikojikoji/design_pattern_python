"""StringDisplay — the ConcreteComponent of the Decorator pattern.

This is the plain object "in the middle of the onion": a single row of
text with no decoration at all. Decorators from ``decorator.border``
wrap around instances of this class (or around each other).
"""

from .display import Display


class StringDisplay(Display):
    """A one-row display showing a fixed string."""

    def __init__(self, string: str) -> None:
        self._string = string

    def get_columns(self) -> int:
        return len(self._string)

    def get_rows(self) -> int:
        return 1

    def get_row_text(self, row: int) -> str:
        if row != 0:
            raise IndexError(f"StringDisplay has exactly 1 row, not row {row}")
        return self._string
