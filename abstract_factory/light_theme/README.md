# `light_theme/` — one concrete product family

This package plays the role of an **application developer supplying one theme** to the abstract toolkit defined in [`../ui/`](../ui/). Everything in here belongs to a single, internally consistent family: the light theme.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`widgets.py`](widgets.py) | **ConcreteProduct A / B** | `LightButton` and `LightCheckbox` — the light family's rendering of each widget kind. |
| [`factory.py`](factory.py) | **ConcreteFactory** | `LightThemeFactory` — answers *every* `create_*` call with a light-family widget. |

## What to notice

**The family is designed as a unit.** Square brackets, `x` check marks, "black text on white" — the widgets in this package share one visual language and are meant to appear on screen together. The pattern exists to keep such sets intact.

**One factory answers for the whole family.** Because `LightThemeFactory` implements *all* the creation methods, a client that holds it can only ever receive light widgets:

```python
def create_button(self, label: str) -> Button:
    return LightButton(label)

def create_checkbox(self, label: str) -> Checkbox:
    return LightCheckbox(label)
```

There is no code path that hands out a dark widget by accident — consistency is structural, not disciplined.

**This package depends on `ui/`, never the reverse.** Its sibling [`../dark_theme/`](../dark_theme/) has exactly the same shape and neither imports the other. To add a third theme, you would create another sibling — you would not touch this one.

## Try it

```bash
# from the repository root
python -m abstract_factory.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to build a sibling of this very package.
