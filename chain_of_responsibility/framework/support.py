"""Support — the abstract Handler of the Chain of Responsibility pattern.

:meth:`Support.handle` implements the pattern's core loop as a **template
method**: try to resolve the request yourself; if you can't, forward it to
the next handler; if there is no next handler, report failure. Subclasses
customise exactly one thing — the :meth:`Support.resolve` predicate that
says whether this handler is capable of dealing with a given ticket.
"""

from abc import ABC, abstractmethod
from typing import Optional, final

from .ticket import Ticket


class Support(ABC):
    """A link in the chain of support handlers.

    Concrete supports (e.g. ``LimitSupport``) implement :meth:`resolve`.
    Handlers are linked with :meth:`set_next`, which returns its argument
    so that chains read fluently::

        alan.set_next(bob).set_next(charlie)

    Client code hands a ticket to the *first* handler only and never
    learns (nor cares) which handler ends up resolving it.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._next: Optional["Support"] = None

    @property
    def name(self) -> str:
        """Human-readable name of this handler (used in the demo output)."""
        return self._name

    @property
    def next_support(self) -> Optional["Support"]:
        """The successor this handler forwards to (``None`` at chain end)."""
        return self._next

    def set_next(self, next_support: "Support") -> "Support":
        """Link ``next_support`` after this handler and return it.

        Returning the argument (not ``self``) is what makes the fluent
        one-liner build a *chain* rather than a *star*: each call attaches
        to the handler linked by the previous call.
        """
        self._next = next_support
        return next_support

    @final
    def handle(self, ticket: Ticket) -> Optional["Support"]:
        """Resolve ``ticket`` or pass it along the chain.

        Returns the handler that resolved the ticket, or ``None`` if the
        ticket fell off the end of the chain unresolved. Marked ``@final``
        because the walk itself is the pattern's invariant — subclasses
        vary only in *whether they can resolve*, never in *how the chain
        is traversed*.
        """
        if self.resolve(ticket):
            self.done(ticket)
            return self
        if self._next is not None:
            return self._next.handle(ticket)
        self.fail(ticket)
        return None

    @abstractmethod
    def resolve(self, ticket: Ticket) -> bool:
        """Return ``True`` if this handler can resolve ``ticket``."""
        raise NotImplementedError

    def done(self, ticket: Ticket) -> None:
        """Hook called when this handler resolves the ticket."""
        print(f"{ticket} is resolved by {self._name}.")

    def fail(self, ticket: Ticket) -> None:
        """Hook called at the end of the chain when nobody resolved it."""
        print(f"{ticket} cannot be resolved by anyone.")
