# `display/` — the Component side of the pattern

This package defines *what is being decorated*. It knows nothing about borders — you could delete [`../border/`](../border/) entirely and this package would still work (it just wouldn't be very decorated).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`display.py`](display.py) | **Component** | The interface shared by *everything* renderable: `get_columns()`, `get_rows()`, `get_row_text(row)`, `show()`. |
| [`string_display.py`](string_display.py) | **ConcreteComponent** | The plain object at the centre of the onion: one row of text, no decoration. |

## The one interface everyone shares

The whole Decorator pattern hangs on a single decision made here: **components and decorators implement the same interface**. A `SideBorder` answers `get_columns()` just like a `StringDisplay` does — it just answers with a bigger number. Because of that, client code (and other decorators!) cannot tell a bare component from a decorated one. That indistinguishability is called **transparency**, and it is what makes decorations stackable.

## Why `show()` is marked `@final`

```python
@final
def show(self) -> None:
    for row in range(self.get_rows()):
        print(self.get_row_text(row))
```

`show()` is a small **template method**: it defines rendering once, in terms of the three abstract methods. Subclasses (including every border) change *what the rows contain*, never *how the rectangle is printed*. That keeps the contract tight: any `Display` whose `get_rows`/`get_row_text` are consistent renders correctly, no matter how deep the decoration stack is.

## The rectangle invariant

Every implementation must keep one promise: *each row returned by `get_row_text` is exactly `get_columns()` characters wide*. Decorators rely on this when they pad or frame the wrapped display — the test `test_every_row_of_a_stack_matches_the_reported_width` in [`../tests/`](../tests/) checks the invariant survives an entire stack.
