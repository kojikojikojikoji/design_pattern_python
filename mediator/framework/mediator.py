"""Abstract Mediator — the single place where widget interplay is decided.

In the Mediator pattern, colleagues (widgets) never reference each other.
When a colleague's state changes, it reports the fact to its mediator via
:meth:`Mediator.colleague_changed`, and the mediator alone decides how the
*other* colleagues must react. All coordination logic therefore lives in
one class instead of being smeared across every widget.
"""

from abc import ABC, abstractmethod


class Mediator(ABC):
    """Coordinator that reacts whenever any of its colleagues changes.

    Concrete mediators (e.g. ``LoginDialog``) hold references to all their
    colleagues and implement :meth:`colleague_changed` — the one method a
    colleague may call. The traffic pattern is strictly star-shaped:

    * colleague → mediator: "something about me changed"
    * mediator → colleagues: "here is your new enabled/disabled state"
    """

    @abstractmethod
    def colleague_changed(self) -> None:
        """Re-evaluate the whole dialog after any colleague's state change.

        Called by colleagues (via ``Colleague._changed``). The mediator
        inspects its colleagues and pushes consistent state back to them.
        """
        raise NotImplementedError
