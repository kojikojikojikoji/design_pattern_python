"""Ticket — the request object that travels along the chain.

In GoF terms this is the **Request**. It carries just enough data for a
handler to decide "can I resolve this?" — here, a ticket number. Handlers
never modify the ticket; they only inspect it.
"""


class Ticket:
    """A support ticket identified by a number.

    The number doubles as the "difficulty" of the ticket in this example,
    which lets each concrete :class:`~..framework.support.Support` express
    its speciality as a simple predicate over the number.
    """

    def __init__(self, number: int) -> None:
        self._number = number

    @property
    def number(self) -> int:
        """The ticket's identifying number (also its difficulty here)."""
        return self._number

    def __str__(self) -> str:
        return f"Ticket #{self._number}"

    def __repr__(self) -> str:
        return f"Ticket({self._number})"
