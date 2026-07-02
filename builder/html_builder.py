"""HtmlBuilder — a Concrete Builder.

It translates the same abstract building steps into HTML. Note that it
also handles a representation-specific concern the Director never needs
to know about: escaping ``<``, ``>`` and ``&`` so that user text cannot
break (or inject into) the markup.
"""

import html
from typing import Sequence

from .document_builder import DocumentBuilder


class HtmlBuilder(DocumentBuilder):
    """Assembles the document as an HTML fragment.

    Every piece of text is passed through :func:`html.escape` — a rule
    that belongs to the HTML representation only, which is exactly why it
    lives inside this builder and nowhere else.
    """

    def __init__(self) -> None:
        self._parts: list[str] = []

    def add_title(self, text: str) -> "HtmlBuilder":
        self._parts.append(f"<h1>{html.escape(text)}</h1>")
        return self

    def add_paragraph(self, text: str) -> "HtmlBuilder":
        self._parts.append(f"<p>{html.escape(text)}</p>")
        return self

    def add_bullet_list(self, items: Sequence[str]) -> "HtmlBuilder":
        lines = ["<ul>"]
        lines.extend(f"  <li>{html.escape(item)}</li>" for item in items)
        lines.append("</ul>")
        self._parts.append("\n".join(lines))
        return self

    def build(self) -> str:
        return "\n".join(self._parts) + "\n"
