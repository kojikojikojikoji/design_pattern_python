"""SalesDatabase — a subsystem class (data access).

One of the fiddly classes the Facade hides. It has its own protocol
that callers must respect: ``connect()`` before ``query()``, and
``disconnect()`` afterwards. Forgetting a step raises an error —
exactly the kind of choreography a Facade exists to encapsulate.

In the Facade pattern this class has no special GoF name; it is simply
a *subsystem class*. It knows nothing about the Facade.
"""


class SalesDatabase:
    """An in-memory stand-in for a real sales database.

    The data is hard-coded so the whole tutorial stays deterministic
    and dependency-free. Each row is ``(product, units, unit_price)``.
    """

    _TABLE: dict[str, tuple[tuple[str, int, int], ...]] = {
        "2026-04": (
            ("Widget", 3, 500),
            ("Gadget", 2, 1250),
            ("Gizmo", 8, 75),
        ),
        "2026-05": (
            ("Widget", 5, 500),
            ("Gizmo", 4, 75),
        ),
    }

    def __init__(self) -> None:
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self) -> None:
        """Open the connection. Must be called before :meth:`query`."""
        self._connected = True

    def disconnect(self) -> None:
        """Close the connection. Well-behaved callers always do this."""
        self._connected = False

    def query(self, month: str) -> tuple[tuple[str, int, int], ...]:
        """Return the sales rows for ``month`` (format ``YYYY-MM``)."""
        if not self._connected:
            raise RuntimeError("query() called before connect()")
        if month not in self._TABLE:
            raise ValueError(f"no sales data for month {month!r}")
        return self._TABLE[month]
