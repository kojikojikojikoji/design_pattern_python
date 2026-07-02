"""NoSupport — a concrete handler that never resolves anything.

It models a pure pass-through station (think: an intake desk or a triage
bot that only logs and forwards). Its value in the example is to show
that a handler which always says "not me" is perfectly legal — the chain
simply flows through it.
"""

from ..framework.support import Support
from ..framework.ticket import Ticket


class NoSupport(Support):
    """Resolves nothing; every ticket is forwarded to the successor."""

    def resolve(self, ticket: Ticket) -> bool:
        return False
