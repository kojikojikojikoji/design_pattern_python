# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the State pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s state -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_the_same_event_behaves_differently_per_state` | The pattern's core promise: identical input, mode-dependent output — achieved with zero conditionals. |
| `test_transitions_are_requested_by_the_states_themselves` | `DayState.on_clock` — not the context, not the client — decides that 17:00 means Night. |
| `test_no_transition_while_still_inside_business_hours` | A state knows its own exit condition, including when it is *not* met (no spurious transitions). |
| `test_clock_moves_the_system_between_day_and_night` | The full loop through the real context: Day → Night → Day across a simulated day. |
| `test_the_context_contains_no_mode_conditionals` | The if-else ladder is *really* gone: the context's source is checked for mode branching. |
| `test_states_are_singletons` | One instance per mode — identity comparisons are safe and transitions allocation-free. |
| `test_abstract_state_cannot_be_instantiated` | A new mode must answer **every** event; forgetting one fails at construction time, not at 3 a.m. when the alarm rings. |

## A note for learners

`RecordingContext` at the top of the test file is the pattern's testing payoff: because states depend only on the abstract `Context`, each mode's behaviour table can be verified in total isolation — no clock simulation, no printing, no real security system. When you add a `WeekendState` (exercise 3), specify it with a recording stub first.
