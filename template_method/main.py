"""Demo client for the Template Method pattern.

Run from the repository root:

    python -m template_method.main

The point to notice: the client makes the SAME call — ``display()`` — on
every object, and each one is rendered by the same inherited skeleton
(open, body x5, close) filled in with different steps.
"""

from .displays.char_display import CharDisplay
from .displays.string_display import StringDisplay
from .framework.abstract_display import AbstractDisplay


def main() -> None:
    # Three displays behind one abstract type. The concrete classes are
    # mentioned only here; everything below uses AbstractDisplay.
    displays: list[AbstractDisplay] = [
        CharDisplay("H"),
        StringDisplay("Hello, world."),
        StringDisplay("Template Method"),
    ]

    for display in displays:
        display.display()  # one template method, three renderings
        print()


if __name__ == "__main__":
    main()
