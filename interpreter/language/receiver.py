"""CommandReceiver — the interface an evaluated program drives.

The language package defines *what a program can ask for* (go, turn
right, turn left) without knowing *who* carries it out. Concrete
receivers — like the :class:`~interpreter.robot.robot.Robot` — live in
their own package and implement this interface. The dependency arrow
points concrete → abstract, exactly as in the other patterns in this
repository.
"""

from abc import ABC, abstractmethod


class CommandReceiver(ABC):
    """Anything that can perform the mini-language's three primitives."""

    @abstractmethod
    def go(self) -> None:
        """Move one step forward in the current heading."""
        raise NotImplementedError

    @abstractmethod
    def turn_right(self) -> None:
        """Rotate 90 degrees clockwise."""
        raise NotImplementedError

    @abstractmethod
    def turn_left(self) -> None:
        """Rotate 90 degrees counter-clockwise."""
        raise NotImplementedError
