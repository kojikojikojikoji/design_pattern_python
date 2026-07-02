"""Abstract Factory — one creation method per product kind.

This is the pattern's namesake class. Where Factory Method has *one*
``create_product`` hook, Abstract Factory bundles **several** — one per
product kind — into a single interface. A concrete factory implements all
of them for one family (one theme), which is what guarantees that a button
and a checkbox obtained from the same factory always match.
"""

from abc import ABC, abstractmethod

from .button import Button
from .checkbox import Checkbox


class UIFactory(ABC):
    """Creates a *family* of matching UI widgets.

    Concrete factories (``LightThemeFactory``, ``DarkThemeFactory``)
    implement every creation method for their theme. Client code that is
    handed a ``UIFactory`` can build a whole screen without ever naming a
    concrete widget class — and without any risk of mixing themes.
    """

    @property
    @abstractmethod
    def theme_name(self) -> str:
        """Human-readable name of the family this factory produces."""
        raise NotImplementedError

    @abstractmethod
    def create_button(self, label: str) -> Button:
        """Create this family's button variant."""
        raise NotImplementedError

    @abstractmethod
    def create_checkbox(self, label: str) -> Checkbox:
        """Create this family's checkbox variant."""
        raise NotImplementedError
