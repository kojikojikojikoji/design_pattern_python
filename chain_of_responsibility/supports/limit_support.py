"""LimitSupport — a concrete handler with a capability ceiling.

It resolves any ticket whose number is *below* its limit — like a support
tier that handles everything up to a certain difficulty and escalates the
rest.
"""

from ..framework.support import Support
from ..framework.ticket import Ticket


class LimitSupport(Support):
    """Resolves tickets with ``number < limit``; escalates the rest."""

    def __init__(self, name: str, limit: int) -> None:
        super().__init__(name)
        self._limit = limit

    @property
    def limit(self) -> int:
        """Tickets strictly below this number are within capability."""
        return self._limit

    def resolve(self, ticket: Ticket) -> bool:
        return ticket.number < self._limit
