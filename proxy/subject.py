"""Abstract Image — the Subject of the Proxy pattern.

The Subject is the shared interface that makes proxies possible: the
real object (``RealImage``) and every stand-in for it (``ImageProxy``,
``ProtectedImage``) all implement this one contract. Client code is
written against ``Image`` and therefore cannot tell — and never needs
to know — whether it is holding the real thing or a proxy.

That interchangeability is the entire trick. A proxy that offered a
*different* interface would force clients to care; a proxy with the
*same* interface can be slid between client and real object without
touching a single line of client code.
"""

from abc import ABC, abstractmethod


class Image(ABC):
    """Something with a filename that can be rendered to text."""

    @property
    @abstractmethod
    def filename(self) -> str:
        """The name of the image file. Answering this must be cheap —
        no proxy should have to touch the real resource for it."""
        raise NotImplementedError

    @abstractmethod
    def render(self) -> str:
        """Return the image as displayable text.

        For the real image this requires the (expensive) pixel data;
        proxies decide *whether and when* that expense is paid.
        """
        raise NotImplementedError
