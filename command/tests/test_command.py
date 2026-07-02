"""Tests for the Command example.

Run from the repository root:

    python -m unittest discover -s command -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from command.editor.delete_command import DeleteCommand
from command.editor.document import Document
from command.editor.insert_command import InsertCommand
from command.framework.command import Command
from command.framework.history import History
from command.framework.macro_command import MacroCommand


class TestCommands(unittest.TestCase):
    def setUp(self) -> None:
        self.document = Document()

    def test_execute_applies_the_action_to_the_receiver(self) -> None:
        """A command carries its receiver and parameters inside itself."""
        command = InsertCommand(self.document, "Hello")
        command.execute()
        self.assertEqual(self.document.text, "Hello")

    def test_undo_restores_the_previous_receiver_state(self) -> None:
        """execute() then undo() is a no-op on the receiver."""
        self.document.insert("Hello")
        command = InsertCommand(self.document, ", world")
        command.execute()
        command.undo()
        self.assertEqual(self.document.text, "Hello")

    def test_delete_command_stores_the_state_its_undo_needs(self) -> None:
        """A command object is the natural home for undo state."""
        self.document.insert("Hello, world")
        command = DeleteCommand(self.document, 7)
        command.execute()
        self.assertEqual(command.removed, ", world")  # remembered…
        command.undo()
        self.assertEqual(self.document.text, "Hello, world")  # …and restored

    def test_macro_command_executes_children_first_to_last(self) -> None:
        """A group of commands is itself a Command (Composite)."""
        macro = MacroCommand([
            InsertCommand(self.document, "a"),
            InsertCommand(self.document, "b"),
            InsertCommand(self.document, "c"),
        ])
        macro.execute()
        self.assertEqual(self.document.text, "abc")

    def test_macro_command_undoes_children_last_to_first(self) -> None:
        """Undoing a macro unwinds it like a stack — one undo, many steps."""
        self.document.insert("start-")
        macro = MacroCommand([
            InsertCommand(self.document, "abc"),
            DeleteCommand(self.document, 4),  # removes "-abc"
        ])
        macro.execute()
        self.assertEqual(self.document.text, "start")
        macro.undo()  # must restore "-abc" BEFORE removing "abc"
        self.assertEqual(self.document.text, "start-")


class TestHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.document = Document()
        self.history = History()

    def test_history_undoes_and_redoes_without_knowing_command_types(self) -> None:
        """The invoker sees only the Command interface, yet undo/redo work."""
        self.history.run(InsertCommand(self.document, "Hello"))
        self.history.run(InsertCommand(self.document, ", world"))
        self.history.undo()
        self.assertEqual(self.document.text, "Hello")
        self.history.redo()
        self.assertEqual(self.document.text, "Hello, world")

    def test_running_a_new_command_clears_the_redo_stack(self) -> None:
        """After undoing and typing something new, the old future is gone."""
        self.history.run(InsertCommand(self.document, "Hello"))
        self.history.undo()
        self.history.run(InsertCommand(self.document, "Goodbye"))
        self.assertFalse(self.history.can_redo)
        self.assertFalse(self.history.redo())
        self.assertEqual(self.document.text, "Goodbye")

    def test_incomplete_command_cannot_be_instantiated(self) -> None:
        """A command must implement BOTH execute() and undo()."""

        class ExecuteOnly(Command):
            def execute(self) -> None:
                pass
            # undo intentionally missing

        with self.assertRaises(TypeError):
            ExecuteOnly()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
