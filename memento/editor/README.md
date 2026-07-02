# `editor/` — the Originator and its Memento

This package holds the two classes that share a secret: the object whose state matters, and the snapshot type that carries that state around without showing it to anyone else.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`text_editor.py`](text_editor.py) | **Originator** | Owns the state (`content` + `cursor`); the only class that can create (`save`) and consume (`restore`) snapshots meaningfully. |
| [`memento.py`](memento.py) | **Memento** | A frozen, opaque copy of that state. Publicly it offers just a `label`. |

## Narrow vs. wide interface

The GoF description gives the memento two faces:

- **Narrow** (for caretakers and everyone else): enough to store and identify a snapshot. Here: `label` and a state-free `__repr__`.
- **Wide** (for the originator only): full access to the captured state. Here: the underscored `_content` and `_cursor` that `TextEditor.restore` reads.

Java can enforce the split with package-private access; C++ with `friend`. **Python cannot enforce it** — `memento._content` is one attribute access away for anyone. This package approximates the discipline with three stdlib-only measures:

1. **Underscore naming** — linters, IDEs and code review all treat `_content` as off-limits outside the `editor` package.
2. **No public accessors** — there is simply no polite way to ask a memento for its contents; even `repr()` shows only the label.
3. **`__slots__`** — the snapshot cannot gain attributes after construction, keeping it an inert value object rather than a mutable grab-bag.

The tests in [`../tests/`](../tests/) pin all three down (`test_memento_exposes_only_a_narrow_interface`, `test_memento_cannot_gain_new_attributes`).

## Why the originator makes its own snapshots

```python
def save(self, label: str) -> EditorMemento:
    return EditorMemento(self._content, self._cursor, label)
```

The alternative — an outsider reading `editor.content`, `editor.cursor`, and stashing them in a dict — works today and breaks the day the editor grows a third field. By owning `save()`/`restore()`, the originator can evolve its internals freely: add a `selection` field, extend both methods, and every caretaker keeps working untouched, because caretakers never knew what was inside.

## Try it

```bash
# from the repository root
python -m memento.main
```

Then read [`../history/`](../history/) to see the caretaker's side of the bargain.
