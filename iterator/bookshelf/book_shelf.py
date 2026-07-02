"""BookShelf — a ConcreteAggregate holding books in insertion order.

Internally it happens to use a Python list, but nothing in its public
iteration contract reveals that. Swap the list for a linked structure,
a file, or a network call, and every client that iterates keeps working
— only :class:`~.book_shelf_iterator.BookShelfIterator` would change.
"""

from typing import List

from ..framework.aggregate import Aggregate
from ..framework.iterator import Iterator
from .book import Book


class BookShelf(Aggregate[Book]):
    """A shelf of :class:`~.book.Book` objects, iterable oldest-first."""

    def __init__(self) -> None:
        self._books: List[Book] = []

    def append_book(self, book: Book) -> None:
        """Put ``book`` at the end of the shelf."""
        self._books.append(book)

    def get_book_at(self, index: int) -> Book:
        """Return the book at ``index`` (used by the shelf's iterator)."""
        return self._books[index]

    def __len__(self) -> int:
        return len(self._books)

    def iterator(self) -> Iterator[Book]:
        """Create a fresh cursor over this shelf (GoF factory method)."""
        # Imported here to avoid a circular import at module load time.
        from .book_shelf_iterator import BookShelfIterator

        return BookShelfIterator(self)
