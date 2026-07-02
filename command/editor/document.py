"""Document — the Receiver: the object commands actually operate on.

The receiver knows *how* to do things (insert text, delete text) but has
no idea it is being driven by command objects, let alone that its edits
are undoable. Undo knowledge lives entirely in the commands.
"""


class Document:
    """A minimal text buffer with two primitive operations."""

    def __init__(self) -> None:
        self._text = ""

    @property
    def text(self) -> str:
        """The current contents of the document."""
        return self._text

    def insert(self, text: str) -> None:
        """Append ``text`` to the end of the document."""
        self._text += text

    def delete_last(self, count: int) -> str:
        """Remove the last ``count`` characters and return them.

        Returning the removed text is what allows ``DeleteCommand`` to
        undo itself: the command squirrels the return value away and
        re-inserts it on ``undo()``.
        """
        if count <= 0:
            return ""
        removed = self._text[-count:]
        self._text = self._text[:-count]
        return removed
