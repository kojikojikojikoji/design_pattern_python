"""IDCardFactory — a concrete Creator.

It fills in the two hooks left abstract by ``framework.factory.Factory``:
what to instantiate (:class:`IDCard`) and how to record it (an in-memory
registry). The inherited ``create`` method ties the two steps together.
"""

from ..framework.factory import Factory
from .id_card import IDCard


class IDCardFactory(Factory):
    """Issues :class:`IDCard` products and keeps a registry of issued cards."""

    def __init__(self) -> None:
        self._registry: list[IDCard] = []

    def create_product(self, owner: str) -> IDCard:
        # The factory owns the serial-number policy; products can't be
        # created with an arbitrary serial from the outside.
        serial = len(self._registry) + 100
        return IDCard(owner, serial)

    def register_product(self, product: IDCard) -> None:
        self._registry.append(product)

    @property
    def registered_cards(self) -> tuple[IDCard, ...]:
        """All cards issued so far, in issue order (read-only view)."""
        return tuple(self._registry)
