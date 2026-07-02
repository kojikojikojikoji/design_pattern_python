"""ImageProxy — a virtual proxy (the Proxy of the pattern).

A **virtual proxy** stands in for an expensive object and defers
creating it until it is genuinely needed. Constructing an
``ImageProxy`` costs nothing but storing a filename; the heavyweight
``RealImage`` is created on the *first* :meth:`render` call and cached
for every call after that.

The proxy answers what it can answer itself (``filename``) without
disturbing the real subject, and delegates what it cannot (``render``).
Deciding *which is which* is the craft of writing a good proxy.
"""

from typing import Optional

from .real_image import RealImage
from .subject import Image


class ImageProxy(Image):
    """A lazy-loading stand-in for :class:`RealImage`.

    Same interface, so clients can't tell the difference; different
    lifetime policy, which is the whole point.
    """

    def __init__(self, filename: str) -> None:
        # Deliberately cheap: no I/O, no RealImage — just remember the name.
        self._filename = filename
        self._real: Optional[RealImage] = None

    @property
    def filename(self) -> str:
        # Answered by the proxy itself — the real image is NOT loaded
        # just to repeat a name the proxy already knows.
        return self._filename

    @property
    def loaded(self) -> bool:
        """Whether the real image has been created yet (for observers)."""
        return self._real is not None

    def render(self) -> str:
        """Delegate to the real image, creating it on first use only."""
        if self._real is None:
            self._real = RealImage(self._filename)  # pay the cost now
        return self._real.render()
