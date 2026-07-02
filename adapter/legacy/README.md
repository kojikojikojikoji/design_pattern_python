# `legacy/` — the adaptee you must not touch

This package plays the role of **third-party or frozen legacy code**. Imagine it lives in `site-packages/` or in a 15-year-old module with no tests: it works, other systems depend on it, and editing it is off the table.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`legacy_email_service.py`](legacy_email_service.py) | **Adaptee** | Actually delivers mail — through an API that predates your conventions. |

## The three deliberate incompatibilities

Each mismatch below is typical of real legacy APIs, and each is something the adapter must translate:

| Legacy API | Modern `Notifier` expectation | Adapter's job |
| --- | --- | --- |
| method is `send_mail(to_address, message, headers)` | method is `notify(recipient, subject, body)` | rename and reorder parameters |
| subject travels as `headers["X-Subject"]` | `subject` is a first-class parameter | build the headers dict |
| returns `False` on failure | raises `NotificationError` | check the bool, raise |

## The one rule of this package

> Nothing in `legacy/` imports from `target/` or `adapters/` — and nothing in this package is ever edited to "help" the adaptation.

That is the whole premise of the Adapter pattern: **reuse without modification**. The test `test_the_adaptee_is_never_modified` in [`../tests/`](../tests/) asserts that no `notify` method has been monkey-patched onto the legacy class.

## Why the demo prints `[legacy]` lines

The `print` calls tagged `[legacy]` make the demo output show *who is really doing the work*. Run `python -m adapter.main` from the repository root and note that both adapter variants produce identical `[legacy]` lines — the old code is untouched and fully in charge of delivery; only the interface around it changed.
