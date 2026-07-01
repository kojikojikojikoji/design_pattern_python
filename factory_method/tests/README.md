# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Factory Method pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s factory_method -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_create_returns_a_product` | Clients can treat every result as an abstract `Product` — concrete type is an implementation detail. |
| `test_created_card_belongs_to_owner` | The creation parameter reaches the concrete product intact. |
| `test_every_created_card_is_registered` | The template method makes "create ⇒ register" an invariant, not a convention. |
| `test_serial_numbers_are_unique_and_sequential` | Centralising creation lets the factory own cross-cutting policy (ID assignment). |
| `test_abstract_classes_cannot_be_instantiated` | `Factory` and `Product` are pure interfaces — you can't use the framework without extending it. |
| `test_incomplete_factory_cannot_be_instantiated` | Forgetting a hook fails **at construction time** (`TypeError`), not later at call time — the value of `abc.abstractmethod`. |

## A note for learners

When you do the exercises (e.g. adding a `TVCardFactory`), write the tests *first* by copying this file and adjusting the expectations. If your new factory passes the equivalents of the first three tests without you modifying `framework/`, you have implemented the pattern correctly.
