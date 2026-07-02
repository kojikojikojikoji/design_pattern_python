"""Abstract Product A — the ``Button`` interface.

In the Abstract Factory pattern, each *kind* of product in the family gets
one abstract interface. This module defines the first kind: buttons. The
abstract side (this package) knows nothing about light or dark themes —
it only knows that "a button has a label, belongs to a theme, and can be
rendered".
"""

from abc import ABC, abstractmethod


class Button(ABC):
    """The interface every themed button must implement.

    Concrete products (``LightButton``, ``DarkButton``) subclass ``Button``.
    Client code renders any button through this interface without knowing
    which theme produced it.
    """

    @property
    @abstractmethod
    def label(self) -> str:
        """The text shown on the button."""
        raise NotImplementedError

    @property
    @abstractmethod
    def theme(self) -> str:
        """Which product family this button belongs to (e.g. ``"light"``).

        Every product created by one factory reports the same theme —
        that consistency is the whole point of Abstract Factory.
        """
        raise NotImplementedError

    @abstractmethod
    def render(self) -> str:
        """Return this button's on-screen representation as text."""
        raise NotImplementedError
