"""Abstract Display — the Component of the Decorator pattern.

Every object in this example — the plain string in the middle *and*
every border wrapped around it — implements this one interface.
That shared interface is what makes decorators stackable: a border
can wrap anything that "is a Display", including another border.
"""

from abc import ABC, abstractmethod
from typing import final


class Display(ABC):
    """Something that can be rendered as a rectangle of text rows.

    Concrete components (e.g. ``StringDisplay``) and decorators
    (e.g. ``SideBorder``, ``FullBorder``) both subclass ``Display``,
    so client code cannot tell — and does not need to tell — whether
    it is holding a bare component or a whole stack of decorations.
    """

    @abstractmethod
    def get_columns(self) -> int:
        """Return the width of the display in characters."""
        raise NotImplementedError

    @abstractmethod
    def get_rows(self) -> int:
        """Return the height of the display in rows."""
        raise NotImplementedError

    @abstractmethod
    def get_row_text(self, row: int) -> str:
        """Return the text of row ``row`` (0-based).

        Every row must be exactly :meth:`get_columns` characters wide,
        and asking for a row outside ``0 <= row < get_rows()`` must
        raise :class:`IndexError`.
        """
        raise NotImplementedError

    @final
    def show(self) -> None:
        """Print every row.

        Marked ``@final``: rendering is defined once, in terms of the
        three abstract methods above. Subclasses change *what* the rows
        contain, never *how* the rectangle is printed.
        """
        for row in range(self.get_rows()):
            print(self.get_row_text(row))
