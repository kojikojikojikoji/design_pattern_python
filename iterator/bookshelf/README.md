# `bookshelf/` — the concrete side of the pattern

This package plays the role of an **application developer using the framework**. It plugs a specific collection — a shelf of books — into the abstract machinery defined in [`../framework/`](../framework/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`book.py`](book.py) | *(element)* | A book with a title. Deliberately boring — the pattern is about visiting, not about elements. |
| [`book_shelf.py`](book_shelf.py) | **ConcreteAggregate** | Stores books (in a private list) and mints cursors via `iterator()`. |
| [`book_shelf_iterator.py`](book_shelf_iterator.py) | **ConcreteIterator** | One traversal in progress: a shelf reference plus an integer position. |

## What to notice

**The cursor state lives in the iterator, not the shelf.**

```python
class BookShelfIterator(Iterator[Book]):
    def __init__(self, book_shelf: BookShelf) -> None:
        self._book_shelf = book_shelf
        self._index = 0        # <- the whole traversal state
```

Because each call to `shelf.iterator()` creates a fresh object with its own `_index`, any number of traversals can run over one shelf simultaneously, and iterating never "consumes" the shelf. Had `_index` lived inside `BookShelf`, one traversal at a time would be a permanent limitation.

**The shelf's storage stays private.** Clients reach books only through the cursor (or the `for` loop, which *is* the cursor). Swap the internal `list` for a linked structure, a file, or a network call, and every client keeps working — only `BookShelfIterator` would change. The iterator reads through the narrow `get_book_at(index)` / `__len__` API rather than touching `_books` directly, keeping that seam explicit.

**Two dialects, one implementation.** `BookShelfIterator` implements only the GoF pair `has_next()`/`next()` — yet it works in a `for` loop, because the abstract `Iterator` bridges to `__iter__`/`__next__` once, for everyone. Nothing in this package mentions `StopIteration` at all.

**The Pythonic replacement.** In production code this entire iterator class collapses into one generator line inside `BookShelf`:

```python
def __iter__(self):
    yield from self._books
```

Exercise 3 in [`../README.md`](../README.md#10-exercises) asks you to perform exactly that refactor and observe which guarantees survive (all of them — the language writes the cursor for you).

## Try it

```bash
# from the repository root
python -m iterator.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to add a second iterator class to this very package.
