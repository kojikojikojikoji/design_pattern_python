"""Abstract State — one behaviour set for one mode of the system.

Every event the security system can experience appears here as a method.
A concrete state answers all of them *for its own mode only*: DayState
implements "how the system behaves in daytime", NightState "at night".
No method here (or in the context) ever asks "is it day or night?" —
being the right object replaces asking.
"""

from abc import ABC, abstractmethod

from .context import Context


class State(ABC):
    """The interface both :class:`DayState` and :class:`NightState` fulfil.

    Each handler receives the :class:`Context` so it can act (log, call
    security) and — crucially — trigger transitions via
    ``context.change_state(...)`` when its own exit condition is met.
    """

    @abstractmethod
    def on_clock(self, context: Context, hour: int) -> None:
        """The clock ticked to ``hour`` — transition if we left this mode."""
        raise NotImplementedError

    @abstractmethod
    def on_use_safe(self, context: Context) -> None:
        """Someone opened the safe."""
        raise NotImplementedError

    @abstractmethod
    def on_alarm(self, context: Context) -> None:
        """The emergency bell was pressed."""
        raise NotImplementedError

    @abstractmethod
    def on_phone(self, context: Context) -> None:
        """The office phone was used."""
        raise NotImplementedError
