"""Tests for the Template Method example.

Run from the repository root:

    python -m unittest discover -s template_method -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import io
import unittest
from contextlib import redirect_stdout

from template_method.displays.char_display import CharDisplay
from template_method.displays.string_display import StringDisplay
from template_method.framework.abstract_display import AbstractDisplay


def rendered_output(display: AbstractDisplay) -> str:
    """Run display() and capture exactly what it wrote to stdout."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        display.display()
    return buffer.getvalue()


class TestTemplateSkeleton(unittest.TestCase):
    def test_template_fixes_the_step_order_and_count(self) -> None:
        """The skeleton is the guarantee: open once, body exactly five
        times, close once — in that order, for EVERY subclass."""
        calls: list[str] = []

        class SpyDisplay(AbstractDisplay):
            def open(self) -> None:
                calls.append("open")

            def print(self) -> None:
                calls.append("print")

            def close(self) -> None:
                calls.append("close")

        SpyDisplay().display()
        self.assertEqual(calls, ["open"] + ["print"] * 5 + ["close"])

    def test_subclasses_share_the_single_inherited_algorithm(self) -> None:
        """Concrete classes implement only the steps; display() itself is
        one shared method, not three copies."""
        self.assertIs(CharDisplay.display, AbstractDisplay.display)
        self.assertIs(StringDisplay.display, AbstractDisplay.display)


class TestConcreteDisplays(unittest.TestCase):
    def test_char_display_renders_five_chars_between_guillemets(self) -> None:
        """open='<<', body='H' x5, close='>>' — the skeleton shapes the line."""
        self.assertEqual(rendered_output(CharDisplay("H")), "<<HHHHH>>\n")

    def test_string_display_renders_a_frame_sized_to_the_string(self) -> None:
        """Same skeleton, different steps: a seven-line framed box."""
        expected = "+---+\n" + "|Hi!|\n" * 5 + "+---+\n"
        self.assertEqual(rendered_output(StringDisplay("Hi!")), expected)

    def test_char_display_rejects_multi_character_input(self) -> None:
        """Concrete classes validate their own configuration up front, so
        the template's steps can stay trivially simple."""
        with self.assertRaises(ValueError):
            CharDisplay("HH")


class TestPatternContracts(unittest.TestCase):
    def test_abstract_display_cannot_be_instantiated(self) -> None:
        """AbstractDisplay is a skeleton, not a usable object."""
        with self.assertRaises(TypeError):
            AbstractDisplay()  # type: ignore[abstract]

    def test_incomplete_display_cannot_be_instantiated(self) -> None:
        """A subclass must implement ALL three steps — a missing step
        fails at construction time, not halfway through display()."""

        class HalfDisplay(AbstractDisplay):
            def open(self) -> None:
                pass

            def print(self) -> None:
                pass
            # close intentionally missing

        with self.assertRaises(TypeError):
            HalfDisplay()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
