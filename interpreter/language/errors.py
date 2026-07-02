"""ParseError — raised when a program text violates the grammar.

Keeping a dedicated exception type lets client code distinguish "the
program is malformed" from any other failure, and lets the tests assert
precisely on grammar violations.
"""


class ParseError(Exception):
    """The program text does not conform to the mini-language grammar."""
