# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Adapter pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s adapter -t .
```

(The legacy service prints to stdout; the tests capture it with `contextlib.redirect_stdout`, so a passing run stays quiet.)

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_object_adapter_is_a_notifier` | The adapter satisfies the Target interface — clients can depend on `Notifier` alone. |
| `test_object_adapter_does_not_expose_the_adaptee_api` | Composition *hides* the legacy API; clients can't accidentally bypass the translation. |
| `test_call_is_translated_to_the_legacy_signature` | `notify(recipient, subject, body)` arrives at the adaptee as `send_mail(to, msg, headers)` with the subject in `X-Subject` — the mechanical heart of the pattern. |
| `test_failure_status_code_becomes_an_exception` | The adapter translates *error conventions*, not just parameter names — `False` becomes `NotificationError`. |
| `test_class_adapter_is_both_target_and_adaptee` | The class adapter variant IS-A `Notifier` *and* IS-A `LegacyEmailService` — the defining property (and liability) of multiple inheritance. |
| `test_class_adapter_translates_the_call_too` | Both variants perform an identical translation; they differ only in wiring. |
| `test_client_code_works_with_any_notifier` | Code written against the Target runs unchanged with either adapter — the payoff. |
| `test_the_adaptee_is_never_modified` | Adaptation wraps; it never edits or monkey-patches the legacy class. |
| `test_target_interface_cannot_be_instantiated` | `Notifier` is a pure interface — `abc.abstractmethod` fails fast at construction time. |

## A note for learners

When you do the exercises (e.g. adding an `SmsAdapter`), write the tests *first* by copying this file and adjusting the expectations. If your new adapter passes the equivalents of the first four tests without you editing `legacy/`, you have implemented the pattern correctly.
