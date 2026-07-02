"""editor — the concrete (application) side of the Command example."""

from .delete_command import DeleteCommand
from .document import Document
from .insert_command import InsertCommand

__all__ = ["DeleteCommand", "Document", "InsertCommand"]
