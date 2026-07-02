# `subsystem/` — the complicated machinery behind the facade

This package plays the role of the **existing, fiddly subsystem** — the kind of code that accumulates in any real project: individually reasonable classes that are painful to use *together* because each has its own little protocol.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`database.py`](database.py) | **Subsystem class** | Data access. Protocol: `connect()` → `query(month)` → `disconnect()`. |
| [`analyzer.py`](analyzer.py) | **Subsystem class** | Business logic. Validates rows, reduces them to a `SalesSummary`. |
| [`renderer.py`](renderer.py) | **Subsystem class** | Presentation. Protocol: `begin(title)` → `add_line(...)`* → `end()`. |
| [`mailer.py`](mailer.py) | **Subsystem class** | Delivery. Sends a finished report, records it in an in-memory outbox. |

(In the Facade pattern the subsystem classes have no individual GoF names — collectively they are simply "the subsystem".)

## The two rules of this package

> 1. Subsystem classes **do not know the Facade exists.** Nothing in this package imports `report_facade.py`. The dependency arrow points one way only: facade → subsystem.
> 2. Subsystem classes **do not know each other.** `SalesDatabase` never calls `ReportRenderer`; `SalesAnalyzer` never opens a connection. Each does one job. *Combining* them is exactly the knowledge the Facade captures.

Rule 1 means you can add, refactor or test the facade without touching this package. Rule 2 means each class stays small and independently reusable — the facade is only one possible arrangement of them.

## The pain is deliberate

The protocols here bite for real:

```python
SalesDatabase().query("2026-04")     # RuntimeError: query() called before connect()
ReportRenderer().add_line("oops")    # RuntimeError: add_line() called before begin()
```

That is not sloppy design for the sake of the demo — real subsystems (DB drivers, SMTP clients, XML writers) genuinely have connection lifecycles and call-order requirements. The tests `test_the_pain_the_facade_removes_is_real` in [`../tests/`](../tests/) pin this down, because it is precisely the complexity that [`../report_facade.py`](../report_facade.py) exists to encapsulate.

## Still open for business

The Facade pattern does **not** hide the subsystem behind access controls — this package remains fully importable and usable (see `test_subsystem_classes_remain_directly_usable`). Clients with unusual needs can bypass the facade; everyone else enjoys the one-call API.
