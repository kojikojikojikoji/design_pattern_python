"""Concrete Colleagues — console simulations of three dialog widgets.

Each widget does two things and two things only:

1. manage its *own* state (checked, text, pressed), and
2. call ``self._changed()`` when that state changes.

None of them knows any other widget exists. Search this file for
``username`` or ``password`` — you won't find them. That absence is the
whole point of the Mediator pattern.
"""

from ..framework.colleague import Colleague


class CheckBox(Colleague):
    """A two-way selector between "Guest login" and "Member login"."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._guest = True  # dialogs open in guest mode

    @property
    def guest(self) -> bool:
        """``True`` while "Guest login" is selected."""
        return self._guest

    def set_guest(self, guest: bool) -> None:
        """Tick the box one way or the other, then notify the mediator."""
        if guest != self._guest:
            self._guest = guest
            mode = "Guest" if guest else "Member"
            print(f"[{self.name}] {mode} login selected")
            self._changed()


class TextField(Colleague):
    """A single-line text input (username, password, ...)."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._text = ""

    @property
    def text(self) -> str:
        """The field's current content."""
        return self._text

    def set_text(self, text: str) -> None:
        """Simulate the user typing into the field.

        A disabled field ignores input, exactly like a greyed-out widget
        in a real GUI toolkit.
        """
        if not self.enabled:
            print(f"[{self.name}] input ignored (field is disabled)")
            return
        if text != self._text:
            self._text = text
            print(f"[{self.name}] text -> {text!r}")
            self._changed()


class Button(Colleague):
    """A push button whose *pressability* is controlled by the mediator."""

    def press(self) -> None:
        """Simulate a click. Only an enabled button actually fires."""
        if self.enabled:
            print(f"[{self.name}] pressed!")
        else:
            print(f"[{self.name}] press ignored (button is disabled)")
