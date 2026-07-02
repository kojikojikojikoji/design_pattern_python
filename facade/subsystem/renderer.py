"""ReportRenderer — a subsystem class (presentation).

Builds the text of a report line by line. It, too, has a protocol the
caller must respect: ``begin()`` first, then any number of
``add_line()`` calls, then ``end()`` to get the finished text.
"""

from typing import Optional


class ReportRenderer:
    """Assembles a plain-text report with a title banner."""

    _WIDTH = 40

    def __init__(self) -> None:
        self._lines: Optional[list[str]] = None

    def begin(self, title: str) -> None:
        """Start a new report with a banner around ``title``."""
        rule = "=" * self._WIDTH
        # rstrip: centred titles must not carry invisible trailing spaces
        self._lines = [rule, title.center(self._WIDTH).rstrip(), rule]

    def add_line(self, text: str) -> None:
        """Append one body line. Requires :meth:`begin` first."""
        if self._lines is None:
            raise RuntimeError("add_line() called before begin()")
        self._lines.append(text)

    def add_rule(self) -> None:
        """Append a thin horizontal rule. Requires :meth:`begin` first."""
        self.add_line("-" * self._WIDTH)

    def end(self) -> str:
        """Finish the report and return the full text."""
        if self._lines is None:
            raise RuntimeError("end() called before begin()")
        text = "\n".join(self._lines)
        self._lines = None  # renderer is reusable for the next report
        return text
