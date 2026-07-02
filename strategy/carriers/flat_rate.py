"""FlatRateShipping — a ConcreteStrategy.

The simplest possible algorithm: every parcel costs the same. Useful as a
baseline and as proof that a strategy can be tiny — the pattern does not
require algorithms to be complicated, only *interchangeable*.
"""

from ..shipping.order import Order
from ..shipping.strategy import ShippingStrategy


class FlatRateShipping(ShippingStrategy):
    """Charges one fixed rate regardless of weight or subtotal."""

    def __init__(self, rate_cents: int = 599) -> None:
        self._rate_cents = rate_cents

    def calculate(self, order: Order) -> int:
        """The order's contents are irrelevant — flat means flat."""
        return self._rate_cents
