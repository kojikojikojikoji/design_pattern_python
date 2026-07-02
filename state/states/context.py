"""Abstract Context — what a State is allowed to ask of its surroundings.

States need to *do* things: switch the active state, ring the security
company, write the log. Rather than depending on the concrete
``SecuritySystem``, they depend on this small abstract interface — so the
same Day/Night states could drive a GUI app, a test stub, or a real
alarm panel unchanged.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # avoid a runtime circular import; used for hints only
    from .state import State


class Context(ABC):
    """The callbacks a :class:`~state.states.state.State` may invoke."""

    @abstractmethod
    def change_state(self, state: State) -> None:
        """Replace the current state — called by states, and ONLY by states.

        This is the pattern's signature move: transitions are decided
        where the state-specific knowledge lives.
        """
        raise NotImplementedError

    @abstractmethod
    def call_security(self, message: str) -> None:
        """Escalate to the security company (an urgent channel)."""
        raise NotImplementedError

    @abstractmethod
    def record_log(self, message: str) -> None:
        """Record a routine event (a non-urgent channel)."""
        raise NotImplementedError
