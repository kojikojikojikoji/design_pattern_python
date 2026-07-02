# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Prototype pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s prototype -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_clone_is_a_new_object_not_the_prototype` | Cloning *creates* — it never hands back the original instance. |
| `test_clone_preserves_the_prototypes_configuration` | A clone starts as an exact copy of its prototype's state; nothing gets lost in the copy. |
| `test_mutating_a_clone_never_touches_the_prototype` | `clone()` is a **deep** copy — clones and prototypes share no mutable state. |
| `test_shallow_copy_shares_nested_state_the_pitfall` | The bug the pattern protects against: `copy.copy` shares the `tags` list, so "changing the copy" corrupts the original. |
| `test_create_returns_clones_through_the_abstract_interface` | Clients create by key and receive abstract `Shape`s — concrete classes stay out of client code. |
| `test_customising_a_created_object_never_corrupts_the_catalogue` | The registry hands out clones, so its stored samples remain pristine forever. |
| `test_a_tweaked_clone_can_be_registered_as_a_new_prototype` | New *kinds* of object can be minted at runtime — registration replaces subclassing. |
| `test_unknown_key_fails_fast_with_the_available_keys` | A typo raises `KeyError` immediately, and the message lists valid keys — errors should help you fix them. |

## A note for learners

When you do the exercises (e.g. adding a `Text` prototype), write the tests *first* by copying this file and adjusting the expectations. The third exercise in [`../README.md`](../README.md#10-exercises) deliberately sabotages `clone()` — predicting which of these tests fail (and where) is the best check that you understand deep vs shallow copying.
