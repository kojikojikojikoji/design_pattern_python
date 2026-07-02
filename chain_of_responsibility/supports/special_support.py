"""SpecialSupport — a concrete handler for exactly one known case.

It resolves a single, specific ticket number — like a specialist who owns
one notorious recurring incident. Placed early in a chain, it demonstrates
"first capable handler wins": ticket #429 never reaches the generalists
behind it.
"""

from ..framework.support import Support
from ..framework.ticket import Ticket


class SpecialSupport(Support):
    """Resolves only the ticket whose number matches exactly."""

    def __init__(self, name: str, number: int) -> None:
        super().__init__(name)
        self._number = number

    @property
    def number(self) -> int:
        """The one ticket number this specialist handles."""
        return self._number

    def resolve(self, ticket: Ticket) -> bool:
        return ticket.number == self._number
