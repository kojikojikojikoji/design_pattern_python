# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Chain of Responsibility pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s chain_of_responsibility -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_first_capable_handler_wins` | When several handlers *could* resolve a request, chain position — not "fitness" — decides. |
| `test_request_travels_until_someone_accepts` | Declining handlers are transparent; the request flows past any number of them. |
| `test_unhandled_request_falls_off_the_end` | "Nobody handled it" is a clean, first-class outcome (`None`), not a crash. |
| `test_set_next_returns_its_argument_for_fluent_chaining` | `a.set_next(b).set_next(c)` builds the chain `a → b → c`, not a star around `a`. |
| `test_chain_order_determines_the_resolver` | Rewiring the chain changes behaviour with zero changes to any handler class. |
| `test_handlers_work_without_knowing_the_whole_chain` | Decoupling is per-link: a lone handler resolves or fails all by itself. |
| `test_no_support_resolves_nothing` | An always-declining handler is legal — pass-through stations compose safely. |
| `test_incomplete_support_cannot_be_instantiated` | Forgetting the `resolve()` hook fails **at construction time** (`TypeError`) — the value of `abc.abstractmethod`. |

## A note for learners

The tests use a small helper, `handle_quietly`, that redirects the demo's `print` output into a buffer — a reminder that `handle()` returns the *resolver* precisely so behaviour can be asserted without scraping stdout. When you do the exercises (e.g. adding an `EvenSupport`), copy this file and adjust the expectations: if your new handler passes the equivalents of the first three tests without you modifying `framework/`, you have implemented the pattern correctly.
