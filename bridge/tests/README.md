# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Bridge pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s bridge -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_same_shape_draws_differently_with_each_renderer` | The implementation axis varies freely while the abstraction stays fixed — one `Circle` class, three behaviours. |
| `test_one_renderer_instance_serves_every_shape` | The abstraction axis varies freely while the implementation stays fixed — one renderer, every shape. |
| `test_all_combinations_work_from_n_plus_m_classes` | The headline economics: 3 × 3 = 9 distinct behaviours from only 6 concrete classes. |
| `test_new_renderer_plugs_in_without_touching_any_shape` | Extending the implementor axis costs one new class and zero edits elsewhere — Open/Closed along the "how" axis. |
| `test_refined_abstraction_reuses_existing_primitives` | `BorderedCircle` adds behaviour composed purely from existing primitives — Open/Closed along the "what" axis. |
| `test_shape_delegates_via_composition_not_inheritance` | The bridge is a HAS-A reference: a shape is *never* a renderer. Composition is the load-bearing decision. |
| `test_both_hierarchy_roots_are_pure_interfaces` | `Shape` and `Renderer` are abstract — `abc.abstractmethod` makes incomplete extensions fail at construction time. |

## A note for learners

When you do the exercises (e.g. adding an `SvgRenderer` or a `Triangle`), write the tests *first* by copying this file and adjusting the expectations. The key assertion to preserve: your addition on one axis must pass its tests **without a single edit** on the other axis. If it can't, your bridge interface is drawn in the wrong place.
