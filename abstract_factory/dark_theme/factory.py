"""DarkThemeFactory — a Concrete Factory.

The dark counterpart of ``LightThemeFactory``. Swapping this factory in is
the *only* change needed to re-skin an entire application — every widget
the client builds afterwards automatically comes from the dark family.
"""

from ..ui.button import Button
from ..ui.checkbox import Checkbox
from ..ui.factory import UIFactory
from .widgets import DarkButton, DarkCheckbox


class DarkThemeFactory(UIFactory):
    """Produces the matching set of dark-theme widgets."""

    @property
    def theme_name(self) -> str:
        return "Dark theme"

    def create_button(self, label: str) -> Button:
        return DarkButton(label)

    def create_checkbox(self, label: str) -> Checkbox:
        return DarkCheckbox(label)
