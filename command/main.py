"""Demo client for the Command pattern.

Run from the repository root:

    python -m command.main

The point to notice: the ``History`` invoker drives every edit, undo and
redo without knowing what any command does. All it sees is the abstract
``Command`` interface — insert, delete and macro commands are completely
interchangeable to it.
"""

from .editor.delete_command import DeleteCommand
from .editor.document import Document
from .editor.insert_command import InsertCommand
from .framework.history import History
from .framework.macro_command import MacroCommand


def main() -> None:
    document = Document()
    history = History()

    def show(action: str) -> None:
        print(f"{action:<24} document = {document.text!r}")

    print("--- Editing ---")
    history.run(InsertCommand(document, "Hello"))
    show("run insert 'Hello'")
    history.run(InsertCommand(document, ", world"))
    show("run insert ', world'")
    history.run(DeleteCommand(document, 7))
    show("run delete 7 chars")

    print()
    print("--- Undo / redo ---")
    history.undo()
    show("undo (delete)")
    history.undo()
    show("undo (insert)")
    history.redo()
    show("redo (insert)")

    print()
    print("--- Macro command ---")
    sign_off = MacroCommand([
        InsertCommand(document, "!"),
        InsertCommand(document, " -- bye"),
    ])
    history.run(sign_off)
    show("run macro sign-off")
    history.undo()
    show("undo (whole macro)")


if __name__ == "__main__":
    main()
