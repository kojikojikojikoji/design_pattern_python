"""Abstract Builder — the step-by-step construction interface.

In the Builder pattern, this class declares the *vocabulary of building
steps* (add a title, add a paragraph, add a bullet list) without saying
anything about the final representation. Concrete builders translate the
same steps into Markdown, HTML, or any format invented later.
"""

from abc import ABC, abstractmethod
from typing import Sequence


class DocumentBuilder(ABC):
    """The interface every concrete document builder must implement.

    Each ``add_*`` step returns ``self`` so that steps can be chained
    fluently (``builder.add_title(...).add_paragraph(...)``). The
    :meth:`build` step finishes construction and returns the assembled
    document as a string.

    Note what is *absent*: there is no ``add_markdown_heading`` or
    ``add_html_tag``. The steps are format-neutral on purpose — that is
    what lets one Director drive every builder.
    """

    @abstractmethod
    def add_title(self, text: str) -> "DocumentBuilder":
        """Append the document's title. Returns ``self`` for chaining."""
        raise NotImplementedError

    @abstractmethod
    def add_paragraph(self, text: str) -> "DocumentBuilder":
        """Append a paragraph of body text. Returns ``self`` for chaining."""
        raise NotImplementedError

    @abstractmethod
    def add_bullet_list(self, items: Sequence[str]) -> "DocumentBuilder":
        """Append a bulleted list. Returns ``self`` for chaining."""
        raise NotImplementedError

    @abstractmethod
    def build(self) -> str:
        """Finish construction and return the complete document."""
        raise NotImplementedError
