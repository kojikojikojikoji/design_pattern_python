"""Abstract Colleague — a widget that only ever talks to its mediator.

A colleague knows exactly one thing about the outside world: the mediator
it belongs to. It never holds a reference to another colleague, so adding
or removing a widget from the dialog cannot break any *other* widget.
"""

from abc import ABC
from typing import Optional

from .mediator import Mediator


class Colleague(ABC):
    """Base class for every widget managed by a :class:`Mediator`.

    Concrete colleagues (text fields, checkboxes, buttons) inherit two
    responsibilities from this class:

    * an ``enabled`` flag that only the mediator is supposed to flip
      (via :meth:`set_enabled`), and
    * the :meth:`_changed` helper that reports state changes *upward*
      to the mediator — never sideways to another widget.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._mediator: Optional[Mediator] = None
        self._enabled = True

    @property
    def name(self) -> str:
        """The widget's display name (used in the console output)."""
        return self._name

    @property
    def enabled(self) -> bool:
        """Whether the widget currently accepts user interaction."""
        return self._enabled

    def set_mediator(self, mediator: Mediator) -> None:
        """Attach this colleague to its (one and only) mediator."""
        self._mediator = mediator

    def set_enabled(self, enabled: bool) -> None:
        """Enable/disable the widget. Called by the mediator, not by peers."""
        if enabled != self._enabled:
            self._enabled = enabled
            print(f"[{self._name}] {'enabled' if enabled else 'disabled'}")

    def _changed(self) -> None:
        """Report "my state changed" to the mediator.

        This is the only outgoing call a colleague ever makes. Note that
        the colleague does not say *what* should happen next — deciding
        that is entirely the mediator's job.
        """
        if self._mediator is not None:
            self._mediator.colleague_changed()
