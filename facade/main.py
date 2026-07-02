"""Demo client for the Facade pattern.

Run from the repository root:

    python -m facade.main

The demo produces the same report twice: first by choreographing the
four subsystem classes by hand (what every client would have to write
without the pattern), then through the Facade's single call. Count the
lines — and the opportunities for mistakes — in each half.
"""

from .report_facade import ReportFacade
from .subsystem.analyzer import SalesAnalyzer
from .subsystem.database import SalesDatabase
from .subsystem.renderer import ReportRenderer


def the_hard_way(month: str) -> str:
    """What client code looks like WITHOUT the Facade.

    Every client must know four classes, their call order, and their
    little protocols (connect before query, begin before add_line...).
    Get any step wrong and it fails at runtime.
    """
    database = SalesDatabase()
    analyzer = SalesAnalyzer()
    renderer = ReportRenderer()

    database.connect()                      # forget this -> RuntimeError
    try:
        rows = database.query(month)
    finally:
        database.disconnect()               # forget this -> connection leak

    summary = analyzer.summarize(rows)      # forget validation? summarize covers it

    renderer.begin(f"Monthly Sales Report {month}")   # forget this -> RuntimeError
    for product, units, unit_price in rows:
        revenue = units * unit_price
        renderer.add_line(
            f"{product:<10} {units:>3} units x ${unit_price:>5,} = ${revenue:>6,}"
        )
    renderer.add_rule()
    renderer.add_line(f"Total units:   {summary.total_units}")
    renderer.add_line(f"Total revenue: ${summary.total_revenue:,}")
    renderer.add_line(f"Best seller:   {summary.best_seller}")
    return renderer.end()


def main() -> None:
    month = "2026-04"

    print("=== WITHOUT the facade: the client choreographs 4 classes ===")
    print(the_hard_way(month))
    print()

    print("=== WITH the facade: one object, one call ===")
    facade = ReportFacade()
    print(facade.build_monthly_report(month))
    print()

    print("=== The facade can also compose bigger conveniences ===")
    facade.email_monthly_report("2026-05", "boss@example.com")


if __name__ == "__main__":
    main()
