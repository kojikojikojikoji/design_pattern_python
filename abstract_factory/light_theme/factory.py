"""LightThemeFactory — a Concrete Factory.

It implements every creation method declared by ``UIFactory``, always
returning widgets from the *light* family. Because one object answers for
the whole family, a client holding this factory physically cannot end up
with a light button next to a dark checkbox.
"""

from ..ui.button import Button
from ..ui.checkbox import Checkbox
from ..ui.factory import UIFactory
from .widgets import LightButton, LightCheckbox


class LightThemeFactory(UIFactory):
    """Produces the matching set of light-theme widgets."""

    @property
    def theme_name(self) -> str:
        return "Light theme"

    def create_button(self, label: str) -> Button:
        return LightButton(label)

    def create_checkbox(self, label: str) -> Checkbox:
        return LightCheckbox(label)
