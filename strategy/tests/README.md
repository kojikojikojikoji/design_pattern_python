# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Strategy pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s strategy -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_context_delegates_to_its_strategy` | The context holds zero algorithm logic — the strategy's answer *is* the context's answer. |
| `test_strategy_can_be_swapped_at_runtime` | Changing the algorithm is one attribute assignment; no context code changes, no restart. |
| `test_all_strategies_are_interchangeable` | Every concrete strategy honours the same narrow contract (`Order` in, integer cents out), so the context can hold any of them. |
| `test_weight_based_charges_proportionally_to_weight` | One complete formula lives in one class — knobs in `__init__`, computation in `calculate`. |
| `test_strategies_compose_like_ordinary_objects` | Strategies are plain objects: a promotion can *wrap* any other strategy as its fallback. |
| `test_abstract_strategy_cannot_be_instantiated` | `ShippingStrategy` is a pure interface — you can't use it without implementing it. |
| `test_incomplete_strategy_cannot_be_instantiated` | Forgetting `calculate` fails **at construction time** (`TypeError`), not later at call time — the value of `abc.abstractmethod`. |

## A note for learners

When you do the exercises (e.g. adding a `DistanceBasedShipping`), write the tests *first* by copying this file and adjusting the expectations. If your new strategy passes the equivalents of the first three tests without you modifying `shipping/`, you have implemented the pattern correctly.
