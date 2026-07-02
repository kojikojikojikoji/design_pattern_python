# `dark_theme/` — a second concrete product family

This package is the dark counterpart of [`../light_theme/`](../light_theme/): another complete, internally consistent widget family plugged into the abstract toolkit in [`../ui/`](../ui/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`widgets.py`](widgets.py) | **ConcreteProduct A / B** | `DarkButton` and `DarkCheckbox` — angle brackets, `*` check marks, "white text on black". |
| [`factory.py`](factory.py) | **ConcreteFactory** | `DarkThemeFactory` — answers *every* `create_*` call with a dark-family widget. |

## What to notice

**It mirrors `light_theme/` exactly.** Same file layout, same class shapes, different visual language. That symmetry is the pattern working as intended: each family is a self-contained, swappable plug-in.

**Swapping the factory re-skins the whole application.** The demo client in [`../main.py`](../main.py) renders the same login form twice; the *only* difference between the two runs is which factory object was passed in:

```python
factories: list[UIFactory] = [LightThemeFactory(), DarkThemeFactory()]
```

No `if theme == "dark"` branches anywhere. Adding a theme never grows a conditional.

**Neither concrete family knows the other exists.** `dark_theme/` imports only from `ui/`. You could delete `light_theme/` and this package would keep working — each family stays independent and disposable.

## Try it

```bash
# from the repository root
python -m abstract_factory.main
```

Compare the two rendered forms in the output — same structure, different family.
