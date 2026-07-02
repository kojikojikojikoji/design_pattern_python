"""Abstract Product B — the ``Checkbox`` interface.

The second product kind in the UI family. Note that it is a *sibling* of
:class:`~abstract_factory.ui.button.Button`, not a subclass: Abstract
Factory is about creating several **different** kinds of product that are
guaranteed to match each other.
"""

from abc import ABC, abstractmethod


class Checkbox(ABC):
    """The interface every themed checkbox must implement.

    Unlike a button, a checkbox carries state (checked / unchecked), so the
    interface also declares :meth:`toggle`. How the state is *drawn* is up
    to each concrete theme.
    """

    @property
    @abstractmethod
    def label(self) -> str:
        """The text shown next to the checkbox."""
        raise NotImplementedError

    @property
    @abstractmethod
    def theme(self) -> str:
        """Which product family this checkbox belongs to (e.g. ``"dark"``)."""
        raise NotImplementedError

    @abstractmethod
    def toggle(self) -> None:
        """Flip the checkbox between checked and unchecked."""
        raise NotImplementedError

    @abstractmethod
    def render(self) -> str:
        """Return this checkbox's on-screen representation as text."""
        raise NotImplementedError
