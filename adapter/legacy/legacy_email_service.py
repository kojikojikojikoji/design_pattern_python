"""Adaptee — an existing, useful class with an incompatible interface.

Pretend this module ships inside a third-party package (or a 15-year-old
corner of your own codebase). It works, it is battle-tested, and you are
**not allowed to change it** — every difference from the modern
``Notifier`` interface is deliberate:

* the method is called ``send_mail``, not ``notify``;
* there is no ``subject`` parameter — the subject travels inside a
  ``headers`` dict under the legacy key ``"X-Subject"``;
* failure is reported by returning ``False``, not by raising.

The Adapter pattern exists precisely so that code like this can be reused
behind a modern interface *without editing a single line of it*.
"""


class LegacyEmailService:
    """A legacy e-mail gateway with its own ideas about method signatures.

    In GoF terms this is the **Adaptee**: it already does the real work
    (delivering messages), but its API does not match what today's client
    code expects.
    """

    def __init__(self) -> None:
        self._outbox: list[tuple[str, str, dict[str, str]]] = []

    def send_mail(self, to_address: str, message: str, headers: dict[str, str]) -> bool:
        """Send ``message`` to ``to_address`` with the given ``headers``.

        Returns ``True`` on success and ``False`` on failure — the
        status-code style typical of older APIs.
        """
        if "@" not in to_address:
            print(f"[legacy] REJECTED mail to '{to_address}' (malformed address)")
            return False
        subject = headers.get("X-Subject", "(no subject)")
        print(f"[legacy] MAIL to=<{to_address}> subject='{subject}' body='{message}'")
        self._outbox.append((to_address, message, dict(headers)))
        return True

    @property
    def outbox(self) -> tuple[tuple[str, str, dict[str, str]], ...]:
        """Every mail successfully sent so far (read-only view)."""
        return tuple(self._outbox)
