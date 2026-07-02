"""ReportFacade — the Facade of the pattern.

This is the single, simple entry point clients are supposed to use.
It owns one instance of each subsystem class and knows the correct
choreography: connect → query → disconnect → validate → summarize →
render → (optionally) mail. Clients call one method and stay blissfully
ignorant of the six-step dance behind it.

Two things worth noticing:

* The Facade adds **no functionality of its own** — every line of real
  work happens in the subsystem. It only encodes the *order of calls*.
* It does **not** forbid direct subsystem access. ``facade.subsystem``
  remains importable for power users; the Facade is a convenience, not
  a prison.
"""

from .subsystem.analyzer import SalesAnalyzer
from .subsystem.database import SalesDatabase
from .subsystem.mailer import ReportMailer
from .subsystem.renderer import ReportRenderer


class ReportFacade:
    """One-call interface to the report-generation subsystem."""

    def __init__(self) -> None:
        self._database = SalesDatabase()
        self._analyzer = SalesAnalyzer()
        self._renderer = ReportRenderer()
        self._mailer = ReportMailer()

    @property
    def mailer(self) -> ReportMailer:
        """The mailer, exposed so callers can inspect the outbox."""
        return self._mailer

    def build_monthly_report(self, month: str) -> str:
        """Build the full sales report for ``month`` — one call.

        Compare this body with the "hard way" block in ``main.py``:
        it is the same choreography, written once, in the right order,
        with the connection reliably closed even if a step fails.
        """
        self._database.connect()
        try:
            rows = self._database.query(month)
        finally:
            self._database.disconnect()

        summary = self._analyzer.summarize(rows)

        self._renderer.begin(f"Monthly Sales Report {month}")
        for product, units, unit_price in rows:
            revenue = units * unit_price
            self._renderer.add_line(
                f"{product:<10} {units:>3} units x ${unit_price:>5,} = ${revenue:>6,}"
            )
        self._renderer.add_rule()
        self._renderer.add_line(f"Total units:   {summary.total_units}")
        self._renderer.add_line(f"Total revenue: ${summary.total_revenue:,}")
        self._renderer.add_line(f"Best seller:   {summary.best_seller}")
        return self._renderer.end()

    def email_monthly_report(self, month: str, recipient: str) -> str:
        """Build the report for ``month``, mail it, and return the text."""
        report = self.build_monthly_report(month)
        self._mailer.send(recipient, report)
        return report
