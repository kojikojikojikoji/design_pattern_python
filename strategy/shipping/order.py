"""Order — the data every strategy works on.

The Strategy pattern needs a stable "vocabulary" shared by the context and
all strategies. Here it is a tiny immutable value object: strategies read
an :class:`Order`, never modify it, and never see anything else. Money is
stored in integer cents so results are exact and deterministic.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    """A customer order, as far as shipping cost calculation is concerned.

    ``frozen=True`` makes orders immutable — a strategy is a pure
    calculation, so nothing should be able to mutate its input.
    """

    weight_kg: float
    """Total parcel weight in kilograms."""

    subtotal_cents: int
    """Merchandise subtotal in cents (e.g. 8000 = $80.00)."""
