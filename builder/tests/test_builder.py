"""Tests for the Builder example.

Run from the repository root:

    python -m unittest discover -s builder -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from builder.director import Director
from builder.document_builder import DocumentBuilder
from builder.html_builder import HtmlBuilder
from builder.markdown_builder import MarkdownBuilder


class TestConcreteBuilders(unittest.TestCase):
    def test_markdown_builder_renders_each_step_as_markdown(self) -> None:
        """All Markdown knowledge lives inside MarkdownBuilder."""
        document = (
            MarkdownBuilder()
            .add_title("Report")
            .add_paragraph("Quarterly numbers.")
            .add_bullet_list(["Revenue up", "Costs down"])
            .build()
        )
        self.assertEqual(
            document,
            "# Report\n\nQuarterly numbers.\n\n- Revenue up\n- Costs down\n",
        )

    def test_html_builder_renders_each_step_as_html(self) -> None:
        """All HTML knowledge lives inside HtmlBuilder."""
        document = (
            HtmlBuilder()
            .add_title("Report")
            .add_paragraph("Quarterly numbers.")
            .add_bullet_list(["Revenue up", "Costs down"])
            .build()
        )
        self.assertEqual(
            document,
            "<h1>Report</h1>\n<p>Quarterly numbers.</p>\n"
            "<ul>\n  <li>Revenue up</li>\n  <li>Costs down</li>\n</ul>\n",
        )

    def test_steps_are_fluent_and_return_the_same_builder(self) -> None:
        """add_* returns self, so recipes read as a single chain."""
        builder = MarkdownBuilder()
        self.assertIs(builder.add_title("T"), builder)
        self.assertIs(builder.add_paragraph("P"), builder)
        self.assertIs(builder.add_bullet_list(["I"]), builder)

    def test_representation_specific_concerns_stay_in_the_builder(self) -> None:
        """Only the HTML builder escapes markup — the recipe never worries."""
        risky = "Ampersands & <tags>"
        html_doc = HtmlBuilder().add_paragraph(risky).build()
        md_doc = MarkdownBuilder().add_paragraph(risky).build()
        self.assertIn("Ampersands &amp; &lt;tags&gt;", html_doc)
        self.assertIn("Ampersands & <tags>", md_doc)


class TestDirector(unittest.TestCase):
    def test_one_recipe_yields_two_representations(self) -> None:
        """The Director's recipe is representation-agnostic."""
        markdown = Director(MarkdownBuilder()).construct_welcome_guide()
        html_doc = Director(HtmlBuilder()).construct_welcome_guide()
        # Same content...
        self.assertIn("Welcome to the Builder Pattern", markdown)
        self.assertIn("Welcome to the Builder Pattern", html_doc)
        # ...different representation.
        self.assertTrue(markdown.startswith("# "))
        self.assertTrue(html_doc.startswith("<h1>"))

    def test_director_accepts_any_future_builder(self) -> None:
        """A builder written later plugs into the unchanged Director."""

        class OutlineBuilder(DocumentBuilder):
            """Renders only the skeleton — e.g. for a table of contents."""

            def __init__(self) -> None:
                self._lines: list[str] = []

            def add_title(self, text: str) -> "OutlineBuilder":
                self._lines.append(f"TITLE: {text}")
                return self

            def add_paragraph(self, text: str) -> "OutlineBuilder":
                self._lines.append("(paragraph)")
                return self

            def add_bullet_list(self, items) -> "OutlineBuilder":
                self._lines.append(f"(list of {len(items)})")
                return self

            def build(self) -> str:
                return "\n".join(self._lines)

        outline = Director(OutlineBuilder()).construct_welcome_guide()
        self.assertEqual(
            outline,
            "TITLE: Welcome to the Builder Pattern\n"
            "(paragraph)\n(list of 3)\n(paragraph)",
        )


class TestAbstractContracts(unittest.TestCase):
    def test_abstract_builder_cannot_be_instantiated(self) -> None:
        """DocumentBuilder is a pure interface."""
        with self.assertRaises(TypeError):
            DocumentBuilder()  # type: ignore[abstract]

    def test_incomplete_builder_cannot_be_instantiated(self) -> None:
        """A builder missing a step fails at construction time."""

        class HalfBuilder(DocumentBuilder):
            def add_title(self, text: str) -> "HalfBuilder":
                return self

            def add_paragraph(self, text: str) -> "HalfBuilder":
                return self

            # add_bullet_list and build intentionally missing

        with self.assertRaises(TypeError):
            HalfBuilder()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
