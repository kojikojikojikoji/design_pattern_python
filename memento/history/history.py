"""History — the Caretaker.

The caretaker is responsible for a memento's *safekeeping*, never its
*contents*. Notice what this module does NOT import: ``TextEditor``.
It has no idea what kind of object produced the snapshots it holds, or
what is inside them — it only relies on the narrow interface (``label``).
That ignorance is exactly what makes undo generic and the originator's
encapsulation safe.
"""

from ..editor.memento import EditorMemento


class History:
    """A LIFO stack of snapshots — the classic undo history.

    ``push`` records a snapshot; ``pop`` hands the most recent one back
    so the *originator* can restore from it. The caretaker itself never
    calls anything on a memento except :attr:`EditorMemento.label`.
    """

    def __init__(self) -> None:
        self._stack: list[EditorMemento] = []

    def push(self, memento: EditorMemento) -> None:
        """Store a snapshot on top of the undo stack."""
        self._stack.append(memento)

    def pop(self) -> EditorMemento:
        """Remove and return the most recent snapshot (LIFO).

        Raises :class:`IndexError` when there is nothing to undo — the
        caretaker owns the "is there history?" question, not the editor.
        """
        if not self._stack:
            raise IndexError("nothing to undo")
        return self._stack.pop()

    @property
    def labels(self) -> tuple[str, ...]:
        """Labels of stored snapshots, oldest first (narrow interface only)."""
        return tuple(memento.label for memento in self._stack)

    def __len__(self) -> int:
        return len(self._stack)
