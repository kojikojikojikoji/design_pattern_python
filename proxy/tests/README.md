# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Proxy pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

A word on method: laziness claims are *measured*, not assumed. `RealImage.loads` counts every expensive load, each test snapshots it in `setUp`, and assertions are made against the delta — so "the proxy didn't load anything" is a number, not a belief.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s proxy -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_proxy_implements_the_same_subject_interface` | A proxy is **substitutable** — code typed against `Image` accepts real subjects and proxies alike. |
| `test_creating_a_proxy_loads_nothing` | The virtual proxy's promise: construction is free; the expensive object does not yet exist. |
| `test_cheap_questions_are_answered_without_loading` | A good proxy answers what it can itself (`filename`) and only delegates what truly needs the real subject. |
| `test_first_render_loads_exactly_once_then_reuses` | Lazy *and* cached: the cost is paid on first use, and exactly once. |
| `test_proxy_renders_exactly_what_the_real_subject_renders` | Transparency: the proxy changes *when* work happens, never *what* the client receives. |
| `test_unauthorised_viewer_is_refused` | The protection flavour: a proxy can control *who* reaches the real subject. |
| `test_denied_access_never_touches_the_expensive_resource` | Proxies compose — protection wrapped around a virtual proxy means a denied request costs nothing at all. |
| `test_every_attempt_is_recorded_in_the_access_log` | The proxy is the natural interception point for cross-cutting concerns (auditing) — the real subject stays untouched. |

## A note for learners

When you do the exercises (e.g. adding a caching or remote-ish proxy), write the tests *first* by copying this file and adjusting the expectations. The load-counter technique transfers directly: any claim of the form "my proxy avoids/defers/deduplicates work" should be asserted as a counter delta, because a proxy that silently did the work eagerly would still pass every output-equality test.
