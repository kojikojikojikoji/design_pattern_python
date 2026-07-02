# `editor/` — the concrete side of the pattern

This package plays the role of an **application developer using the framework**. It plugs a specific domain — a tiny text editor — into the abstract machinery defined in [`../framework/`](../framework/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`document.py`](document.py) | **Receiver** | The text buffer commands operate on: `insert()` and `delete_last()`. |
| [`insert_command.py`](insert_command.py) | **ConcreteCommand** | Appends text; its undo is *computed* (delete that many characters). |
| [`delete_command.py`](delete_command.py) | **ConcreteCommand** | Removes text; its undo state is *stored* (the removed text itself). |

## What to notice

**The receiver is oblivious.** `Document` knows how to edit text and nothing about commands, undo, or history. You could use it directly, test it directly, and reuse it in a program with no undo at all. Command objects wrap it from the outside.

**Two undo strategies, side by side.** `InsertCommand` reverses itself by *arithmetic* — it knows it added `len(text)` characters, so undo deletes that many. `DeleteCommand` cannot recompute what it destroyed, so `execute()` saves the removed text inside the command:

```python
def execute(self) -> None:
    self._removed = self._document.delete_last(self._count)

def undo(self) -> None:
    self._document.insert(self._removed)
```

This pairing is the most instructive part of the package: **whatever information an inverse needs, the command captures it at execute time.** Nothing else in the system has to care.

**One enabling detail in the receiver.** `Document.delete_last()` *returns* the text it removed. A receiver API that reports what it did is what makes cheap, precise undo possible — a small design courtesy worth copying into your own receivers.

**This package depends on `framework/`, never the reverse.** To support a different domain (turtle graphics, a mixer console, a database), you would create a *sibling* package with its own receiver and commands — `History` and `MacroCommand` would work with it unchanged.

## Try it

```bash
# from the repository root
python -m command.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to add a new command to this very package.
