"""Prototype Registry — a catalogue of samples, cloned on demand.

The registry (GoF calls the equivalent role a *prototype manager*) maps
string keys to pre-configured prototype objects. Clients ask for a copy
by name — ``registry.create("alert-badge")`` — and never mention a
concrete class. Adding a new kind of object to the system becomes a
*registration* (a runtime act), not a *code change*.
"""

from .shape import Shape


class ShapeRegistry:
    """Stores prototypes and hands out independent clones of them.

    Two invariants matter here:

    * :meth:`create` returns a **clone**, never the stored prototype
      itself — otherwise every "created" object would be the same shared
      instance, and mutating one would corrupt the catalogue.
    * The registry stores and returns objects only through the abstract
      :class:`Shape` interface; it neither knows nor cares which concrete
      classes are registered.
    """

    def __init__(self) -> None:
        self._prototypes: dict[str, Shape] = {}

    def register(self, key: str, prototype: Shape) -> None:
        """File ``prototype`` in the catalogue under ``key``."""
        self._prototypes[key] = prototype

    def unregister(self, key: str) -> None:
        """Remove the prototype filed under ``key``."""
        del self._prototypes[key]

    def create(self, key: str) -> Shape:
        """Return an independent clone of the prototype filed under ``key``.

        Raises:
            KeyError: if nothing is registered under ``key`` — with the
                available keys listed, because "unknown name" errors
                should help you fix the name.
        """
        try:
            prototype = self._prototypes[key]
        except KeyError:
            available = ", ".join(sorted(self._prototypes)) or "(none)"
            raise KeyError(
                f"No prototype registered under {key!r}. Available: {available}"
            ) from None
        return prototype.clone()

    @property
    def keys(self) -> "tuple[str, ...]":
        """The registered keys, sorted (read-only view)."""
        return tuple(sorted(self._prototypes))
