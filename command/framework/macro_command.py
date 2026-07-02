"""MacroCommand — a command made of commands (Composite meets Command).

Because :class:`~.command.Command` is an ordinary interface, a *group* of
commands can itself implement it. Executing the macro executes every
child in order; undoing it undoes every child in **reverse** order — the
same discipline as unwinding a stack.
"""

from typing import Sequence, Tuple

from .command import Command


class MacroCommand(Command):
    """A composite command that runs a fixed sequence of sub-commands.

    The sequence is copied and frozen at construction time, so a macro
    always replays exactly the steps it was built with — even if the
    caller later mutates the list it passed in.
    """

    def __init__(self, commands: Sequence[Command]) -> None:
        self._commands: Tuple[Command, ...] = tuple(commands)

    def execute(self) -> None:
        """Execute every sub-command, first to last."""
        for command in self._commands:
            command.execute()

    def undo(self) -> None:
        """Undo every sub-command, last to first.

        Reversing the order matters: later commands may depend on the
        state produced by earlier ones, so they must be unwound first.
        """
        for command in reversed(self._commands):
            command.undo()

    def __len__(self) -> int:
        return len(self._commands)
