# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Decorator pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s decorator -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_decorated_object_is_still_a_display` | Decoration is **transparent** — a wrapped object still satisfies the Component interface, so clients never need to know. |
| `test_show_prints_exactly_the_rows_of_the_stack` | One rendering call (`show()`) works identically for bare and decorated objects. |
| `test_side_border_pads_both_sides_of_every_row` | A decorator delegates inward, then adds exactly its own contribution around the result. |
| `test_full_border_frames_the_component` | Different decorators add different responsibilities through the same mechanism. |
| `test_decorators_stack_to_any_depth` | Because decorators wrap the *abstract* type, they compose recursively — ten layers work as well as one. |
| `test_decoration_leaves_the_component_untouched` | Decoration is **composition, not mutation** — the wrapped object is never modified. |
| `test_every_row_of_a_stack_matches_the_reported_width` | Each layer preserves the rectangle invariant that the layer above relies on. |
| `test_border_is_abstract_and_cannot_be_instantiated` | `Border` only defines structure; forgetting to implement the geometry methods fails at construction time. |

## A note for learners

When you do the exercises (e.g. adding an `UpDownBorder`), write the tests *first* by copying this file and adjusting the expectations. If your new decorator passes the equivalents of the stacking and invariant tests without you modifying `display/`, you have implemented the pattern correctly.
