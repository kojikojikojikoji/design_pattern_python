"""framework — the abstract (pattern) side of the Chain of Responsibility example."""

from .support import Support
from .ticket import Ticket

__all__ = ["Support", "Ticket"]
