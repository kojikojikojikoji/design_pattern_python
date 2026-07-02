"""TextEditor — the Originator.

The Originator is the object whose state is worth saving. Only it knows
its own internals, so only it can create a meaningful snapshot
(:meth:`save`) and only it can consume one (:meth:`restore`). Everyone
else — the caretaker included — merely ferries mementos around.
"""

from .memento import EditorMemento


class TextEditor:
    """A minimal text editor: a string of content plus a cursor position.

    Two fields are deliberately used (not just one) to show that a
    memento captures the originator's state *as a whole* — restoring
    brings back both the text and where you were typing.
    """

    def __init__(self) -> None:
        self._content = ""
        self._cursor = 0

    @property
    def content(self) -> str:
        """The full text currently in the editor."""
        return self._content

    @property
    def cursor(self) -> int:
        """The insertion point, as an index into :attr:`content`."""
        return self._cursor

    def write(self, text: str) -> None:
        """Insert ``text`` at the cursor and advance the cursor past it."""
        self._content = (
            self._content[: self._cursor] + text + self._content[self._cursor:]
        )
        self._cursor += len(text)

    def move_cursor(self, index: int) -> None:
        """Move the insertion point (clamped to the valid range)."""
        self._cursor = max(0, min(index, len(self._content)))

    def save(self, label: str) -> EditorMemento:
        """Snapshot the current state into an opaque memento.

        The originator decides what goes into a snapshot — callers cannot
        build a memento with forged internals because they are not meant
        to call ``EditorMemento(...)`` themselves.
        """
        return EditorMemento(self._content, self._cursor, label)

    def restore(self, memento: EditorMemento) -> None:
        """Rewind this editor to a previously saved state.

        This is the *wide interface* in action: the originator reads the
        memento's underscored attributes. In Python that privilege is a
        convention rather than a compiler rule — this method (plus
        ``save``) should stay the only code that touches them.
        """
        self._content = memento._content
        self._cursor = memento._cursor

    def __str__(self) -> str:
        # Render the cursor as "|" so demo output shows both state fields.
        return f"{self._content[: self._cursor]}|{self._content[self._cursor:]}"
