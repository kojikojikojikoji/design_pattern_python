"""MarkdownBuilder — a Concrete Builder.

It translates the abstract building steps into Markdown syntax. All
Markdown knowledge in the whole package lives in this one file — the
Director and the client never see a ``#`` or a ``-``.
"""

from typing import Sequence

from .document_builder import DocumentBuilder


class MarkdownBuilder(DocumentBuilder):
    """Assembles the document as Markdown text.

    The builder accumulates parts internally; :meth:`build` joins them
    with blank lines, as Markdown block elements require.
    """

    def __init__(self) -> None:
        self._parts: list[str] = []

    def add_title(self, text: str) -> "MarkdownBuilder":
        self._parts.append(f"# {text}")
        return self

    def add_paragraph(self, text: str) -> "MarkdownBuilder":
        self._parts.append(text)
        return self

    def add_bullet_list(self, items: Sequence[str]) -> "MarkdownBuilder":
        self._parts.append("\n".join(f"- {item}" for item in items))
        return self

    def build(self) -> str:
        return "\n\n".join(self._parts) + "\n"
