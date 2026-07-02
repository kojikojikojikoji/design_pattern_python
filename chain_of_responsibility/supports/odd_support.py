"""OddSupport — a concrete handler with a quirky speciality.

It resolves tickets with odd numbers only. The point of such an arbitrary
rule: a handler's capability can be *any* predicate, and the chain still
composes — no other class needs to understand the rule.
"""

from ..framework.support import Support
from ..framework.ticket import Ticket


class OddSupport(Support):
    """Resolves tickets whose number is odd."""

    def resolve(self, ticket: Ticket) -> bool:
        return ticket.number % 2 == 1
