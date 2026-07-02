"""BookShelfIterator — a ConcreteIterator: one cursor over one shelf.

All it stores is a reference to the shelf and an integer position. The
traversal logic (order, bounds) lives here, *outside* the aggregate —
which is exactly what lets a shelf support several simultaneous,
independent iterations.
"""

from ..framework.iterator import Iterator
from .book import Book
from .book_shelf import BookShelf


class BookShelfIterator(Iterator[Book]):
    """Walks a :class:`~.book_shelf.BookShelf` from oldest to newest book."""

    def __init__(self, book_shelf: BookShelf) -> None:
        self._book_shelf = book_shelf
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._book_shelf)

    def next(self) -> Book:
        book = self._book_shelf.get_book_at(self._index)
        self._index += 1
        return book
