"""Demo client for the Decorator pattern.

Run from the repository root:

    python -m decorator.main

The point to notice: ``b1``…``b4`` are all typed as the abstract
``Display``. The client renders each one with the same ``show()``
call, entirely unaware of whether it is holding a bare string or a
four-layer onion of borders.
"""

from .border.full_border import FullBorder
from .border.side_border import SideBorder
from .display.display import Display
from .display.string_display import StringDisplay


def main() -> None:
    # A bare component, then the same component wrapped once and twice.
    b1: Display = StringDisplay("Hello, world.")
    b2: Display = SideBorder(b1, "#")
    b3: Display = FullBorder(b2)

    print("b1 - the bare component:")
    b1.show()
    print()
    print("b2 - b1 wrapped in a SideBorder('#'):")
    b2.show()
    print()
    print("b3 - b2 wrapped again in a FullBorder:")
    b3.show()
    print()

    # Decorators wrap decorators: build a four-layer onion in one go.
    b4: Display = SideBorder(
        FullBorder(
            FullBorder(
                SideBorder(
                    FullBorder(StringDisplay("Hello.")),
                    "*",
                )
            )
        ),
        "/",
    )
    print("b4 - five layers of decoration, one show() call:")
    b4.show()


if __name__ == "__main__":
    main()
