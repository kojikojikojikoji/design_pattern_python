# `framework/` — the abstract side of the pattern

This package plays the role that a **library or framework author** would play in real life. It defines *what a handler is* and *how a request travels a chain*, without knowing anything about limits, odd numbers, or any other concrete capability rule.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`ticket.py`](ticket.py) | **Request** | The immutable payload handlers inspect: a numbered support ticket. |
| [`support.py`](support.py) | **Handler** | The chain machinery: `set_next()` linking + the `handle()` walk (try → forward → fail). |

## The one rule of this package

> `framework/` must **never** import from `supports/` (or any other concrete package).

The dependency arrow points one way only: concrete → abstract. New handler types (see the exercises in [`../README.md`](../README.md#10-exercises)) are added as siblings in `supports/` without ever editing this package — the Open/Closed Principle.

## Why `handle()` is marked `@final`

```python
@final
def handle(self, ticket: Ticket) -> Optional["Support"]:
    if self.resolve(ticket):
        self.done(ticket)
        return self
    if self._next is not None:
        return self._next.handle(ticket)
    self.fail(ticket)
    return None
```

`handle()` encodes the pattern's invariant — *resolve it, or forward it, or (at the chain's end) admit failure*. If subclasses could override the walk, one badly written handler could swallow requests or skip the rest of the chain by accident. `@final` (checked by type checkers such as mypy/pyright) turns the convention into a rule. Subclasses customise exactly one thing: the `resolve()` predicate.

## Why `set_next()` returns its argument

```python
def set_next(self, next_support: "Support") -> "Support":
    self._next = next_support
    return next_support
```

Returning the **argument** (not `self`) makes the fluent one-liner build a *chain* rather than a *star*:

```python
alan.set_next(bob).set_next(charlie)   # alan -> bob -> charlie
```

Each call attaches to the handler returned by the previous call. The test `test_set_next_returns_its_argument_for_fluent_chaining` in [`../tests/`](../tests/) pins this down.

## Why `ABC` + `@abstractmethod`

Declaring `resolve()` with `@abstractmethod` means a handler without a capability rule **cannot even be instantiated** — Python raises `TypeError` at construction time instead of failing mysteriously mid-chain. Fail fast, fail loudly. The test `test_incomplete_support_cannot_be_instantiated` demonstrates this.
