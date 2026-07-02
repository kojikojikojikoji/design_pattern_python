"""Abstract Observer — "call me when the subject changes".

The Observer declares the one method a :class:`~observer.framework.subject.Subject`
may call on its subscribers: :meth:`update`. This example uses the
**pull style**: ``update`` receives the subject itself and each observer
pulls whatever state it cares about (``subject.price``, ``subject.symbol``).
The alternative **push style** would pass the changed data as arguments —
see section 4 of the tutorial for the trade-off.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # avoid a runtime circular import; used for hints only
    from .subject import Subject


class Observer(ABC):
    """The interface every subscriber must implement.

    Concrete observers (displays, alerts, loggers, ...) subclass this and
    implement :meth:`update`. The subject knows its observers *only*
    through this interface — never their concrete types.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """React to a change in ``subject``.

        Pull style: the observer receives the subject and reads the state
        it needs. One observer type can therefore watch many subjects and
        tell them apart.
        """
        raise NotImplementedError
