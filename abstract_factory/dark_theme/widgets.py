"""Concrete Products for the *dark* family.

A sibling of ``light_theme.widgets`` with its own visual language: angle
brackets, ``*`` check marks, "white text on black". It implements the same
abstract interfaces, so any client written against ``abstract_factory.ui``
can use these widgets without modification.
"""

from ..ui.button import Button
from ..ui.checkbox import Checkbox

THEME = "dark"


class DarkButton(Button):
    """A button drawn in the dark theme's visual language."""

    def __init__(self, label: str) -> None:
        self._label = label

    @property
    def label(self) -> str:
        return self._label

    @property
    def theme(self) -> str:
        return THEME

    def render(self) -> str:
        return f"< {self._label} >        (dark button: white text on black)"

    def __repr__(self) -> str:
        return f"DarkButton(label={self._label!r})"


class DarkCheckbox(Checkbox):
    """A checkbox drawn in the dark theme's visual language."""

    def __init__(self, label: str) -> None:
        self._label = label
        self._checked = False

    @property
    def label(self) -> str:
        return self._label

    @property
    def theme(self) -> str:
        return THEME

    @property
    def checked(self) -> bool:
        """Current state (extra to the interface; handy for tests)."""
        return self._checked

    def toggle(self) -> None:
        self._checked = not self._checked

    def render(self) -> str:
        mark = "*" if self._checked else " "
        return f"({mark}) {self._label}   (dark checkbox)"

    def __repr__(self) -> str:
        return f"DarkCheckbox(label={self._label!r}, checked={self._checked})"
