"""History — the Invoker: runs commands and remembers them for undo/redo.

The invoker is deliberately ignorant: it knows commands can ``execute()``
and ``undo()`` and nothing more. All undo/redo behaviour lives here, in
one place, and works for every command ever written — including ones
that don't exist yet.
"""

from typing import List

from .command import Command


class History:
    """Executes commands and maintains undo/redo stacks.

    * ``run(cmd)``  — execute and push onto the undo stack; clears redo.
    * ``undo()``    — pop the undo stack, reverse it, push onto redo.
    * ``redo()``    — pop the redo stack, re-execute, push back onto undo.

    Clearing the redo stack on ``run`` is the classic editor rule: once
    you type something new, the "future" you had undone is gone.
    """

    def __init__(self) -> None:
        self._undo_stack: List[Command] = []
        self._redo_stack: List[Command] = []

    @property
    def can_undo(self) -> bool:
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo_stack)

    def run(self, command: Command) -> None:
        """Execute ``command`` and record it as the newest undoable step."""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self) -> bool:
        """Reverse the most recent command. Returns False if none exists."""
        if not self._undo_stack:
            return False
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        return True

    def redo(self) -> bool:
        """Re-apply the most recently undone command, if any."""
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        return True
