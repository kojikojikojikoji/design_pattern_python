# `shipping/` — the abstract side of the pattern

This package defines the pattern's fixed vocabulary: *what an order is*, *what a shipping algorithm looks like*, and *who delegates to it*. It knows nothing about flat rates, per-kilogram pricing, or promotions — those live in [`../carriers/`](../carriers/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`order.py`](order.py) | *(shared data)* | The immutable input every algorithm reads: weight + subtotal. |
| [`strategy.py`](strategy.py) | **Strategy** | The one-method interface every algorithm implements: `calculate(order) -> cents`. |
| [`quoter.py`](quoter.py) | **Context** | Holds the *current* strategy, delegates `quote()` to it, allows runtime swapping. |

## The one rule of this package

> `shipping/` must **never** import from `carriers/` (or any other concrete package).

The dependency arrow points one way only: concrete → abstract. You can add a tenth pricing rule without editing a single line here — the Open/Closed Principle.

## Why the context holds *zero* pricing logic

```python
def quote(self, order: Order) -> int:
    return self._strategy.calculate(order)
```

The naive alternative is an `if/elif` chain inside the context — every new pricing rule then means editing (and re-testing) the context. Here the context is *closed*: new rules arrive as new classes, and swapping them is one attribute assignment:

```python
quoter.strategy = WeightBasedShipping()   # runtime swap, context unchanged
```

## Why the Strategy interface is so narrow

`ShippingStrategy` has exactly one method, takes a plain immutable `Order`, and returns a plain `int`. The narrower the contract, the easier it is to write, test, and swap implementations — and the easier it becomes to replace a class with a **plain function** in Pythonic code (see section 8 of [`../README.md`](../README.md#8-when-to-use-it-and-when-not-to)).

## Why `ABC` + `@abstractmethod`

Declaring `calculate` with `@abstractmethod` means a half-written strategy **cannot even be instantiated** — Python raises `TypeError` at construction time instead of `AttributeError` in the middle of a checkout. The test `test_incomplete_strategy_cannot_be_instantiated` in [`../tests/`](../tests/) demonstrates this.
