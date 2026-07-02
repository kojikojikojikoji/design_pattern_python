"""Context — the token stream the parser consumes.

In GoF terms this is the **Context**: it holds the information global to
the interpretation — here, the sequence of tokens and a cursor into it.
Each Node's ``parse`` classmethod pulls tokens from the Context and
advances the cursor; the Context itself knows nothing about the grammar.
"""

from typing import List, Optional

from .errors import ParseError


class Context:
    """A cursor over the whitespace-separated tokens of a program text."""

    def __init__(self, program_text: str) -> None:
        self._tokens: List[str] = program_text.split()
        self._index = 0

    @property
    def current_token(self) -> Optional[str]:
        """The token under the cursor, or ``None`` past the end."""
        if self._index < len(self._tokens):
            return self._tokens[self._index]
        return None

    def advance(self) -> None:
        """Move the cursor to the next token."""
        self._index += 1

    def expect(self, token: str) -> None:
        """Consume ``token`` or raise :class:`ParseError`.

        This is the parser's workhorse for fixed keywords such as
        ``program``, ``repeat`` and ``end``.
        """
        if self.current_token != token:
            raise ParseError(
                f"expected {token!r} but found {self.current_token!r}"
            )
        self.advance()

    def read_number(self) -> int:
        """Consume the current token as a non-negative integer."""
        token = self.current_token
        if token is None or not token.isdigit():
            raise ParseError(f"expected a number but found {token!r}")
        self.advance()
        return int(token)
