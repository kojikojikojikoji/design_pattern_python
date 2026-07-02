# `securitysystem/` — the Context side of the pattern

This package is what the rest of the application sees: a security panel with buttons and a clock. Its defining feature is what it *doesn't* contain.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`security_system.py`](security_system.py) | **ConcreteContext** | Holds the current `State`; forwards every event to it; implements the three callbacks states use (`change_state`, `call_security`, `record_log`). |

## What to notice

**Every event handler is a blind delegation.**

```python
def use_safe(self) -> None:
    self._state.on_use_safe(self)
```

No `if`, no `match`, no `isinstance`. The context does not know how many modes exist, which one is active beyond holding the reference, or what any of them do. Grep this file for `Day` — it appears exactly once, choosing the *initial* state in `__init__`. That single line is the only state decision the context ever makes; the test `test_the_context_contains_no_mode_conditionals` keeps it that way.

**`change_state` is a service, not a decision.**

```python
def change_state(self, state: State) -> None:
    print(f"[State] {self._state} -> {state}")
    self._state = state
```

States call this when *their* exit condition is met. The context's only contributions are the reassignment and the audit line — which is also the perfect single place for cross-cutting transition concerns (logging, metrics, notifying observers).

**The context is also the states' toolbox.** `call_security` and `record_log` implement the abstract [`Context`](../states/context.py) interface. States say *what* should happen ("escalate this"), the context decides *how* (here: print; in production: page someone). Swap this class for one that writes to syslog and neither state changes by a character.

## Try it

```bash
# from the repository root
python -m state.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the third one asks you to add a whole new mode and count how few files change.
