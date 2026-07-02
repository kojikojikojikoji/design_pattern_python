"""Tests for the Memento example.

Run from the repository root:

    python -m unittest discover -s memento -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from memento.editor.text_editor import TextEditor
from memento.history.history import History


class TestSaveAndRestore(unittest.TestCase):
    def setUp(self) -> None:
        self.editor = TextEditor()

    def test_restore_returns_the_editor_to_the_saved_state(self) -> None:
        """A memento captures the originator's state as a whole."""
        self.editor.write("Hello")
        self.editor.move_cursor(2)
        snapshot = self.editor.save("mid-edit")

        self.editor.move_cursor(5)
        self.editor.write(", world")
        self.editor.restore(snapshot)

        self.assertEqual(self.editor.content, "Hello")
        self.assertEqual(self.editor.cursor, 2)  # cursor came back too

    def test_editing_after_save_does_not_change_the_snapshot(self) -> None:
        """Mementos are frozen copies, not live views of the originator."""
        self.editor.write("v1")
        snapshot = self.editor.save("v1")
        self.editor.write(" v2")
        self.editor.restore(snapshot)
        self.assertEqual(self.editor.content, "v1")

    def test_undo_restores_snapshots_in_lifo_order(self) -> None:
        """Caretaker (History) + originator = a working undo stack."""
        history = History()
        for text in ("a", "b", "c"):
            self.editor.write(text)
            history.push(self.editor.save(text))

        self.editor.restore(history.pop())
        self.assertEqual(self.editor.content, "abc")
        self.editor.restore(history.pop())
        self.assertEqual(self.editor.content, "ab")
        self.editor.restore(history.pop())
        self.assertEqual(self.editor.content, "a")


class TestEncapsulation(unittest.TestCase):
    def test_memento_exposes_only_a_narrow_interface(self) -> None:
        """The only public attribute of a snapshot is its display label."""
        memento = TextEditor().save("empty")
        public = {name for name in dir(memento) if not name.startswith("_")}
        self.assertEqual(public, {"label"})

    def test_memento_repr_does_not_leak_state(self) -> None:
        """Even printing a memento reveals the label, not the contents."""
        editor = TextEditor()
        editor.write("secret text")
        self.assertEqual(repr(editor.save("draft")), "<EditorMemento 'draft'>")

    def test_memento_cannot_gain_new_attributes(self) -> None:
        """__slots__ keeps snapshots inert value objects."""
        memento = TextEditor().save("empty")
        with self.assertRaises(AttributeError):
            memento.extra = "sneaky"  # type: ignore[attr-defined]

    def test_caretaker_needs_only_the_narrow_interface(self) -> None:
        """History works with ANY object offering .label — proof that it
        never peeks at editor internals."""

        class OpaqueToken:
            label = "not an editor snapshot at all"

        history = History()
        token = OpaqueToken()
        history.push(token)  # type: ignore[arg-type]
        self.assertEqual(history.labels, ("not an editor snapshot at all",))
        self.assertIs(history.pop(), token)

    def test_pop_on_empty_history_raises(self) -> None:
        """The caretaker owns the 'anything to undo?' question."""
        with self.assertRaises(IndexError):
            History().pop()


if __name__ == "__main__":
    unittest.main()
