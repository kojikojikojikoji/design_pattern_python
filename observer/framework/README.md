# `framework/` — the abstract side of the pattern

This package defines the publish/subscribe machinery of the Observer pattern without knowing anything about stocks, tickers or alerts. Any one-to-many "when X changes, tell everyone" relationship could be built on top of it.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`observer.py`](observer.py) | **Observer** | The subscriber interface: `update(subject)`. |
| [`subject.py`](subject.py) | **Subject** (Observable) | The subscription list plus `attach` / `detach` / `notify_observers`. |

## The one rule of this package

> The subject knows its observers **only through the abstract `Observer` interface**.

`Subject` stores `Observer` instances and calls exactly one method on them. It never checks concrete types, never imports from `stock/`. That is what allows an open-ended, changing set of subscribers: a ticker, a chart, an alert, and any class a user writes next year.

## Pull style vs. push style

This framework uses the **pull style**:

```python
observer.update(self)        # "something changed — come and look"
```

The observer receives the subject and pulls what it needs (`subject.price`). The alternative, **push style**, sends the data itself: `observer.update(symbol, old_price, new_price)`.

| | Pull (used here) | Push |
| --- | --- | --- |
| Coupling | Observer must know the subject's read API | Subject must guess what observers need |
| Flexibility | One observer can watch many subjects and read anything | Only the pushed data is available |
| Cost | Observers may re-read state they don't need | Data is computed/copied even if nobody needs it |

GoF's advice: pull is more reusable, push is more efficient when you know the audience. Real libraries pick per case — Django signals push keyword arguments; Qt signals push typed payloads; this example pulls.

## Why `notify_observers` iterates a snapshot

```python
for observer in list(self._observers):
    observer.update(self)
```

Observers commonly unsubscribe *from inside* `update` (one-shot alerts, closed windows). Mutating a list while iterating it skips elements silently in Python — a maddening heisenbug. Copying first makes self-removal mid-broadcast safe; the test `test_observer_may_detach_itself_during_notification` in [`../tests/`](../tests/) locks the guarantee in.

## Why `Subject` is a concrete class (not an ABC)

`Observer` is an ABC because subscribers must *supply* behaviour. `Subject` already has complete, reusable behaviour — subscription management — so it is a plain base class to inherit from, exactly how GoF sketches it. A subject subclass only adds its own state and decides *when* to call `notify_observers()`.
