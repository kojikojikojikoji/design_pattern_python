"""ShippingQuoter — the Context that delegates to a Strategy.

In GoF terms this is the **Context** participant. It holds a reference to
the *current* :class:`~strategy.shipping.strategy.ShippingStrategy` and
forwards the actual work to it. The context contains **no pricing logic
whatsoever** — that is the whole point: adding or changing a pricing rule
never touches this class.
"""

from .order import Order
from .strategy import ShippingStrategy


class ShippingQuoter:
    """Quotes shipping costs by delegating to a swappable strategy.

    The strategy can be replaced at runtime through the :attr:`strategy`
    property — for example when the user picks a different delivery option
    in a checkout UI, or when a promotion begins at midnight.
    """

    def __init__(self, strategy: ShippingStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> ShippingStrategy:
        """The algorithm currently in use."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ShippingStrategy) -> None:
        """Swap the algorithm at runtime. The context never needs to know
        (or care) which concrete class it received."""
        self._strategy = strategy

    def quote(self, order: Order) -> int:
        """Return the shipping cost for ``order`` in cents.

        Pure delegation — the context decides *when* to calculate,
        the strategy decides *how*.
        """
        return self._strategy.calculate(order)
