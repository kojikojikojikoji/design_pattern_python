# `framework/` — the abstract side of the pattern

This package plays the role that a **library or framework author** would play in real life. It defines *what an aggregate is* and *what an iterator is*, without knowing anything about books — or any other concrete element type (both interfaces are `Generic[T]`).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`aggregate.py`](aggregate.py) | **Aggregate** | The single promise a collection makes: `iterator()` hands out a fresh cursor. |
| [`iterator.py`](iterator.py) | **Iterator** | The cursor protocol: `has_next()` / `next()` — plus the bridge to Python's native protocol. |

## The one rule of this package

> `framework/` must **never** import from `bookshelf/` (or any other concrete package).

The dependency arrow points one way only: concrete → abstract. New aggregates (see the exercises in [`../README.md`](../README.md#10-exercises)) are added as siblings of `bookshelf/` without ever editing this package — the Open/Closed Principle.

## The four-line bridge between two worlds

```python
def __iter__(self) -> "Iterator[T]":
    return self

def __next__(self) -> T:
    if not self.has_next():
        raise StopIteration
    return self.next()
```

This is the most instructive code in the package. GoF's protocol *asks before taking* (`has_next` → `next`); Python's protocol *takes until told to stop* (`__next__` → `StopIteration`). They encode the same contract — sequential access with a definite end — so a mechanical adapter translates one into the other. Because the adapter lives on the **abstract** class, every concrete iterator that implements the two GoF methods instantly works in `for` loops, comprehensions, `list(...)`, `sum(...)`, unpacking, and everywhere else Python consumes iterables.

`Aggregate.__iter__` completes the bridge on the collection side:

```python
def __iter__(self) -> Iterator[T]:
    return self.iterator()
```

`for book in shelf:` and `shelf.iterator()` are now literally the same call.

## Why `iterator()` is a factory method

`Aggregate.iterator()` creates an object (a cursor) whose concrete class the client never names — compare [`../../factory_method/`](../../factory_method/). Each call must return a **fresh** cursor positioned before the first element; that contract is what makes simultaneous independent traversals possible, and the test `test_multiple_iterators_are_independent_cursors` in [`../tests/`](../tests/) pins it down.

## Why `ABC` + `@abstractmethod`

Declaring `has_next`/`next`/`iterator` with `@abstractmethod` means a half-written cursor or collection **cannot even be instantiated** — Python raises `TypeError` at construction time instead of failing mid-loop. Fail fast, fail loudly. The test `test_abstract_interfaces_cannot_be_instantiated` demonstrates this.
