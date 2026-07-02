# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Builder pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s builder -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_markdown_builder_renders_each_step_as_markdown` | All Markdown syntax lives in one class — the step vocabulary maps cleanly onto it. |
| `test_html_builder_renders_each_step_as_html` | The same steps map onto a completely different representation. |
| `test_steps_are_fluent_and_return_the_same_builder` | Every `add_*` returns `self`, so recipes read as one chain — a convention the whole pattern relies on. |
| `test_representation_specific_concerns_stay_in_the_builder` | HTML escaping happens in `HtmlBuilder` and *only* there — format rules can't leak or be forgotten. |
| `test_one_recipe_yields_two_representations` | The pattern's central promise: one Director recipe, many outputs. |
| `test_director_accepts_any_future_builder` | A builder written later (here, an outline generator) plugs into the unchanged Director — Open/Closed. |
| `test_abstract_builder_cannot_be_instantiated` | `DocumentBuilder` is a pure interface — you can't use the vocabulary without implementing it. |
| `test_incomplete_builder_cannot_be_instantiated` | Forgetting a step fails **at construction time** (`TypeError`), not mid-recipe — the value of `abc.abstractmethod`. |

## A note for learners

When you do the exercises (e.g. adding a `PlainTextBuilder`), write the tests *first* by copying this file and adjusting the expectations. If your new builder passes the equivalents of the first three tests without you modifying `director.py`, you have implemented the pattern correctly.
