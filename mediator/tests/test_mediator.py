"""Tests for the Mediator example.

Run from the repository root:

    python -m unittest discover -s mediator -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import contextlib
import io
import unittest

from mediator.framework.colleague import Colleague
from mediator.framework.mediator import Mediator
from mediator.logindialog.login_dialog import LoginDialog
from mediator.logindialog.widgets import TextField


def quiet(callable_, *args):
    """Run ``callable_`` with the demo's console output suppressed."""
    with contextlib.redirect_stdout(io.StringIO()):
        return callable_(*args)


class TestLoginDialogRules(unittest.TestCase):
    def setUp(self) -> None:
        self.dialog = quiet(LoginDialog)

    def test_guest_mode_locks_credential_fields(self) -> None:
        """The mediator, not the widgets, decides who is interactive."""
        self.assertFalse(self.dialog.username.enabled)
        self.assertFalse(self.dialog.password.enabled)
        self.assertTrue(self.dialog.ok.enabled)

    def test_password_unlocks_only_after_a_username_exists(self) -> None:
        """Ordering rules live in ONE place: LoginDialog.colleague_changed."""
        quiet(self.dialog.mode.set_guest, False)
        self.assertFalse(self.dialog.password.enabled)
        quiet(self.dialog.username.set_text, "alice")
        self.assertTrue(self.dialog.password.enabled)

    def test_ok_unlocks_only_when_credentials_are_complete(self) -> None:
        quiet(self.dialog.mode.set_guest, False)
        self.assertFalse(self.dialog.ok.enabled)
        quiet(self.dialog.username.set_text, "alice")
        self.assertFalse(self.dialog.ok.enabled)
        quiet(self.dialog.password.set_text, "s3cret")
        self.assertTrue(self.dialog.ok.enabled)

    def test_any_change_re_derives_the_whole_dialog_state(self) -> None:
        """The mediator recomputes from facts — no stale intermediate state."""
        quiet(self.dialog.mode.set_guest, False)
        quiet(self.dialog.username.set_text, "alice")
        quiet(self.dialog.password.set_text, "s3cret")
        quiet(self.dialog.username.set_text, "")  # username removed again
        self.assertFalse(self.dialog.password.enabled)
        self.assertFalse(self.dialog.ok.enabled)


class TestStarTopology(unittest.TestCase):
    def test_widgets_hold_no_references_to_other_widgets(self) -> None:
        """Colleagues are wired to the mediator only — never to each other."""
        dialog = quiet(LoginDialog)
        widgets = (dialog.mode, dialog.username, dialog.password,
                   dialog.ok, dialog.cancel)
        for widget in widgets:
            peers = [value for value in vars(widget).values()
                     if isinstance(value, Colleague)]
            self.assertEqual(peers, [], f"{widget.name} references a peer widget")

    def test_a_colleague_reports_changes_to_its_mediator(self) -> None:
        """The only outgoing call a widget makes is colleague_changed()."""

        class RecordingMediator(Mediator):
            def __init__(self) -> None:
                self.calls = 0

            def colleague_changed(self) -> None:
                self.calls += 1

        mediator = RecordingMediator()
        field = TextField("field")
        field.set_mediator(mediator)
        quiet(field.set_text, "hello")
        self.assertEqual(mediator.calls, 1)

    def test_disabled_widgets_ignore_user_input(self) -> None:
        """Widgets enforce the mediator's verdict on their own state."""
        dialog = quiet(LoginDialog)  # guest mode: username is disabled
        quiet(dialog.username.set_text, "intruder")
        self.assertEqual(dialog.username.text, "")

    def test_abstract_roles_cannot_be_instantiated(self) -> None:
        """Mediator is a pure interface; you must supply the coordination."""
        with self.assertRaises(TypeError):
            Mediator()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
