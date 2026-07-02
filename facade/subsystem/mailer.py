"""ReportMailer — a subsystem class (delivery).

"Sends" a finished report to a recipient. To keep the tutorial
dependency-free and deterministic it prints a confirmation and records
the delivery in an in-memory outbox instead of talking to an SMTP
server — the shape of the API is what matters here.
"""


class ReportMailer:
    """Delivers report texts and keeps a record of what was sent."""

    def __init__(self) -> None:
        self._outbox: list[tuple[str, str]] = []

    @property
    def outbox(self) -> tuple[tuple[str, str], ...]:
        """Every ``(recipient, body)`` pair sent so far (read-only view)."""
        return tuple(self._outbox)

    def send(self, recipient: str, body: str) -> None:
        """Deliver ``body`` to ``recipient``."""
        if "@" not in recipient:
            raise ValueError(f"{recipient!r} is not an e-mail address")
        self._outbox.append((recipient, body))
        line_count = body.count("\n") + 1
        print(f"[mailer] sent {line_count}-line report to {recipient}")
