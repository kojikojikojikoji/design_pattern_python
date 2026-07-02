# `states/` — the State side of the pattern

This package holds the pattern's core idea: **each mode of the system is a class**, and everything that varies by mode — behaviour *and* transitions — lives inside those classes.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`state.py`](state.py) | **State** | The interface: one handler per event (`on_clock`, `on_use_safe`, `on_alarm`, `on_phone`). |
| [`day_state.py`](day_state.py) | **ConcreteState** | Business-hours behaviour; exits to `NightState` when the clock leaves 09–17. |
| [`night_state.py`](night_state.py) | **ConcreteState** | After-hours behaviour; the *same events* escalate; exits to `DayState` at opening time. |
| [`context.py`](context.py) | **Context** (interface) | The callbacks a state may invoke: `change_state`, `call_security`, `record_log`. |

## The one rule of this package

> Nothing in this package (or outside it) ever asks *"is it day or night?"* — **being** the right object replaces **asking**.

The daytime column of the behaviour table is `day_state.py`, the night column is `night_state.py`. To read what happens when the safe opens at night, you open one file and read one three-line method. To add a new mode (say, `WeekendState`), you add one file — and Python's `@abstractmethod` forces you to answer *every* event, so a mode can't silently forget one (see `test_abstract_state_cannot_be_instantiated`).

## Transitions live here, too

```python
# day_state.py
def on_clock(self, context: Context, hour: int) -> None:
    if not OPENING_HOUR <= hour < CLOSING_HOUR:
        from .night_state import NightState
        context.change_state(NightState())
```

Each state knows its own exit condition and names its successor. The context merely executes `change_state` when asked. Centralised alternatives (a transition table in the context) exist, but distributing transitions like this keeps each mode's *entire* story — behaviour plus departure — in one class.

The `import` inside the method is deliberate: `DayState` names `NightState` and vice versa, an inherent cycle of any two-state machine with distributed transitions. Deferring one import breaks the cycle at module-load time; the docstring at the import site says so, so nobody "fixes" it back into an `ImportError`.

## Why the states are singletons

Day/Night carry no per-context data — they are pure behaviour — so each class shares one instance via `__new__`:

```python
DayState() is DayState()   # True
```

Transitions allocate nothing, and identity checks (`system.state is DayState()`) are reliable everywhere. Hiroshi Yuki's original does the same with a Java singleton. If a state ever needs per-context fields (a retry counter, say), drop the singleton for that state and store the counter in the context instead — states shared across contexts must stay stateless.

## Why states depend on an abstract `Context`

The handlers receive a [`Context`](context.py) — an interface with three callbacks — rather than the concrete `SecuritySystem`. That keeps this package reusable (any host that can log, escalate and swap states qualifies) and makes states trivially testable with a recording stub, which is exactly what [`../tests/`](../tests/) does.
