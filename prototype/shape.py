"""Abstract Prototype — an object that can produce a copy of itself.

In the Prototype pattern, new objects are created by asking an existing
object to *clone itself* instead of calling a class constructor. This
module defines the cloning contract. The key design decision is that
:meth:`Shape.clone` uses :func:`copy.deepcopy`, so a clone shares **no
mutable state** with its prototype — see the shallow-copy pitfall
demonstrated in ``main.py`` and in the tests.
"""

import copy
from abc import ABC, abstractmethod
from typing import Sequence, final


class Shape(ABC):
    """Base class for all clonable shapes.

    Every shape carries a ``label`` and a mutable list of ``tags`` — the
    tags exist precisely to demonstrate why :meth:`clone` must be a
    *deep* copy: with a shallow copy, a prototype and all of its clones
    would silently share one tags list.
    """

    def __init__(self, label: str, tags: Sequence[str]) -> None:
        self._label = label
        #: Mutable metadata; the classic trap for shallow copies.
        self.tags: list[str] = list(tags)

    @property
    def label(self) -> str:
        """Human-readable name of this shape."""
        return self._label

    @final
    def clone(self) -> "Shape":
        """Return an independent copy of this shape.

        Implemented once, here, with :func:`copy.deepcopy` — subclasses
        inherit correct cloning for free, including any nested mutable
        state they add. Compare with ``copy.copy``, which would copy the
        object but *share* its ``tags`` list (see the tests).

        Marked ``@final``: a subclass that needs special copying (say, an
        attribute that must not be duplicated) should implement
        ``__deepcopy__`` — the :mod:`copy` module's own hook — rather
        than weaken the "clones are always deep" guarantee by overriding
        this method.
        """
        return copy.deepcopy(self)

    @abstractmethod
    def describe(self) -> str:
        """Return a one-line description of this shape."""
        raise NotImplementedError
