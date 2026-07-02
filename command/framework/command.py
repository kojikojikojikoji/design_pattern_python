"""Command — the abstract interface every executable action implements.

This is the heart of the pattern: **a request, reified as an object**.
Because a request is an object, it can be stored in a list (history),
passed around, composed into bigger commands, executed later — and, if
it also knows how to reverse itself, undone.
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """One undoable action, packaged as an object.

    Concrete commands (e.g. ``InsertCommand``) capture *at construction
    time* everything they need to run: the receiver they act on and the
    parameters of the action. Invokers (e.g. :class:`~.history.History`)
    then execute them without knowing what they do.
    """

    @abstractmethod
    def execute(self) -> None:
        """Perform the action on the receiver."""
        raise NotImplementedError

    @abstractmethod
    def undo(self) -> None:
        """Reverse the action, restoring the receiver's previous state.

        Contract: calling ``undo`` directly after ``execute`` must leave
        the receiver exactly as it was before ``execute``.
        """
        raise NotImplementedError
