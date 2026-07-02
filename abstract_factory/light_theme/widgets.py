"""Concrete Products for the *light* family.

``LightButton`` and ``LightCheckbox`` implement the abstract interfaces
from ``abstract_factory.ui``. They are designed to be used **together**:
square brackets, ``x`` check marks, "black text on white". Nothing here
knows the dark family exists.
"""

from ..ui.button import Button
from ..ui.checkbox import Checkbox

THEME = "light"


class LightButton(Button):
    """A button drawn in the light theme's visual language."""

    def __init__(self, label: str) -> None:
        self._label = label

    @property
    def label(self) -> str:
        return self._label

    @property
    def theme(self) -> str:
        return THEME

    def render(self) -> str:
        return f"[ {self._label} ]        (light button: black text on white)"

    def __repr__(self) -> str:
        return f"LightButton(label={self._label!r})"


class LightCheckbox(Checkbox):
    """A checkbox drawn in the light theme's visual language."""

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
        mark = "x" if self._checked else " "
        return f"[{mark}] {self._label}   (light checkbox)"

    def __repr__(self) -> str:
        return f"LightCheckbox(label={self._label!r}, checked={self._checked})"
