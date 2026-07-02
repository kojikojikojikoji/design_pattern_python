# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Facade pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s facade -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_one_call_replaces_the_whole_choreography` | The facade produces byte-for-byte what the manual four-class choreography produces — it adds convenience, not magic. |
| `test_report_contains_data_and_summary` | One facade call spans every subsystem layer (data → analysis → rendering). |
| `test_facade_never_leaks_the_connection` | The facade owns the subsystem's lifecycles — the connection is closed even when a middle step fails. |
| `test_subsystem_errors_pass_through_unchanged` | A facade simplifies access; it does not swallow or disguise real errors. |
| `test_email_report_delivers_the_rendered_text` | Facades compose: a bigger convenience (`email_monthly_report`) is built on a smaller one (`build_monthly_report`). |
| `test_subsystem_classes_remain_directly_usable` | The facade is a convenience, not a prison — direct subsystem access stays possible. |
| `test_the_pain_the_facade_removes_is_real` | The subsystem protocols genuinely fail when mis-ordered; that is the complexity being encapsulated. |

## A note for learners

When you do the exercises (e.g. adding a `quarterly_report` method), write the tests *first* by copying this file and adjusting the expectations. The equivalence test (`facade output == manual choreography output`) is the most valuable one to replicate: it keeps your facade honest about being a *simplifier*, not a place where business logic quietly accumulates.
