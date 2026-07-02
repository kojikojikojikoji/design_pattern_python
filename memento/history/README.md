# `history/` — the Caretaker

This package is deliberately small and deliberately ignorant. The **Caretaker** is responsible for a memento's *safekeeping*, never its *contents* — it decides *when* to save and *which* snapshot to hand back, while having no idea what a snapshot contains.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`history.py`](history.py) | **Caretaker** | A LIFO stack of mementos: `push`, `pop`, `labels`, `len`. |

## What to notice

**Look at the imports.** `history.py` imports `EditorMemento` for type hints only — it never imports `TextEditor`. The caretaker cannot restore anything by itself; it can only give a snapshot back to an originator and let *it* do the restoring:

```python
editor.restore(history.pop())   # caretaker supplies, originator consumes
```

**Only the narrow interface is used.** The single memento member `History` ever touches is `label`. The test `test_caretaker_needs_only_the_narrow_interface` proves it by feeding `History` an object that isn't an editor snapshot at all — everything still works, because opacity was the contract all along.

**The caretaker owns the history policy.** LIFO order, "nothing to undo" errors, how many snapshots to keep — all of that is caretaker business. You could swap this class for one with a bounded ring buffer (exercise 2 in [`../README.md`](../README.md#10-exercises)) or a redo stack (exercise 1) without touching the editor at all. That clean division of labour is the pattern's practical payoff.

## Try it

```bash
# from the repository root
python -m memento.main
```
