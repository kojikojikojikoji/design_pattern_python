"""Abstract Product — the interface every concrete product must implement.

In the Factory Method pattern, the *framework* side (this package) knows
nothing about concrete products such as ``IDCard``. It only knows that
"a product is something that can be used". That single assumption is
expressed by this abstract class.
"""

from abc import ABC, abstractmethod


class Product(ABC):
    """The common interface for all objects a :class:`Factory` can create.

    Concrete products (e.g. ``IDCard``) subclass ``Product`` and implement
    :meth:`use`. Client code can then work with any product through this
    interface without knowing its concrete class.
    """

    @abstractmethod
    def use(self) -> None:
        """Use the product. Each concrete product defines what this means."""
        raise NotImplementedError
