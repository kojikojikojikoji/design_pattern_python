"""Class adapter — adapts by *inheriting* from the adaptee.

The class adapter subclasses **both** the Target (``Notifier``) and the
Adaptee (``LegacyEmailService``). In C++ this is done with private
inheritance; in Python it is plain multiple inheritance.

Trade-offs versus the object adapter:

* (+) No forwarding boilerplate — ``send_mail`` is simply inherited, and
  protected members of the adaptee could be overridden if needed.
* (−) The adapter is welded to one concrete adaptee class at *class
  definition time*; you cannot hand it a different instance to wrap.
* (−) The adaptee's whole public API (``send_mail``, ``outbox``) leaks
  into the adapter's interface, so clients *can* bypass the translation.

Prefer the object adapter unless you specifically need to override parts
of the adaptee's behaviour.
"""

from typing import final

from ..legacy.legacy_email_service import LegacyEmailService
from ..target.notifier import NotificationError, Notifier


@final
class LegacyEmailClassAdapter(Notifier, LegacyEmailService):
    """IS-A :class:`Notifier` *and* IS-A :class:`LegacyEmailService`.

    Only :meth:`notify` is defined here; the actual sending machinery is
    inherited directly from the adaptee.
    """

    def notify(self, recipient: str, subject: str, body: str) -> None:
        delivered = self.send_mail(  # inherited from LegacyEmailService
            to_address=recipient,
            message=body,
            headers={"X-Subject": subject},
        )
        if not delivered:
            raise NotificationError(f"could not notify {recipient!r}")
