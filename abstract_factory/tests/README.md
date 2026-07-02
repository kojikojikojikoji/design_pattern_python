# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Abstract Factory pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s abstract_factory -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_factories_return_abstract_products` | Clients can treat every widget as its abstract interface — concrete classes are an implementation detail. |
| `test_products_from_one_factory_form_a_consistent_family` | The pattern's central promise: a button and a checkbox from the same factory always match. |
| `test_different_factories_produce_different_families` | Swapping the factory swaps the *whole* family — the variation point is one object, not scattered conditionals. |
| `test_creation_parameters_reach_the_products` | Creation parameters pass through the factory to the concrete product intact. |
| `test_client_works_with_any_factory_unchanged` | One client function serves every family — the client contains zero theme logic. |
| `test_new_family_needs_no_changes_to_ui_or_client` | A brand-new family plugs in without editing `ui/` or `main.py` — Open/Closed for whole families. |
| `test_abstract_classes_cannot_be_instantiated` | `UIFactory`, `Button` and `Checkbox` are pure interfaces — you can't use the toolkit without extending it. |
| `test_incomplete_factory_cannot_be_instantiated` | A factory missing one product kind fails **at construction time** (`TypeError`), not when the missing widget is first requested — the value of `abc.abstractmethod`. |

## A note for learners

When you do the exercises (e.g. adding a `high_contrast/` family), write the tests *first* by copying this file and adjusting the expectations. If your new family passes the equivalents of the first five tests without you modifying `ui/` or `build_login_form`, you have implemented the pattern correctly.
