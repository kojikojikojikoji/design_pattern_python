"""Abstract Strategy — the interchangeable-algorithm interface.

In GoF terms this is the **Strategy** participant: one small interface
that every concrete algorithm implements. The context
(:class:`~strategy.shipping.quoter.ShippingQuoter`) talks to algorithms
*only* through this interface, which is what makes them swappable at
runtime.
"""

from abc import ABC, abstractmethod

from .order import Order


class ShippingStrategy(ABC):
    """The common interface for every shipping-cost algorithm.

    Concrete strategies (flat rate, weight based, promotional…) subclass
    this and implement :meth:`calculate`. Note how narrow the contract is:
    one method, plain data in, plain data out. Narrow interfaces are what
    keep strategies trivially interchangeable.
    """

    @abstractmethod
    def calculate(self, order: Order) -> int:
        """Return the shipping cost for ``order``, in cents."""
        raise NotImplementedError
