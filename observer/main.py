"""Demo client for the Observer pattern.

Run from the repository root:

    python -m observer.main

The price sequence is scripted (no randomness), so the output below is
reproducible. Watch the subscriber list change over time: a chart joins
mid-run, the alert removes ITSELF during a notification, and the ticker
is detached near the end.
"""

from .stock.displays import BarChartDisplay, ThresholdAlert, TickerDisplay
from .stock.stock_price import StockPrice


def main() -> None:
    feed = StockPrice("ACME", 100)
    ticker = TickerDisplay()
    chart = BarChartDisplay()
    alert = ThresholdAlert(110)

    print("== Subscribing the ticker and a one-shot alert (threshold 110) ==")
    feed.attach(ticker)
    feed.attach(alert)

    print()
    print("-- tick: 102 --")
    feed.set_price(102)

    print()
    print("== Subscribing the bar chart mid-run ==")
    feed.attach(chart)

    print()
    print("-- tick: 107 --")
    feed.set_price(107)

    print()
    print("-- tick: 112 (crosses the alert threshold) --")
    feed.set_price(112)

    print()
    print("-- tick: 96 (the alert is gone — it unsubscribed itself) --")
    feed.set_price(96)

    print()
    print("== Unsubscribing the ticker ==")
    feed.detach(ticker)

    print()
    print("-- tick: 105 --")
    feed.set_price(105)


if __name__ == "__main__":
    main()
