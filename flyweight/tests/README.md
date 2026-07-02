# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Flyweight pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s flyweight -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_same_character_yields_the_same_object` | The factory returns *the* glyph, not *a* glyph — verified with `is` (identity), the strongest possible claim. |
| `test_different_characters_yield_different_objects` | Sharing is keyed by intrinsic state; distinct characters rightly get distinct objects. |
| `test_object_count_grows_with_unique_chars_not_text_length` | The pattern's whole economy: 28 characters of text cost 3 objects. Object count scales with the *alphabet*, not the *document*. |
| `test_flyweights_are_shared_across_clients` | One pool serves every client — separate banners hold the very same instances. |
| `test_glyph_holds_only_intrinsic_state` | A flyweight stores nothing contextual: no position, no owner. Extrinsic state stays with the client. |
| `test_intrinsic_state_is_exposed_immutably` | Shared implies read-only: state comes back as an immutable tuple, so no holder can corrupt the others. |
| `test_unsupported_character_is_rejected_eagerly` | The pool stays clean — invalid requests fail fast instead of caching garbage. |
| `test_banner_renders_with_shared_glyphs` | Sharing is invisible in the output; rendering combines shared shapes with client-supplied extrinsic state (order, row). |

## A note for learners

When you do the exercises (e.g. adding characters to the font), write the tests *first* by copying this file and adjusting the expectations. The identity test (`assertIs`) and the object-count test are the two that actually verify *flyweight-ness* — a version of this code that quietly constructed a fresh `Glyph` per character would still render correctly and pass every other test.
