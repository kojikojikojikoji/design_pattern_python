"""SalesAnalyzer — a subsystem class (business logic).

Turns raw database rows into a summary. Like every subsystem class it
is independent of the others: it neither connects to the database nor
formats reports. Combining the pieces is someone else's job — either
the client's (painful) or the Facade's (pleasant).
"""

from typing import NamedTuple


class SalesSummary(NamedTuple):
    """The result of analysing one month of sales rows."""

    total_units: int
    total_revenue: int
    best_seller: str  # product with the highest revenue


class SalesAnalyzer:
    """Validates raw rows and reduces them to a :class:`SalesSummary`."""

    def validate(self, rows: tuple[tuple[str, int, int], ...]) -> None:
        """Reject data the rest of the pipeline could choke on."""
        if not rows:
            raise ValueError("cannot analyse an empty result set")
        for product, units, unit_price in rows:
            if units < 0 or unit_price < 0:
                raise ValueError(f"negative figure in row for {product!r}")

    def summarize(self, rows: tuple[tuple[str, int, int], ...]) -> SalesSummary:
        """Compute totals and the best-selling product (by revenue)."""
        self.validate(rows)
        total_units = sum(units for _, units, _ in rows)
        total_revenue = sum(units * price for _, units, price in rows)
        best_seller = max(rows, key=lambda row: row[1] * row[2])[0]
        return SalesSummary(total_units, total_revenue, best_seller)
