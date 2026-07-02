"""Demo client for the Memento pattern.

Run from the repository root:

    python -m memento.main

The client wires an Originator (TextEditor) to a Caretaker (History).
Notice that the client and the caretaker only ever *carry* mementos —
saving and restoring state stays a private conversation between the
editor and its own snapshots.
"""

from .editor.text_editor import TextEditor
from .history.history import History


def show(editor: TextEditor) -> None:
    """Print the editor's state ("|" marks the cursor position)."""
    print(f'  editor: "{editor}" (cursor at {editor.cursor})')


def main() -> None:
    editor = TextEditor()
    history = History()

    print("== Writing the first draft ==")
    editor.write("Hello")
    show(editor)
    history.push(editor.save("draft 1"))
    print("  saved snapshot 'draft 1'")

    print()
    print("== Writing more, then saving again ==")
    editor.write(", world")
    show(editor)
    history.push(editor.save("draft 2"))
    print("  saved snapshot 'draft 2'")

    print()
    print("== An edit in the middle (cursor moves, too) ==")
    editor.move_cursor(5)
    editor.write(" there")
    show(editor)

    print()
    print(f"== Undo (history: {history.labels}) ==")
    editor.restore(history.pop())
    show(editor)

    print()
    print(f"== Undo again (history: {history.labels}) ==")
    editor.restore(history.pop())
    show(editor)

    print()
    print(f"History is now empty: {len(history)} snapshots left.")


if __name__ == "__main__":
    main()
