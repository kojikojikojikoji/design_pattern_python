"""StockPrice — a concrete Subject.

A price feed for one stock symbol. It stores the latest price and, on
every change, notifies its observers — without knowing (or caring) how
many there are or what they do with the number. The prices are set from
a scripted sequence in the demo, so every run is deterministic.
"""

from ..framework.subject import Subject


class StockPrice(Subject):
    """The observable state: one symbol, one integer price.

    Note what is *absent* here: no mention of tickers, charts or alerts.
    The feed's entire duty to the outside world is "hold the state and
    announce changes" — everything reactive lives in the observers.
    """

    def __init__(self, symbol: str, price: int) -> None:
        super().__init__()
        self._symbol = symbol
        self._price = price

    @property
    def symbol(self) -> str:
        """The stock's ticker symbol (e.g. ``"ACME"``)."""
        return self._symbol

    @property
    def price(self) -> int:
        """The latest price — the state that observers pull in ``update``."""
        return self._price

    def set_price(self, price: int) -> None:
        """Record a new price and broadcast the change to all observers."""
        self._price = price
        self.notify_observers()
