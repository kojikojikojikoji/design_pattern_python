"""Tests for the Facade example.

Run from the repository root:

    python -m unittest discover -s facade -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import io
import unittest
from contextlib import redirect_stdout

from facade.main import the_hard_way
from facade.report_facade import ReportFacade
from facade.subsystem.database import SalesDatabase
from facade.subsystem.renderer import ReportRenderer


class TestReportFacade(unittest.TestCase):
    def setUp(self) -> None:
        self.facade = ReportFacade()

    def test_one_call_replaces_the_whole_choreography(self) -> None:
        """The facade's single method produces exactly what the manual
        multi-class choreography produces — it adds convenience, not magic."""
        self.assertEqual(
            self.facade.build_monthly_report("2026-04"),
            the_hard_way("2026-04"),
        )

    def test_report_contains_data_and_summary(self) -> None:
        """One call spans all subsystem layers: data, analysis, rendering."""
        report = self.facade.build_monthly_report("2026-04")
        self.assertIn("Widget", report)                # database layer
        self.assertIn("Total revenue: $4,600", report)  # analyzer layer
        self.assertIn("=" * 40, report)                 # renderer layer

    def test_facade_never_leaks_the_connection(self) -> None:
        """The facade encapsulates the subsystem's protocols (connect /
        disconnect) — even when a step in the middle fails."""
        with self.assertRaises(ValueError):
            self.facade.build_monthly_report("1999-01")
        # the connection was still closed on the way out
        self.assertFalse(self.facade._database.connected)

    def test_subsystem_errors_pass_through_unchanged(self) -> None:
        """A facade simplifies access; it does not swallow real errors."""
        with self.assertRaises(ValueError):
            self.facade.build_monthly_report("not-a-month")

    def test_email_report_delivers_the_rendered_text(self) -> None:
        """Facades can compose bigger conveniences out of smaller ones."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):  # silence the mailer's confirmation
            report = self.facade.email_monthly_report("2026-05", "a@b.com")
        self.assertEqual(self.facade.mailer.outbox, (("a@b.com", report),))


class TestSubsystemStaysOpen(unittest.TestCase):
    def test_subsystem_classes_remain_directly_usable(self) -> None:
        """The facade is a convenience, not a prison — power users can
        still drive the subsystem classes themselves."""
        database = SalesDatabase()
        database.connect()
        rows = database.query("2026-04")
        database.disconnect()
        self.assertEqual(rows[0], ("Widget", 3, 500))

    def test_the_pain_the_facade_removes_is_real(self) -> None:
        """The subsystem protocols genuinely bite when mis-ordered —
        this is the complexity the facade shields clients from."""
        with self.assertRaises(RuntimeError):
            SalesDatabase().query("2026-04")   # forgot connect()
        with self.assertRaises(RuntimeError):
            ReportRenderer().add_line("oops")  # forgot begin()


if __name__ == "__main__":
    unittest.main()
