# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Template Method pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s template_method -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_template_fixes_the_step_order_and_count` | The skeleton is invariant: open once → body exactly five times → close once, in that order, for every subclass (proven with a spy that records the call sequence). |
| `test_subclasses_share_the_single_inherited_algorithm` | `display()` exists once, at the top of the hierarchy — concrete classes contribute steps, never copies of the algorithm. |
| `test_char_display_renders_five_chars_between_guillemets` | Filling the skeleton with tiny steps yields `<<HHHHH>>` — the shape comes from the template, the content from the subclass. |
| `test_string_display_renders_a_frame_sized_to_the_string` | The *same* skeleton produces a completely different rendering when the steps change — that contrast is the pattern. |
| `test_char_display_rejects_multi_character_input` | Concrete classes validate configuration in `__init__`, keeping the hook steps trivially simple. |
| `test_abstract_display_cannot_be_instantiated` | `AbstractDisplay` is a skeleton to inherit from, never an object to use directly. |
| `test_incomplete_display_cannot_be_instantiated` | Forgetting a step fails **at construction time** (`TypeError`), not halfway through `display()` — the value of `abc.abstractmethod`. |

## A note for learners

When you do the exercises (e.g. adding an `HtmlDisplay`), write the tests *first* by copying this file and adjusting the expectations. The spy test is the important one to imitate: if your new class passes it without you modifying `framework/`, the skeleton is still in charge — which means you have implemented the pattern correctly.
