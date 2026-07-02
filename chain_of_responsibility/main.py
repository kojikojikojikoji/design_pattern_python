"""Demo client for the Chain of Responsibility pattern.

Run from the repository root:

    python -m chain_of_responsibility.main

The point to notice: the client hands every ticket to ``alan`` (the head
of the chain) and nothing else. Which handler resolves a ticket — or
whether anyone does — is decided entirely by the chain's composition,
which could be rewired without touching this loop.
"""

from .framework.support import Support
from .framework.ticket import Ticket
from .supports.limit_support import LimitSupport
from .supports.no_support import NoSupport
from .supports.odd_support import OddSupport
from .supports.special_support import SpecialSupport


def main() -> None:
    # Build the chain. set_next returns its argument, so the links read
    # left-to-right exactly as the tickets will travel.
    alan = NoSupport("Alan")
    bob = LimitSupport("Bob", 100)
    charlie = SpecialSupport("Charlie", 429)
    diana = LimitSupport("Diana", 300)
    elmo = OddSupport("Elmo")
    alan.set_next(bob).set_next(charlie).set_next(diana).set_next(elmo)

    print("Support chain: Alan -> Bob(<100) -> Charlie(#429) "
          "-> Diana(<300) -> Elmo(odd)")
    print()

    # The client only ever talks to the head of the chain.
    head: Support = alan
    for number in (45, 104, 212, 305, 429, 430):
        head.handle(Ticket(number))


if __name__ == "__main__":
    main()
