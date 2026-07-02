"""Iterator — the abstract cursor over an aggregate's elements.

This class carries the GoF interface (``has_next`` / ``next``) AND a
bridge to Python's native iterator protocol (``__iter__`` / ``__next__``).
The bridge is four lines, defined once, here — every concrete iterator
that implements the two GoF methods automatically works in a ``for``
loop, a comprehension, ``list(...)``, ``sum(...)`` and everywhere else
Python expects an iterable.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Iterator(ABC, Generic[T]):
    """A cursor that walks an aggregate one element at a time.

    Concrete iterators (e.g. ``BookShelfIterator``) implement:

    * :meth:`has_next` — is there another element?
    * :meth:`next` — return the current element and advance

    Each iterator owns its own position, so several iterations over the
    same aggregate can be in flight at once without interfering.
    """

    @abstractmethod
    def has_next(self) -> bool:
        """Return ``True`` while there are elements left to visit."""
        raise NotImplementedError

    @abstractmethod
    def next(self) -> T:
        """Return the next element and advance the cursor."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Bridge to Python's iterator protocol.
    # GoF's (has_next, next) pair and Python's __next__/StopIteration are
    # the same idea with different spellings; this adapter translates.
    # ------------------------------------------------------------------

    def __iter__(self) -> "Iterator[T]":
        return self

    def __next__(self) -> T:
        if not self.has_next():
            raise StopIteration
        return self.next()
