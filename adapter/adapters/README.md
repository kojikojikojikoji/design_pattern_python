# `adapters/` — where the two worlds meet

This package contains the only code in the whole example that imports from **both** [`../target/`](../target/) and [`../legacy/`](../legacy/). If the legacy service is ever replaced, this is the only package that changes.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`object_adapter.py`](object_adapter.py) | **Adapter** (object form) | Implements `Notifier`, *holds* a `LegacyEmailService`, forwards translated calls. |
| [`class_adapter.py`](class_adapter.py) | **Adapter** (class form) | Implements `Notifier` by *inheriting* from `LegacyEmailService` as well. |

## The translation, in one place

Both variants perform exactly the same three-part translation:

```python
delivered = ...send_mail(
    to_address=recipient,             # 1. rename the parameters
    message=body,
    headers={"X-Subject": subject},   # 2. repackage the subject
)
if not delivered:
    raise NotificationError(...)      # 3. status code -> exception
```

Before the adapter existed, this block would be copy-pasted at every call site — with the `X-Subject` key and the boolean check waiting to be forgotten. Now it exists once, is tested once, and every client gets it for free.

## Object adapter vs class adapter

| | `LegacyEmailAdapter` (composition) | `LegacyEmailClassAdapter` (inheritance) |
| --- | --- | --- |
| Relationship | HAS-A: `self._service` | IS-A: subclasses the adaptee |
| Can wrap any adaptee instance | ✅ injected at runtime | ❌ fixed at class definition |
| Hides the legacy API | ✅ `send_mail` not exposed | ❌ `send_mail` leaks through |
| Can override adaptee internals | ❌ | ✅ |

**Prefer the object adapter.** The class adapter is included because GoF describes both and the comparison is instructive — in Python, multiple inheritance makes it easy to write and just as easy to misuse. The leaking API is not hypothetical: exercise 3 in [`../README.md`](../README.md#10-exercises) has you exploit it.

## Why the adapters are `@final`

Both classes are marked `typing.final`. An adapter should be a *thin, closed* translation layer — if you need different behaviour, write another adapter (or wrap a differently-configured adaptee) rather than building inheritance trees on top of glue code.
