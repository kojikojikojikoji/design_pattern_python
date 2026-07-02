# `framework/` — the abstract side of the pattern

This package defines the two *roles* of the Mediator pattern without knowing anything about login dialogs, text fields or buttons. Any coordinated group of objects — form widgets, chat participants, aircraft — could be built on top of it.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`mediator.py`](mediator.py) | **Mediator** | The interface colleagues report to: `colleague_changed()`. |
| [`colleague.py`](colleague.py) | **Colleague** | A participant that knows *only* its mediator; carries the `enabled` flag and the `_changed()` reporting helper. |

## The one rule of this package

> A colleague may hold a reference to its **mediator** — and to nothing else.

Look at `Colleague.__init__`: the only cross-object reference it stores is `self._mediator`. There is no list of siblings, no callbacks to other widgets. The communication topology is a **star**, not a mesh:

```
   TextField ─┐               ┌─ Button
              ├──▶ Mediator ◀─┤
   CheckBox ──┘               └─ TextField
```

With *n* colleagues, a mesh needs up to *n × (n − 1)* directed relationships; the star always needs exactly *n*. That is the pattern's complexity argument in one line.

## Why the report method carries no payload

```python
@abstractmethod
def colleague_changed(self) -> None: ...
```

`colleague_changed()` deliberately says only *"something changed"* — not what, and not what should happen next. The mediator re-reads whichever colleagues it cares about and derives the full dialog state from current facts. This keeps colleagues free of any opinion about consequences ("when I change, disable the OK button") that would couple them right back together.

## Why `_changed()` is provided by the base class

`Colleague._changed()` is the single, uniform channel through which state changes flow upward. Concrete widgets call it and never invent their own side channels — which is what makes the guarantee *"no widget references another widget"* testable (see [`../tests/`](../tests/)).
