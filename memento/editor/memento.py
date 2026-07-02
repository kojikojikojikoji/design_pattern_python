"""EditorMemento — an opaque snapshot of a TextEditor's state.

This class is the pattern's namesake and its most misunderstood part.
A memento has **two faces**:

* a **narrow interface**, shown to everyone: here, just ``label`` and
  ``__repr__``. Enough to store, list and hand back — nothing more.
* a **wide interface**, meant for the Originator only: the underscored
  attributes ``_content`` and ``_cursor`` that ``TextEditor.restore``
  reads to rebuild its state.

Java enforces the split with package-private access; Python cannot.
Instead we approximate it with conventions and small hard edges:
underscore names (linters and IDEs warn), no public accessors for the
state, and ``__slots__`` so the object cannot even grow new attributes.
Honest code only ever sees the narrow face.
"""


class EditorMemento:
    """A frozen snapshot. Create via :meth:`TextEditor.save`, not directly.

    Caretakers (e.g. ``History``) treat instances as opaque tokens: they
    may keep them, count them and read :attr:`label` — and nothing else.
    """

    # __slots__ removes __dict__: the snapshot cannot gain attributes
    # after construction, which keeps it an inert value object.
    __slots__ = ("_content", "_cursor", "_label")

    def __init__(self, content: str, cursor: int, label: str) -> None:
        self._content = content
        self._cursor = cursor
        self._label = label

    @property
    def label(self) -> str:
        """The narrow interface: a display name for undo menus and logs."""
        return self._label

    def __repr__(self) -> str:
        # Deliberately does NOT leak the captured state.
        return f"<EditorMemento {self._label!r}>"
