# `displays/` — the concrete side of the pattern

This package plays the role of an **application developer using the framework**. It plugs concrete rendering styles into the algorithm skeleton defined in [`../framework/`](../framework/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`char_display.py`](char_display.py) | **ConcreteClass** | Renders one character as `<<HHHHH>>` on a single line. |
| [`string_display.py`](string_display.py) | **ConcreteClass** | Renders a string five times inside a `+---+` frame sized to fit. |

## What to notice

**Only the steps are implemented.** Each class defines `open`, `print` and `close` — nothing else. The `display()` skeleton (open → body ×5 → close) is inherited untouched from `framework.AbstractDisplay`. If you find yourself re-implementing `display()`, you are fighting the pattern.

**Same skeleton, radically different output.**

```python
CharDisplay("H").display()          # <<HHHHH>>            (one line)
StringDisplay("Hi!").display()      # +---+ |Hi!| ×5 +---+ (seven lines)
```

Both are one call to the *same inherited method*. `CharDisplay` treats a "step" as a few characters on one line; `StringDisplay` treats it as a whole line. The template neither knows nor cares — it only guarantees the order and the count.

**Constructor = configuration, steps = behaviour.** `CharDisplay` validates its input once in `__init__` (exactly one character) so that the steps can stay trivial. Note that `StringDisplay._print_line` is a private helper shared by two steps — concrete classes may organise their own code freely below the hook line.

**This package depends on `framework/`, never the reverse.** To add a new rendering style (e.g. an `HtmlDisplay`), you add a sibling module here. The skeleton and the existing displays stay untouched.

## Try it

```bash
# from the repository root
python -m template_method.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to build a sibling of these very classes.
