"""DeleteCommand — a ConcreteCommand that removes text from a document.

Unlike ``InsertCommand``, its undo cannot be computed — you can't restore
text you no longer have. So ``execute()`` *saves the removed text inside
the command object*. This is the pattern's signature move: a command is
the natural home for the state its own reversal needs.
"""

from ..framework.command import Command
from .document import Document


class DeleteCommand(Command):
    """Delete the last ``count`` characters of a :class:`~.document.Document`."""

    def __init__(self, document: Document, count: int) -> None:
        self._document = document
        self._count = count
        self._removed = ""

    def execute(self) -> None:
        # Remember what we removed so that undo() can restore it.
        self._removed = self._document.delete_last(self._count)

    def undo(self) -> None:
        self._document.insert(self._removed)

    @property
    def removed(self) -> str:
        """The text removed by the last ``execute()`` (for the tests/demo)."""
        return self._removed

    def __repr__(self) -> str:
        return f"DeleteCommand({self._count})"
