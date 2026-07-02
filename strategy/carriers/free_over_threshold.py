"""FreeShippingOverThreshold — a ConcreteStrategy that composes another.

A promotional rule: orders at or above a subtotal threshold ship free;
everything else falls back to a *wrapped* strategy. This shows that
strategies are ordinary objects — they can be configured, combined and
layered like any other object, because they all share one tiny interface.
"""

from ..shipping.order import Order
from ..shipping.strategy import ShippingStrategy


class FreeShippingOverThreshold(ShippingStrategy):
    """Ships free above a subtotal threshold, otherwise delegates.

    The fallback is *any* other :class:`ShippingStrategy` — this class
    neither knows nor cares which one. Strategies composing strategies is
    a small taste of the Decorator pattern.
    """

    def __init__(self, threshold_cents: int, fallback: ShippingStrategy) -> None:
        self._threshold_cents = threshold_cents
        self._fallback = fallback

    def calculate(self, order: Order) -> int:
        """Free if the order qualifies; the fallback's price otherwise."""
        if order.subtotal_cents >= self._threshold_cents:
            return 0
        return self._fallback.calculate(order)
