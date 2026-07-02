# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Command pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s command -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_execute_applies_the_action_to_the_receiver` | A command carries its receiver and parameters inside itself — it is a self-contained request. |
| `test_undo_restores_the_previous_receiver_state` | The core contract: `execute()` then `undo()` is a no-op on the receiver. |
| `test_delete_command_stores_the_state_its_undo_needs` | A command object is the natural home for undo state (the removed text lives *in the command*). |
| `test_macro_command_executes_children_first_to_last` | A group of commands is itself a `Command` — Composite applied to requests. |
| `test_macro_command_undoes_children_last_to_first` | Composite undo unwinds like a stack; reversing the order is what keeps dependent steps correct. |
| `test_history_undoes_and_redoes_without_knowing_command_types` | The invoker sees only the abstract interface, yet full undo/redo works — for future commands too. |
| `test_running_a_new_command_clears_the_redo_stack` | The classic editor rule: type after undoing, and the old "future" is discarded. |
| `test_incomplete_command_cannot_be_instantiated` | Forgetting `undo()` fails **at construction time** (`TypeError`), not when the user hits Ctrl-Z — the value of `abc.abstractmethod`. |

## A note for learners

The macro-undo test is the one to study closely: its macro *inserts* text and then *deletes* some of it, so undoing in the wrong order would produce garbage. If you ever doubt why `MacroCommand.undo()` iterates `reversed(...)`, break it on purpose and watch that test fail. When you do the exercises (e.g. adding `ReplaceAllCommand`), write the tests *first* by copying this file — your new command passes the equivalents of the first three tests or it isn't a command yet.
