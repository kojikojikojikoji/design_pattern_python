# `framework/` — the abstract side of the pattern

This package defines *the algorithm* — its steps and their order — without defining what any step actually does. It knows nothing about characters or framed strings; those live in [`../displays/`](../displays/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`abstract_display.py`](abstract_display.py) | **AbstractClass** | Owns the template method `display()` = `open()` → `print()` ×5 → `close()`, and declares the three abstract primitive operations. |

## The Hollywood Principle

> "Don't call us, we'll call you."

Subclasses never call `open`/`print`/`close` themselves and never orchestrate anything — they *implement* the steps and wait for the inherited `display()` to call them at the right moments. The control flow lives at the top of the hierarchy; the details live at the bottom. This inversion is the essence of every framework you have ever used.

## Why `display()` is marked `@final`

```python
@final
def display(self) -> None:
    self.open()
    for _ in range(5):
        self.print()
    self.close()
```

`display()` encodes an invariant of the whole family — *every display opens, prints its body exactly five times, and closes, in that order*. If subclasses could override it, that invariant would become a suggestion. `@final` (checked by type checkers such as mypy/pyright) turns the convention into a rule: subclasses may change *what* each step does, never *whether or when* it happens.

## Why `ABC` + `@abstractmethod`

Declaring the three steps with `@abstractmethod` means an incomplete display **cannot even be instantiated** — Python raises `TypeError` at construction time instead of `AttributeError` halfway through `display()` at call time. Fail fast, fail loudly. The test `test_incomplete_display_cannot_be_instantiated` in [`../tests/`](../tests/) demonstrates this.

## The one rule of this package

> `framework/` must **never** import from `displays/` (or any other concrete package).

The dependency arrow points one way only: concrete → abstract. You can add ten new display types without editing this package — the Open/Closed Principle. (This is the same discipline as [`../../factory_method/framework/`](../../factory_method/framework/) — no coincidence: Factory Method's `create()` *is* a template method.)
