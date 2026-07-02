"""Tests for the Iterator example.

Run from the repository root:

    python -m unittest discover -s iterator -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from iterator.bookshelf.book import Book
from iterator.bookshelf.book_shelf import BookShelf
from iterator.framework.aggregate import Aggregate
from iterator.framework.iterator import Iterator


def make_shelf(*titles: str) -> BookShelf:
    shelf = BookShelf()
    for title in titles:
        shelf.append_book(Book(title))
    return shelf


class TestBookShelfIteration(unittest.TestCase):
    def setUp(self) -> None:
        self.shelf = make_shelf("A", "B", "C")

    def test_iterator_visits_every_element_in_order(self) -> None:
        """The traversal policy (oldest-first) lives in the iterator."""
        iterator = self.shelf.iterator()
        titles = []
        while iterator.has_next():
            titles.append(iterator.next().title)
        self.assertEqual(titles, ["A", "B", "C"])

    def test_has_next_is_false_once_exhausted(self) -> None:
        """The GoF protocol signals the end explicitly via has_next()."""
        iterator = self.shelf.iterator()
        for _ in range(3):
            iterator.next()
        self.assertFalse(iterator.has_next())

    def test_multiple_iterators_are_independent_cursors(self) -> None:
        """Position lives in the iterator, NOT in the aggregate."""
        first = self.shelf.iterator()
        second = self.shelf.iterator()
        first.next()
        first.next()
        # second is unaffected by first's progress.
        self.assertEqual(second.next().title, "A")

    def test_the_aggregate_works_directly_in_a_for_loop(self) -> None:
        """Aggregate.__iter__ makes every shelf a native Python iterable."""
        titles = [book.title for book in self.shelf]
        self.assertEqual(titles, ["A", "B", "C"])

    def test_the_gof_iterator_is_also_a_python_iterator(self) -> None:
        """has_next/next and __next__/StopIteration are the same idea."""
        iterator = self.shelf.iterator()
        self.assertEqual(next(iterator).title, "A")  # builtin next() works
        self.assertEqual(list(iterator), [self.shelf.get_book_at(1),
                                          self.shelf.get_book_at(2)])
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_iteration_does_not_expose_internal_storage(self) -> None:
        """Clients see books one by one, never the underlying list."""
        seen = [book for book in self.shelf]
        self.assertTrue(all(isinstance(book, Book) for book in seen))
        # A fresh iteration yields the same sequence — nothing was consumed
        # from the shelf itself.
        self.assertEqual([b.title for b in self.shelf], ["A", "B", "C"])

    def test_abstract_interfaces_cannot_be_instantiated(self) -> None:
        """Aggregate and Iterator are pure interfaces."""
        with self.assertRaises(TypeError):
            Aggregate()  # type: ignore[abstract]
        with self.assertRaises(TypeError):
            Iterator()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
