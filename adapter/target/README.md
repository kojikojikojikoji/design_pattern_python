# `target/` — the interface the application wants

This package plays the role of **your application's own abstractions**. It defines the notification interface all client code is written against, in the style your codebase prefers today: clear keyword parameters, a first-class `subject`, and failures **raised** as exceptions.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`notifier.py`](notifier.py) | **Target** | The interface clients expect: `notify(recipient, subject, body)`, raising `NotificationError` on failure. |

## The one rule of this package

> `target/` must **never** import from `legacy/` or `adapters/`.

The Target is defined purely by what the *application* needs, not by what any particular implementation happens to offer. If the modern interface were shaped to make the legacy service easy to wrap, the legacy design would quietly leak into every client — the exact disease the Adapter pattern is meant to cure.

## An interface is more than method names

Look closely at what the `notify` docstring promises:

```python
@abstractmethod
def notify(self, recipient: str, subject: str, body: str) -> None:
    """Raises NotificationError if delivery fails."""
```

The **error-reporting style is part of the contract**. The legacy service returns `False` on failure; the Target raises. An adapter that translated the parameters but forwarded the boolean would satisfy the type checker and still be wrong. The test `test_failure_status_code_becomes_an_exception` in [`../tests/`](../tests/) pins this down.

## Why an ABC and not just duck typing?

Python would happily accept any object with a `notify` method. Declaring `Notifier` as an `ABC` buys two things for a tutorial-sized price:

- adapters that forget to implement `notify` fail **at construction time** (`TypeError`), not at first use;
- `isinstance(x, Notifier)` gives tests and reviewers a precise way to say "this is a valid plug-in point".
