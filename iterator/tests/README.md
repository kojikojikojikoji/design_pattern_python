# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Iterator pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s iterator -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_iterator_visits_every_element_in_order` | The traversal policy (oldest-first) lives in the iterator, and it covers the whole collection. |
| `test_has_next_is_false_once_exhausted` | The GoF protocol signals the end explicitly — no sentinel values, no exceptions needed. |
| `test_multiple_iterators_are_independent_cursors` | Position lives in the iterator, **not** the aggregate — concurrent traversals never interfere. |
| `test_the_aggregate_works_directly_in_a_for_loop` | `Aggregate.__iter__` makes every shelf a native Python iterable — the pattern and the language meet. |
| `test_the_gof_iterator_is_also_a_python_iterator` | `has_next`/`next` and `__next__`/`StopIteration` are the same contract; the bridge translates faithfully. |
| `test_iteration_does_not_expose_internal_storage` | Clients receive elements one by one and never the backing list; iterating consumes nothing. |
| `test_abstract_interfaces_cannot_be_instantiated` | `Aggregate` and `Iterator` are pure interfaces — you can't use the framework without extending it. |

## A note for learners

The independence test is the heart of the pattern: two cursors over one shelf, one races ahead, the other still returns the first book. If you ever move traversal state into the aggregate "for convenience", that test is the one that fails. When you do the exercises (e.g. the `ReverseBookShelfIterator` or the generator refactor), copy this file and adjust the expectations — a correct iterator implementation passes the equivalents of the first five tests without any change to `framework/`.
