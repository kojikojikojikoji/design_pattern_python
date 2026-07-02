"""RealImage — the RealSubject of the Proxy pattern.

This is the object that does the actual work — and pays the actual
cost. Its constructor simulates an expensive disk load (in real life:
reading megabytes of pixels, decoding a JPEG, fetching from a network
share). That cost in the constructor is precisely what motivates the
virtual proxy: creating a ``RealImage`` is never free, so we'd like to
avoid creating it until someone truly needs the pixels.

The class counts every load in :attr:`RealImage.loads` so the demo and
the tests can *prove* when loading did and did not happen.
"""

from typing import ClassVar

from .subject import Image


class RealImage(Image):
    """An image whose pixel data is loaded eagerly, in the constructor.

    It implements the :class:`~proxy.subject.Image` contract directly;
    all the interesting expense lives in ``__init__``.
    """

    #: How many times ANY real image has been loaded — the evidence the
    #: tests use to prove the proxy's laziness.
    loads: ClassVar[int] = 0

    def __init__(self, filename: str) -> None:
        self._filename = filename
        # --- the expensive part, paid immediately at construction ---
        print(f"    (disk) loading {filename} ... done")
        RealImage.loads += 1
        width = len(filename) + 4
        self._pixels = [
            "+" + "-" * width + "+",
            "|" + f" {filename} ".center(width) + "|",
            "+" + "-" * width + "+",
        ]

    @property
    def filename(self) -> str:
        return self._filename

    def render(self) -> str:
        """Return the 'pixels' — cheap now, because loading already happened."""
        return "\n".join(self._pixels)
