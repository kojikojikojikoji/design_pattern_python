"""Tests for the Decorator example.

Run from the repository root:

    python -m unittest discover -s decorator -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import io
import unittest
from contextlib import redirect_stdout

from decorator.border.border import Border
from decorator.border.full_border import FullBorder
from decorator.border.side_border import SideBorder
from decorator.display.display import Display
from decorator.display.string_display import StringDisplay


def all_rows(display: Display) -> list[str]:
    """Collect every row of a display as a list of strings."""
    return [display.get_row_text(row) for row in range(display.get_rows())]


class TestDecoratorTransparency(unittest.TestCase):
    def test_decorated_object_is_still_a_display(self) -> None:
        """Decoration is transparent: a wrapped object keeps the Component type."""
        decorated = FullBorder(SideBorder(StringDisplay("hi"), "*"))
        self.assertIsInstance(decorated, Display)

    def test_show_prints_exactly_the_rows_of_the_stack(self) -> None:
        """Clients render any stack with the same one call — show()."""
        decorated = SideBorder(StringDisplay("abc"), "#")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            decorated.show()
        self.assertEqual(buffer.getvalue(), "#abc#\n")


class TestConcreteDecorators(unittest.TestCase):
    def test_side_border_pads_both_sides_of_every_row(self) -> None:
        """A decorator adds its contribution around the wrapped result."""
        decorated = SideBorder(StringDisplay("abc"), "*")
        self.assertEqual(all_rows(decorated), ["*abc*"])
        self.assertEqual(decorated.get_columns(), 5)

    def test_full_border_frames_the_component(self) -> None:
        """FullBorder adds two rows and two columns — a complete frame."""
        decorated = FullBorder(StringDisplay("abc"))
        self.assertEqual(all_rows(decorated), ["+---+", "|abc|", "+---+"])


class TestStacking(unittest.TestCase):
    def test_decorators_stack_to_any_depth(self) -> None:
        """Decorators wrap Displays — including other decorators."""
        display: Display = StringDisplay("x")
        for _ in range(10):
            display = FullBorder(display)
        # each layer adds 2 columns and 2 rows to the 1x1 core
        self.assertEqual(display.get_columns(), 21)
        self.assertEqual(display.get_rows(), 21)

    def test_decoration_leaves_the_component_untouched(self) -> None:
        """Wrapping composes objects; it never mutates the wrapped one."""
        core = StringDisplay("core")
        FullBorder(SideBorder(core, "!"))
        self.assertEqual(all_rows(core), ["core"])
        self.assertEqual(core.get_columns(), 4)

    def test_every_row_of_a_stack_matches_the_reported_width(self) -> None:
        """Each layer keeps the rectangle invariant its wrapper relies on."""
        stack = SideBorder(FullBorder(SideBorder(StringDisplay("Hello."), "*")), "/")
        for row_text in all_rows(stack):
            self.assertEqual(len(row_text), stack.get_columns())

    def test_border_is_abstract_and_cannot_be_instantiated(self) -> None:
        """Border only defines the wrapping structure; it is not usable alone."""
        with self.assertRaises(TypeError):
            Border(StringDisplay("x"))  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
