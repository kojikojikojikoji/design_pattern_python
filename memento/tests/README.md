# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Memento pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s memento -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_restore_returns_the_editor_to_the_saved_state` | A memento captures the originator's state *as a whole* — text and cursor come back together. |
| `test_editing_after_save_does_not_change_the_snapshot` | Snapshots are frozen copies, not live views; later edits cannot corrupt history. |
| `test_undo_restores_snapshots_in_lifo_order` | Originator + caretaker compose into a correct undo stack. |
| `test_memento_exposes_only_a_narrow_interface` | The public face of a snapshot is exactly one attribute: `label`. |
| `test_memento_repr_does_not_leak_state` | Opacity survives printing/logging — a common accidental leak in real code. |
| `test_memento_cannot_gain_new_attributes` | `__slots__` keeps snapshots inert value objects (Python's substitute for enforced privacy). |
| `test_caretaker_needs_only_the_narrow_interface` | `History` works with *any* object offering `.label` — proof it never peeks at editor internals. |
| `test_pop_on_empty_history_raises` | History policy (including "nothing to undo") belongs to the caretaker, not the editor. |

## A note for learners

The encapsulation tests are the interesting ones: they don't check *behaviour*, they check *what is impossible* (or at least loudly discouraged) — no public state, no leaking `repr`, no attribute injection. When you do the exercises, keep those three green; they are what separates a Memento from "a dict of the object's fields".
