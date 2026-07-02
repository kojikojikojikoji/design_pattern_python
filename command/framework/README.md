# `framework/` — the abstract side of the pattern

This package plays the role that a **library or framework author** would play in real life. It defines *what a command is*, *how commands compose*, and *how history works*, without knowing anything about documents, text, or any other concrete domain.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`command.py`](command.py) | **Command** | The interface every action implements: `execute()` + `undo()`. |
| [`macro_command.py`](macro_command.py) | **Command (Composite)** | A command made of commands: executes first-to-last, undoes last-to-first. |
| [`history.py`](history.py) | **Invoker** | Runs commands and maintains the undo/redo stacks. |

## The one rule of this package

> `framework/` must **never** import from `editor/` (or any other concrete package).

The dependency arrow points one way only: concrete → abstract. `History` can undo commands that haven't been invented yet, precisely because it depends only on the two-method interface. Add a whole new command family (see the exercises in [`../README.md`](../README.md#10-exercises)) without editing this package — the Open/Closed Principle.

## The `execute`/`undo` contract

```python
class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...
```

The contract every implementation must honour: **`undo()` called immediately after `execute()` restores the receiver exactly.** `History` is built entirely on that promise — it never inspects receivers, diffs state, or knows what "restoring" means.

Declaring both methods with `@abstractmethod` means a command missing its inverse **cannot even be instantiated** — Python raises `TypeError` at construction time rather than corrupting the history at undo time. The test `test_incomplete_command_cannot_be_instantiated` in [`../tests/`](../tests/) demonstrates this.

## Why `MacroCommand` undoes in reverse

```python
def undo(self) -> None:
    for command in reversed(self._commands):
        command.undo()
```

Later sub-commands may depend on state produced by earlier ones (the demo's macro deletes characters that a previous insert created). Undoing in execution order would try to reverse actions whose preconditions no longer hold; unwinding **last-to-first** — like popping a stack — guarantees each `undo()` sees exactly the state its `execute()` left behind.

The sub-command sequence is also copied into a tuple at construction, so a macro always replays exactly the steps it was built with, even if the caller mutates the original list.

## Why `run()` clears the redo stack

```python
def run(self, command: Command) -> None:
    command.execute()
    self._undo_stack.append(command)
    self._redo_stack.clear()
```

After *undo, undo, type something new*, the timeline has branched: the commands you undid describe a future that no longer follows from the document's state. Replaying them could corrupt it. Clearing redo on every fresh `run()` is the rule every editor you have ever used follows — and here it is one line, written once, for all commands.
