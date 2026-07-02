"""CharDisplay — a ConcreteClass.

Renders a single character five times between guillemets, on one line:
``<<HHHHH>>``. Only the three primitive operations are implemented; the
algorithm's skeleton is inherited untouched.
"""

from ..framework.abstract_display import AbstractDisplay


class CharDisplay(AbstractDisplay):
    """Displays one character as ``<<ccccc>>`` on a single line."""

    def __init__(self, ch: str) -> None:
        if len(ch) != 1:
            raise ValueError(f"CharDisplay needs exactly one character, got {ch!r}")
        self._ch = ch

    def open(self) -> None:
        """Start the line with an opening guillemet."""
        print("<<", end="")

    def print(self) -> None:
        """Emit the character once (the template calls this five times)."""
        print(self._ch, end="")

    def close(self) -> None:
        """End the line with a closing guillemet and a newline."""
        print(">>")
