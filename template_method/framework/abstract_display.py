"""AbstractDisplay — the AbstractClass that owns the algorithm's skeleton.

In GoF terms this is the **AbstractClass** participant. Its
:meth:`AbstractDisplay.display` is the *template method*: it fixes the
overall algorithm (open, print five times, close) once and for all, while
delegating each individual step to abstract *primitive operations* that
subclasses implement. Subclasses vary the steps; they can never vary the
skeleton.
"""

from abc import ABC, abstractmethod
from typing import final


class AbstractDisplay(ABC):
    """Displays something by running a fixed three-phase algorithm.

    Subclasses (e.g. ``CharDisplay``, ``StringDisplay``) implement the
    three hook steps:

    * :meth:`open`  — start the output (a header, an opening bracket…)
    * :meth:`print` — emit the body once (called five times)
    * :meth:`close` — finish the output

    Client code only ever calls :meth:`display`, so every subclass is
    guaranteed to produce output with the same overall shape.
    """

    @final
    def display(self) -> None:
        """The template method: the skeleton of the algorithm.

        Marked ``@final``: subclasses must not change the procedure
        itself, only fill in the steps. "Open, then the body five times,
        then close" is a guarantee here, not a convention.
        """
        self.open()
        for _ in range(5):
            self.print()
        self.close()

    @abstractmethod
    def open(self) -> None:
        """Primitive operation: begin the output."""
        raise NotImplementedError

    @abstractmethod
    def print(self) -> None:
        """Primitive operation: emit the body once."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Primitive operation: finish the output."""
        raise NotImplementedError
