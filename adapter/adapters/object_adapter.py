"""Object adapter — adapts by *containing* the adaptee (composition).

This is the variant GoF (and most Python code) prefers. The adapter
implements the Target interface (``Notifier``) and holds a reference to
the Adaptee (``LegacyEmailService``), forwarding translated calls to it.

Because the adaptee is injected, this adapter can wrap *any* instance —
including a subclass of the legacy service, a pre-configured one, or a
test double — without new adapter classes.
"""

from typing import final

from ..legacy.legacy_email_service import LegacyEmailService
from ..target.notifier import NotificationError, Notifier


@final
class LegacyEmailAdapter(Notifier):
    """Makes a :class:`LegacyEmailService` usable wherever a
    :class:`Notifier` is expected.

    The translation performed by :meth:`notify`:

    * ``recipient``            → ``to_address``
    * ``subject``              → ``headers["X-Subject"]``
    * ``body``                 → ``message``
    * ``False`` return value   → :class:`NotificationError` raised
    """

    def __init__(self, service: LegacyEmailService) -> None:
        self._service = service  # HAS-A: the adaptee is a component

    def notify(self, recipient: str, subject: str, body: str) -> None:
        delivered = self._service.send_mail(
            to_address=recipient,
            message=body,
            headers={"X-Subject": subject},
        )
        if not delivered:
            raise NotificationError(f"could not notify {recipient!r}")
