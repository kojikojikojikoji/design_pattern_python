"""framework — the abstract (pattern) side of the Command example."""

from .command import Command
from .history import History
from .macro_command import MacroCommand

__all__ = ["Command", "History", "MacroCommand"]
