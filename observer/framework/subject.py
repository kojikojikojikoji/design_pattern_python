"""Subject (a.k.a. Observable) — maintains and notifies subscribers.

The Subject owns the subscription list and the notification loop, and
knows observers only through the abstract :class:`Observer` interface.
Concrete subjects (e.g. ``StockPrice``) subclass this and call
:meth:`notify_observers` whenever their state changes.
"""

from .observer import Observer


class Subject:
    """Base class for anything that can be observed.

    Provides the three subscription operations of the pattern:
    :meth:`attach`, :meth:`detach` and :meth:`notify_observers`.
    """

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    @property
    def observers(self) -> tuple[Observer, ...]:
        """The current subscribers, in notification order (read-only view)."""
        return tuple(self._observers)

    def attach(self, observer: Observer) -> None:
        """Subscribe ``observer``. Attaching twice has no extra effect."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Unsubscribe ``observer``. Safe to call from inside ``update``."""
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        """Call ``update(self)`` on every subscriber, in subscription order.

        Note the ``list(...)`` copy: iteration runs over a **snapshot** of
        the subscriber list, so an observer may detach itself (or attach a
        colleague) *during* notification without corrupting the loop —
        a classic real-world Observer bug, prevented here by design.
        """
        for observer in list(self._observers):
            observer.update(self)
