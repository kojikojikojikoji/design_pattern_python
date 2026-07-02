"""WeightBasedShipping — a ConcreteStrategy.

A base handling fee plus a per-kilogram charge. Compare it side by side
with :class:`~strategy.carriers.flat_rate.FlatRateShipping`: completely
different formula, identical interface — which is exactly what lets the
context swap between them without noticing.
"""

from ..shipping.order import Order
from ..shipping.strategy import ShippingStrategy


class WeightBasedShipping(ShippingStrategy):
    """Charges ``base + per_kg × weight``, rounded to whole cents."""

    def __init__(self, base_cents: int = 300, per_kg_cents: int = 150) -> None:
        self._base_cents = base_cents
        self._per_kg_cents = per_kg_cents

    def calculate(self, order: Order) -> int:
        """Heavier parcels cost more; the policy knobs live in __init__."""
        return self._base_cents + round(self._per_kg_cents * order.weight_kg)
