"""InsertCommand — a ConcreteCommand that appends text to a document.

Its undo is computed, not stored: since the command knows exactly what it
inserted, reversing it is "delete that many characters".
"""

from ..framework.command import Command
from .document import Document


class InsertCommand(Command):
    """Append a fixed piece of text to a :class:`~.document.Document`."""

    def __init__(self, document: Document, text: str) -> None:
        self._document = document
        self._text = text

    def execute(self) -> None:
        self._document.insert(self._text)

    def undo(self) -> None:
        self._document.delete_last(len(self._text))

    def __repr__(self) -> str:
        return f"InsertCommand({self._text!r})"
