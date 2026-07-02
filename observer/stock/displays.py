"""Concrete Observers — three unrelated reactions to the same price feed.

Each class implements ``update(subject)`` and pulls the state it needs
from the subject. They know nothing about each other, and the subject
knows nothing about them — you can attach any mix of them, at any time,
including while a notification is in flight (see ThresholdAlert).
"""

from ..framework.observer import Observer
from .stock_price import StockPrice


class TickerDisplay(Observer):
    """Shows every price as a plain number — the "digit display"."""

    def update(self, subject: StockPrice) -> None:
        print(f"[Ticker] {subject.symbol}: {subject.price}")


class BarChartDisplay(Observer):
    """Shows every price as a bar — same event, different presentation."""

    def update(self, subject: StockPrice) -> None:
        bar = "#" * (subject.price // 10)
        print(f"[Chart ] {bar} ({subject.price})")


class ThresholdAlert(Observer):
    """Fires once when the price crosses a threshold, then unsubscribes.

    The interesting line is ``subject.detach(self)``: an observer removing
    *itself* in the middle of a notification round. This is safe only
    because ``Subject.notify_observers`` iterates over a snapshot of the
    subscriber list — a guarantee the tests pin down.
    """

    def __init__(self, threshold: int) -> None:
        self._threshold = threshold

    def update(self, subject: StockPrice) -> None:
        if subject.price >= self._threshold:
            print(
                f"[Alert ] {subject.symbol} reached {subject.price} "
                f"(>= {self._threshold}) — notifying the trader, then unsubscribing."
            )
            subject.detach(self)
