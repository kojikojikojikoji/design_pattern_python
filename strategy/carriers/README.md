# `carriers/` — the concrete side of the pattern

This package plays the role of an **application developer using the abstraction**. It plugs specific pricing algorithms into the machinery defined in [`../shipping/`](../shipping/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`flat_rate.py`](flat_rate.py) | **ConcreteStrategy** | One fixed price, no matter what. |
| [`weight_based.py`](weight_based.py) | **ConcreteStrategy** | Base fee + per-kilogram charge. |
| [`free_over_threshold.py`](free_over_threshold.py) | **ConcreteStrategy** | Promotional rule that *wraps* another strategy as its fallback. |

## What to notice

**Each algorithm is a whole class, and nothing but the algorithm.** No `if promotion_active:` branches scattered around, no flags — one pricing rule per file, each independently readable and testable:

```python
class FlatRateShipping(ShippingStrategy):
    def calculate(self, order: Order) -> int:
        return self._rate_cents
```

**Configuration lives in `__init__`, computation in `calculate`.** `WeightBasedShipping(base_cents=300, per_kg_cents=150)` builds a *configured* algorithm object. Two instances with different knobs are effectively two different strategies — no subclassing needed.

**Strategies can compose.** `FreeShippingOverThreshold(5000, fallback=WeightBasedShipping())` layers a promotion over any other rule. It works because every strategy — including the wrapper itself — honours the same one-method interface.

**This package depends on `shipping/`, never the reverse.** To add a new pricing rule (e.g. `DistanceBasedShipping`), you add a sibling module here. The context, the interface and the existing rules stay untouched.

## Try it

```bash
# from the repository root
python -m strategy.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to build a sibling of these very classes.
