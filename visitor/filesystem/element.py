"""Abstract Element — anything a Visitor can visit.

In GoF terms this is the **Element** participant. Its single method,
:meth:`accept`, is one half of the *double dispatch* handshake: the
element receives a visitor and immediately calls back the ``visit_*``
method that matches its own concrete type.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # imported for type hints only — no runtime dependency
    from ..visitors.visitor import Visitor


class Element(ABC):
    """The common interface for every node in the file-system tree.

    Concrete elements (``File``, ``Directory``) implement :meth:`accept`
    with one line each: ``visitor.visit_file(self)`` or
    ``visitor.visit_directory(self)``. That one line is what replaces
    fragile ``isinstance`` chains in every operation.
    """

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        """Dispatch to the visitor method matching this element's type."""
        raise NotImplementedError
