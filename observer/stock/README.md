# `stock/` — the concrete side of the pattern

This package plugs a specific application — a stock-price feed with three kinds of subscribers — into the abstract machinery defined in [`../framework/`](../framework/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`stock_price.py`](stock_price.py) | **ConcreteSubject** | Holds one symbol + price; calls `notify_observers()` on every `set_price`. |
| [`displays.py`](displays.py) | **ConcreteObserver** (×3) | `TickerDisplay` (digits), `BarChartDisplay` (bars), `ThresholdAlert` (one-shot alarm). |

## What to notice

**The subject is reaction-free.** `StockPrice` contains no printing, no thresholds, no formatting — just state and an announcement. Every reaction lives in an observer, which is why adding a fourth reaction (a logger, a Slack notifier) touches zero existing code.

**Same event, independent reactions.** `TickerDisplay` and `BarChartDisplay` render the *same* notification completely differently, and neither knows the other exists. This is the pattern's fan-out: one `set_price`, N presentations.

**`ThresholdAlert` unsubscribes itself mid-notification.**

```python
def update(self, subject: StockPrice) -> None:
    if subject.price >= self._threshold:
        print(...)
        subject.detach(self)     # goodbye — from INSIDE the broadcast
```

A one-shot subscriber is a standard real-world need (fire an alarm once, then stop). It works here only because `Subject.notify_observers` iterates a snapshot of the subscriber list — see [`../framework/README.md`](../framework/README.md) for why that matters.

**Concrete observers may know the concrete subject.** `update` is annotated with `StockPrice`, not `Subject`, because pull-style observers need the subject's read API (`symbol`, `price`). The decoupling the pattern promises is one-directional: the *subject* must not know concrete observers; observers knowing their subject's interface is normal and fine.

## Try it

```bash
# from the repository root
python -m observer.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to write a new observer without touching this package's subject.
