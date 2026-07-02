# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Mediator pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s mediator -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_guest_mode_locks_credential_fields` | Widgets never decide their own interactivity — the mediator pushes it to them. |
| `test_password_unlocks_only_after_a_username_exists` | Cross-widget ordering rules live in exactly one method, not in widget event handlers. |
| `test_ok_unlocks_only_when_credentials_are_complete` | The mediator can express rules involving *three* widgets that none of those widgets knows about. |
| `test_any_change_re_derives_the_whole_dialog_state` | State is recomputed from facts each time, so removing a username correctly re-locks dependants — no stale state. |
| `test_widgets_hold_no_references_to_other_widgets` | The topology really is a star: a colleague's only cross-object reference is its mediator. |
| `test_a_colleague_reports_changes_to_its_mediator` | The entire colleague→mediator protocol is one call: `colleague_changed()` — verified with a recording stub. |
| `test_disabled_widgets_ignore_user_input` | Colleagues enforce the mediator's verdict locally (a greyed-out field swallows keystrokes). |
| `test_abstract_roles_cannot_be_instantiated` | `Mediator` is a pure interface — the coordination logic must be supplied by a concrete subclass. |

## A note for learners

The stub in `test_a_colleague_reports_changes_to_its_mediator` is worth copying: because colleagues depend only on the abstract `Mediator`, you can unit-test any widget in complete isolation by handing it a fake mediator. That testability is a fringe benefit of the star topology.
