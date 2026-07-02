"""Target — the interface the application is written against.

In the Adapter pattern, the *Target* is the interface your client code
expects. Here it is a modern notification API: keyword-friendly
parameters, a separate ``subject`` argument, and failures reported by
**raising an exception** rather than returning a status code.

Nothing in this module knows that a crusty ``LegacyEmailService`` exists —
that ignorance is the whole point. Client code depends on this interface
only, and adapters make incompatible classes satisfy it.
"""

from abc import ABC, abstractmethod


class NotificationError(Exception):
    """Raised when a notification cannot be delivered.

    This exception is part of the Target contract: modern client code
    expects failures to be *raised*, not silently returned as ``False``.
    Translating the legacy service's boolean status code into this
    exception is one of the adapter's jobs.
    """


class Notifier(ABC):
    """The interface every notification channel must satisfy.

    Client code (see ``adapter/main.py``) is written exclusively against
    this abstract class. Whether a message actually travels through a
    legacy e-mail system, a chat webhook, or a carrier pigeon is decided
    by whichever concrete ``Notifier`` gets injected.
    """

    @abstractmethod
    def notify(self, recipient: str, subject: str, body: str) -> None:
        """Deliver ``body`` to ``recipient`` under the given ``subject``.

        Raises :class:`NotificationError` if delivery fails.
        """
        raise NotImplementedError
