# `border/` — the Decorator side of the pattern

This package defines *the decorations*. Every class here both **is a** `Display` (it subclasses it) and **has a** `Display` (it wraps one) — that pair of relationships is the entire mechanism of the pattern.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`border.py`](border.py) | **Decorator** | Establishes the structure: subclass `Display`, hold a wrapped `Display`. |
| [`side_border.py`](side_border.py) | **ConcreteDecorator** | Adds one character to the left and right of every row. |
| [`full_border.py`](full_border.py) | **ConcreteDecorator** | Draws a complete `+---+` / `|` frame around the wrapped display. |

## Is-a *and* has-a, at the same time

```python
class Border(Display, ABC):
    def __init__(self, display: Display) -> None:
        self._display = display
```

- **is-a** (`Display` subclass) → a border can be used anywhere a plain display could. Clients don't know they're holding a decorated object.
- **has-a** (`self._display`) → the border delegates the real work inward and adds its own contribution around the result.

Because `self._display` is typed as the *abstract* `Display`, a border can wrap a `StringDisplay` — or another border. Stack as deep as you like; nobody in the stack knows or cares what's underneath them.

## Delegate, then contribute

Look at how little `SideBorder` does:

```python
def get_row_text(self, row: int) -> str:
    return f"{self._border_char}{self._display.get_row_text(row)}{self._border_char}"
```

It asks the wrapped display for its row, then adds exactly its own two characters. It never inspects what it wrapped, never special-cases "am I wrapping a FullBorder?". Each decorator owns **one thin layer of behaviour** — that is the pattern's answer to subclass explosion (see section 1 of [`../README.md`](../README.md)).

## Adding a new decoration

Write a sibling class: subclass `Border`, implement the three geometry methods, done. `UpDownBorder` (frame lines only above and below) is Exercise 1 in [`../README.md`](../README.md#10-exercises) — it requires **zero changes** to `display/` or to the other borders.
