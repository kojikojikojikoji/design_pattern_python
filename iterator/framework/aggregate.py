"""Aggregate — the abstract collection that can hand out iterators.

The single promise an aggregate makes: "ask me for an iterator and you
can visit my elements" — nothing about *how* those elements are stored.
That is the decoupling the pattern buys: clients iterate without knowing
whether the aggregate is a list, a tree, a file, or a database cursor.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .iterator import Iterator

T = TypeVar("T")


class Aggregate(ABC, Generic[T]):
    """A collection whose elements can be visited via an :class:`Iterator`.

    :meth:`iterator` is the GoF factory method for cursors; ``__iter__``
    simply delegates to it, so every ``Aggregate`` subclass is also a
    Python iterable for free.
    """

    @abstractmethod
    def iterator(self) -> Iterator[T]:
        """Create a fresh cursor positioned before the first element."""
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        # Python's for-loop calls __iter__; we answer with the same
        # object the GoF-style iterator() returns.
        return self.iterator()
