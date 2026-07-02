"""Abstract Border — the Decorator of the pattern.

A ``Border`` *is a* ``Display`` (it subclasses it) and *has a*
``Display`` (it wraps one). That dual relationship is the entire
mechanism of the Decorator pattern:

* **is-a** — a decorated object can be used anywhere the bare object
  could, so decoration is transparent to clients;
* **has-a** — the decorator forwards work to the wrapped object and
  adds its own contribution around the result.

Because the wrapped thing is typed as the abstract ``Display``, a
border can wrap a plain ``StringDisplay`` *or another border* — which
is why decorations stack to any depth.
"""

from abc import ABC

from ..display.display import Display


class Border(Display, ABC):
    """Base class for all decorators in this example.

    It contributes nothing visible by itself; it only establishes the
    "wraps another Display" structure that concrete borders build on.
    """

    def __init__(self, display: Display) -> None:
        self._display = display  # the component being decorated
