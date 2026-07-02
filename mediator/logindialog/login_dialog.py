"""LoginDialog — the concrete Mediator.

This is the *only* class in the whole package that knows the dialog's
business rules ("guests skip credentials", "no password before a
username", ...). The widgets stay generic and reusable; the coordination
knowledge is concentrated here, in one readable method.
"""

from ..framework.mediator import Mediator
from .widgets import Button, CheckBox, TextField


class LoginDialog(Mediator):
    """A login form that keeps its five widgets mutually consistent.

    The rules it enforces (all inside :meth:`colleague_changed`):

    * Guest mode  — username/password are disabled, OK is enabled.
    * Member mode — username is enabled; the password field unlocks only
      once a username exists; OK unlocks only once both fields are filled.
    * Cancel is always enabled.
    """

    def __init__(self) -> None:
        # The mediator creates and owns all of its colleagues.
        self.mode = CheckBox("mode")
        self.username = TextField("username")
        self.password = TextField("password")
        self.ok = Button("OK")
        self.cancel = Button("Cancel")

        for widget in (self.mode, self.username, self.password, self.ok, self.cancel):
            widget.set_mediator(self)

        # Establish a consistent initial state (dialogs open in guest mode).
        self.colleague_changed()

    def colleague_changed(self) -> None:
        """Recompute every widget's enabled state from the current facts.

        Because this method derives the *entire* dialog state from scratch
        each time, there is no event-ordering bug to have: no matter which
        colleague changed, the outcome is the same for the same facts.
        """
        if self.mode.guest:
            self.username.set_enabled(False)
            self.password.set_enabled(False)
            self.ok.set_enabled(True)
        else:
            self.username.set_enabled(True)
            has_username = bool(self.username.text)
            has_password = bool(self.password.text)
            self.password.set_enabled(has_username)
            self.ok.set_enabled(has_username and has_password)
        self.cancel.set_enabled(True)
