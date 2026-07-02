"""shipping — the abstract (pattern) side of the Strategy example."""

from .order import Order
from .quoter import ShippingQuoter
from .strategy import ShippingStrategy

__all__ = ["Order", "ShippingQuoter", "ShippingStrategy"]
