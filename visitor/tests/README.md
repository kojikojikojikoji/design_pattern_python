# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Visitor pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s visitor -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_accept_dispatches_on_the_element_type` | Double dispatch works: the same visitor is routed to `visit_file` or `visit_directory` by each element's own `accept` — no `isinstance` chains anywhere. |
| `test_size_visitor_totals_every_file_in_the_subtree` | A whole operation (recursive size measurement) lives in one visitor class, not scattered across element classes. |
| `test_list_visitor_renders_the_full_tree_with_paths` | Visitors own their traversal *and* its working state (the current path) — state the elements never carry. |
| `test_new_operation_requires_no_element_changes` | The pattern's payoff: a brand-new operation is added as a new class, with zero edits to `filesystem/`. |
| `test_visitors_work_on_any_subtree` | Every element accepts visitors, so operations can target a single file or any directory, not just the root. |
| `test_abstract_element_and_visitor_cannot_be_instantiated` | `Element` and `Visitor` are pure interfaces — the pattern's two hierarchies meet only through them. |
| `test_incomplete_visitor_cannot_be_instantiated` | A visitor that forgets an element type fails **at construction time** (`TypeError`), not mid-traversal — `abc` turns "handle every case" into a checked rule. |

## A note for learners

When you do the exercises (e.g. adding a `FindVisitor`), write the tests *first* by copying this file and adjusting the expectations. The key check: your new visitor's test must pass **without any diff** in `filesystem/`. If you had to touch an element class, the operation has leaked into the structure.
