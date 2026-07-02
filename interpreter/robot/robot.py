"""Robot — a concrete CommandReceiver that walks a 2-D grid.

The robot starts at (0, 0) facing north. ``go`` moves one cell in the
current heading; ``right``/``left`` rotate 90 degrees. Every action is
appended to a human-readable log, which is what the demo prints — so an
interpreted program leaves a visible trace.
"""

from typing import List, Tuple

from ..language.receiver import CommandReceiver

_HEADINGS: Tuple[str, ...] = ("north", "east", "south", "west")
_MOVES = {
    "north": (0, 1),
    "east": (1, 0),
    "south": (0, -1),
    "west": (-1, 0),
}


class Robot(CommandReceiver):
    """A grid-walking robot driven by interpreted programs."""

    def __init__(self) -> None:
        self._x = 0
        self._y = 0
        self._heading_index = 0  # index into _HEADINGS; 0 = north
        self._log: List[str] = []

    @property
    def position(self) -> Tuple[int, int]:
        """Current (x, y) grid position."""
        return (self._x, self._y)

    @property
    def heading(self) -> str:
        """Current compass heading: north, east, south or west."""
        return _HEADINGS[self._heading_index]

    @property
    def log(self) -> Tuple[str, ...]:
        """Every action performed so far, in order (read-only view)."""
        return tuple(self._log)

    def go(self) -> None:
        dx, dy = _MOVES[self.heading]
        self._x += dx
        self._y += dy
        self._log.append(f"go    -> moved {self.heading} to ({self._x}, {self._y})")

    def turn_right(self) -> None:
        self._heading_index = (self._heading_index + 1) % 4
        self._log.append(f"right -> now facing {self.heading}")

    def turn_left(self) -> None:
        self._heading_index = (self._heading_index - 1) % 4
        self._log.append(f"left  -> now facing {self.heading}")
