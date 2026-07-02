"""Demo client for the Builder pattern.

Run from the repository root:

    python -m builder.main

The point to notice: the Director is constructed twice with different
builders, and ``construct_welcome_guide`` — the recipe — is executed
character-for-character identically both times. Only the representation
of the result differs.
"""

from .director import Director
from .html_builder import HtmlBuilder
from .markdown_builder import MarkdownBuilder


def main() -> None:
    # The only lines that mention concrete classes: choosing the builders.
    print("=== The same recipe, rendered as Markdown ===")
    print(Director(MarkdownBuilder()).construct_welcome_guide())

    print("=== The same recipe, rendered as HTML ===")
    print(Director(HtmlBuilder()).construct_welcome_guide())


if __name__ == "__main__":
    main()
