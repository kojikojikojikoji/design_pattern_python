"""IDCard — a concrete Product.

This is the "idcard" side of the example: it depends on the abstract
``framework`` package, but the framework never depends on it.
"""

from ..framework.product import Product


class IDCard(Product):
    """An ID card issued to a person, identified by a serial number.

    Note that the constructor is *not* meant to be called by client code.
    Cards are issued through ``IDCardFactory.create``, which also assigns
    the serial number and registers the card — one of the practical
    benefits of funnelling creation through a factory.
    """

    def __init__(self, owner: str, serial: int) -> None:
        print(f"Creating {owner}'s card (serial: {serial}).")
        self._owner = owner
        self._serial = serial

    def use(self) -> None:
        """Use the card — the behaviour required by the Product interface."""
        print(f"Using {self._owner}'s card (serial: {self._serial}).")

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def serial(self) -> int:
        return self._serial

    def __repr__(self) -> str:
        return f"IDCard(owner={self._owner!r}, serial={self._serial})"
