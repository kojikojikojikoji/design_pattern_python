"""Component — the interface shared by leaves and composites.

In the Composite pattern the *Component* declares everything a client can
do **uniformly** to any node of the tree: ask its name, ask its size,
render it. Whether the node is a single file or a directory containing
thousands of entries is invisible through this interface — that
uniformity is the pattern's core promise.

Design choice — "safe" vs "transparent":
    This example uses the **safe** design: child management (``add``)
    lives only on :class:`~composite.filesystem.directory.Directory`, so
    ``File("x").add(...)`` is a *type error you can see*, not a runtime
    surprise. The alternative — declaring ``add`` here and raising in
    leaves — is the "transparent" design; see the trade-off discussion in
    the package README.
"""

from abc import ABC, abstractmethod


class Entry(ABC):
    """A node in the file-system tree: either a file or a directory.

    Concrete subclasses implement :meth:`size` and their own tree label;
    the recursive tree rendering is shared here so every node — leaf or
    composite — can print itself the same way.
    """

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        """The entry's name (no path separators)."""
        return self._name

    @property
    @abstractmethod
    def size(self) -> int:
        """Total size in bytes. Composites aggregate this recursively."""
        raise NotImplementedError

    def render_tree(self) -> str:
        """Render this entry (and, for directories, everything below it)."""
        return "\n".join(self._tree_lines())

    def _tree_lines(self) -> list[str]:
        """One rendered line per node; composites override to recurse."""
        return [self._label()]

    def _label(self) -> str:
        """How this node appears in a tree listing."""
        return f"{self.name} ({self.size})"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, size={self.size})"
