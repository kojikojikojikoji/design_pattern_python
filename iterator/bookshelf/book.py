"""Book — the element type stored in the aggregate.

Deliberately boring: the pattern is about *visiting* elements, so the
elements themselves need no special powers.
"""


class Book:
    """A book identified by its title."""

    def __init__(self, title: str) -> None:
        self._title = title

    @property
    def title(self) -> str:
        return self._title

    def __repr__(self) -> str:
        return f"Book({self._title!r})"
