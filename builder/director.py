"""Director — knows the *recipe*, not the representation.

The Director encodes construction plans ("a welcome guide is: title,
intro paragraph, list of steps, closing paragraph") as sequences of
abstract building steps. It works with any :class:`DocumentBuilder`, so
the same recipe can produce Markdown today and HTML tomorrow — or a
format that hasn't been invented yet.
"""

from .document_builder import DocumentBuilder


class Director:
    """Drives a builder through a fixed sequence of construction steps.

    The Director is the only place where document *structure* is decided;
    builders decide only *rendering*. Separating the two is the point of
    the pattern: recipes and representations can now vary independently.
    """

    def __init__(self, builder: DocumentBuilder) -> None:
        self._builder = builder

    def construct_welcome_guide(self) -> str:
        """Build the standard welcome guide using the injected builder."""
        return (
            self._builder
            .add_title("Welcome to the Builder Pattern")
            .add_paragraph(
                "The same construction steps can produce entirely "
                "different representations."
            )
            .add_bullet_list(
                [
                    "The Director chooses WHICH steps run, and in what order.",
                    "Each Builder decides HOW a step is rendered.",
                    "The client only picks a builder and asks the Director to build.",
                ]
            )
            .add_paragraph("Swap the builder and rerun: nothing else changes.")
            .build()
        )
