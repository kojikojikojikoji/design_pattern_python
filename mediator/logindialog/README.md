# `logindialog/` — the concrete side of the pattern

This package plugs a specific application — a login form — into the abstract roles defined in [`../framework/`](../framework/). It is a console simulation of the classic dialog from Hiroshi Yuki's book: a Guest/Member checkbox, two text fields, and OK/Cancel buttons.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`widgets.py`](widgets.py) | **ConcreteColleague** (×3) | `CheckBox`, `TextField`, `Button` — manage their own state, report changes via `_changed()`. |
| [`login_dialog.py`](login_dialog.py) | **ConcreteMediator** | `LoginDialog` — owns all five widgets and holds *all* of the coordination rules. |

## What to notice

**The widgets are ignorant of each other.** Open [`widgets.py`](widgets.py) and search for `username`, `password` or `OK`. You will not find them — a `TextField` has no idea it sits next to a `Button`. That is why the same three widget classes could be reused, unchanged, in a completely different dialog with completely different rules.

**All the rules live in one method.** Every business rule of the form — guests skip credentials, no password before a username, OK requires both — is expressed inside `LoginDialog.colleague_changed()`:

```python
if self.mode.guest:
    self.username.set_enabled(False)
    self.password.set_enabled(False)
    self.ok.set_enabled(True)
else:
    self.username.set_enabled(True)
    has_username = bool(self.username.text)
    ...
```

Need a new rule ("Cancel is disabled while logging in")? You edit this one method. Without a mediator, that rule would be sliced up and buried inside several widget event handlers.

**The state is *derived*, never patched.** `colleague_changed()` recomputes every widget's enabled state from scratch on every change. There is no "if the password just changed, then…" branching per event source, so there is no event-ordering bug to have.

## Try it

```bash
# from the repository root
python -m mediator.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to add a fourth widget and observe how little code changes.
