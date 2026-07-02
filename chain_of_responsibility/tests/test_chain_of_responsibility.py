"""Tests for the Chain of Responsibility example.

Run from the repository root:

    python -m unittest discover -s chain_of_responsibility -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import contextlib
import io
import unittest
from typing import Optional

from chain_of_responsibility.framework.support import Support
from chain_of_responsibility.framework.ticket import Ticket
from chain_of_responsibility.supports.limit_support import LimitSupport
from chain_of_responsibility.supports.no_support import NoSupport
from chain_of_responsibility.supports.odd_support import OddSupport
from chain_of_responsibility.supports.special_support import SpecialSupport


def handle_quietly(head: Support, ticket: Ticket) -> Optional[Support]:
    """Run a ticket through the chain with the demo's prints suppressed."""
    with contextlib.redirect_stdout(io.StringIO()):
        return head.handle(ticket)


class TestChainOfResponsibility(unittest.TestCase):
    def setUp(self) -> None:
        # The same chain the demo builds:
        # Alan -> Bob(<100) -> Charlie(#429) -> Diana(<300) -> Elmo(odd)
        self.alan = NoSupport("Alan")
        self.bob = LimitSupport("Bob", 100)
        self.charlie = SpecialSupport("Charlie", 429)
        self.diana = LimitSupport("Diana", 300)
        self.elmo = OddSupport("Elmo")
        self.alan.set_next(self.bob).set_next(self.charlie) \
            .set_next(self.diana).set_next(self.elmo)

    def test_first_capable_handler_wins(self) -> None:
        """A ticket is resolved by the FIRST handler able to, not the best."""
        # Both Bob (<100) and Diana (<300) could resolve #45,
        # but Bob sits earlier in the chain.
        resolver = handle_quietly(self.alan, Ticket(45))
        self.assertIs(resolver, self.bob)

    def test_request_travels_until_someone_accepts(self) -> None:
        """Handlers that decline are transparent — the ticket flows past them."""
        # 305 is refused by Bob, Charlie and Diana; Elmo (odd) accepts.
        resolver = handle_quietly(self.alan, Ticket(305))
        self.assertIs(resolver, self.elmo)

    def test_unhandled_request_falls_off_the_end(self) -> None:
        """If no handler accepts, the chain reports failure (returns None)."""
        # 430: not < 100, not #429, not < 300, not odd.
        resolver = handle_quietly(self.alan, Ticket(430))
        self.assertIsNone(resolver)

    def test_set_next_returns_its_argument_for_fluent_chaining(self) -> None:
        """a.set_next(b).set_next(c) builds a -> b -> c, not a star."""
        a, b, c = NoSupport("a"), NoSupport("b"), NoSupport("c")
        result = a.set_next(b).set_next(c)
        self.assertIs(result, c)
        self.assertIs(a.next_support, b)
        self.assertIs(b.next_support, c)

    def test_chain_order_determines_the_resolver(self) -> None:
        """Rewiring the chain changes behaviour without touching handlers."""
        # #429 normally goes to specialist Charlie; put Diana (<300)…
        # nothing changes for 429, so use #45 with Odd before Limit instead.
        odd_first = OddSupport("OddFirst")
        limit_second = LimitSupport("LimitSecond", 100)
        odd_first.set_next(limit_second)
        self.assertIs(handle_quietly(odd_first, Ticket(45)), odd_first)
        # Same handlers, opposite order: LimitSecond now sees #45 first.
        odd_last = OddSupport("OddLast")
        limit_first = LimitSupport("LimitFirst", 100)
        limit_first.set_next(odd_last)
        self.assertIs(handle_quietly(limit_first, Ticket(45)), limit_first)

    def test_handlers_work_without_knowing_the_whole_chain(self) -> None:
        """A handler needs no chain at all — decoupling is per-link."""
        lone = LimitSupport("Lone", 100)
        self.assertIs(handle_quietly(lone, Ticket(5)), lone)
        self.assertIsNone(handle_quietly(lone, Ticket(500)))

    def test_no_support_resolves_nothing(self) -> None:
        """An always-declining handler is legal; alone it always fails."""
        lone = NoSupport("Lone")
        self.assertIsNone(handle_quietly(lone, Ticket(1)))

    def test_incomplete_support_cannot_be_instantiated(self) -> None:
        """A handler must implement the resolve() predicate."""
        with self.assertRaises(TypeError):
            Support("nameless")  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
