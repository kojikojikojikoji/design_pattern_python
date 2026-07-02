"""Tests for the Abstract Factory example.

Run from the repository root:

    python -m unittest discover -s abstract_factory -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from abstract_factory.dark_theme.factory import DarkThemeFactory
from abstract_factory.light_theme.factory import LightThemeFactory
from abstract_factory.main import build_login_form
from abstract_factory.ui.button import Button
from abstract_factory.ui.checkbox import Checkbox
from abstract_factory.ui.factory import UIFactory


class TestConcreteFactories(unittest.TestCase):
    def test_factories_return_abstract_products(self) -> None:
        """Clients can treat every widget as its abstract interface."""
        for factory in (LightThemeFactory(), DarkThemeFactory()):
            self.assertIsInstance(factory.create_button("OK"), Button)
            self.assertIsInstance(factory.create_checkbox("On"), Checkbox)

    def test_products_from_one_factory_form_a_consistent_family(self) -> None:
        """A button and a checkbox from the same factory always match."""
        for factory in (LightThemeFactory(), DarkThemeFactory()):
            button = factory.create_button("OK")
            checkbox = factory.create_checkbox("On")
            self.assertEqual(button.theme, checkbox.theme)

    def test_different_factories_produce_different_families(self) -> None:
        """Swapping the factory swaps the whole family, not one widget."""
        light = LightThemeFactory().create_button("OK")
        dark = DarkThemeFactory().create_button("OK")
        self.assertEqual(light.theme, "light")
        self.assertEqual(dark.theme, "dark")
        self.assertNotEqual(light.render(), dark.render())

    def test_creation_parameters_reach_the_products(self) -> None:
        """The label passed to the factory ends up on the widget."""
        button = DarkThemeFactory().create_button("Sign in")
        self.assertEqual(button.label, "Sign in")
        self.assertIn("Sign in", button.render())


class TestClientCode(unittest.TestCase):
    def test_client_works_with_any_factory_unchanged(self) -> None:
        """One client function serves every family — that's the payoff."""
        light_form = build_login_form(LightThemeFactory())
        dark_form = build_login_form(DarkThemeFactory())
        # Same structure (3 lines), different skin.
        self.assertEqual(len(light_form.splitlines()), 3)
        self.assertEqual(len(dark_form.splitlines()), 3)
        self.assertNotEqual(light_form, dark_form)

    def test_new_family_needs_no_changes_to_ui_or_client(self) -> None:
        """The pattern is open for extension: add a family, touch nothing."""

        class HighContrastButton(Button):
            def __init__(self, label: str) -> None:
                self._label = label

            @property
            def label(self) -> str:
                return self._label

            @property
            def theme(self) -> str:
                return "high-contrast"

            def render(self) -> str:
                return f"** {self._label} **"

        class HighContrastCheckbox(Checkbox):
            def __init__(self, label: str) -> None:
                self._label = label
                self._checked = False

            @property
            def label(self) -> str:
                return self._label

            @property
            def theme(self) -> str:
                return "high-contrast"

            def toggle(self) -> None:
                self._checked = not self._checked

            def render(self) -> str:
                mark = "#" if self._checked else "."
                return f"{{{mark}}} {self._label}"

        class HighContrastFactory(UIFactory):
            @property
            def theme_name(self) -> str:
                return "High contrast"

            def create_button(self, label: str) -> Button:
                return HighContrastButton(label)

            def create_checkbox(self, label: str) -> Checkbox:
                return HighContrastCheckbox(label)

        form = build_login_form(HighContrastFactory())
        self.assertIn("High contrast", form)
        self.assertIn("** Sign in **", form)


class TestAbstractContracts(unittest.TestCase):
    def test_abstract_classes_cannot_be_instantiated(self) -> None:
        """UIFactory, Button and Checkbox are pure interfaces."""
        for abstract_cls in (UIFactory, Button, Checkbox):
            with self.assertRaises(TypeError):
                abstract_cls()  # type: ignore[abstract]

    def test_incomplete_factory_cannot_be_instantiated(self) -> None:
        """A factory missing one product kind fails at construction time."""

        class ButtonsOnlyFactory(UIFactory):
            @property
            def theme_name(self) -> str:
                return "incomplete"

            def create_button(self, label: str) -> Button:
                return LightThemeFactory().create_button(label)

            # create_checkbox intentionally missing

        with self.assertRaises(TypeError):
            ButtonsOnlyFactory()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
