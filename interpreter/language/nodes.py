"""Node classes — one class per grammar rule (the heart of Interpreter).

The mini-language's grammar, in BNF:

    <program>    ::= "program" <command list>
    <command list> ::= <command>* "end"
    <command>    ::= <repeat command> | <primitive command>
    <repeat command> ::= "repeat" <number> <command list>
    <primitive command> ::= "go" | "right" | "left"

Each non-terminal on the left becomes exactly one class below, and each
class knows how to do two things:

* ``parse(context)``  — build itself from the token stream
  (together the classes form a recursive-descent parser), and
* ``execute(receiver)`` — interpret itself against a receiver
  (together the resulting tree of objects *is* the program).

That one-rule-one-class mapping is what makes the pattern maintainable:
change a grammar rule, and you know exactly which class to edit.
"""

from abc import ABC, abstractmethod
from typing import List

from .context import Context
from .errors import ParseError
from .receiver import CommandReceiver


class Node(ABC):
    """AbstractExpression — the interface shared by every grammar rule."""

    @classmethod
    @abstractmethod
    def parse(cls, context: Context) -> "Node":
        """Consume tokens from ``context`` and build this node."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, receiver: CommandReceiver) -> None:
        """Interpret this node, driving ``receiver``."""
        raise NotImplementedError


class ProgramNode(Node):
    """<program> ::= "program" <command list>"""

    def __init__(self, body: "CommandListNode") -> None:
        self._body = body

    @classmethod
    def parse(cls, context: Context) -> "ProgramNode":
        context.expect("program")
        return cls(CommandListNode.parse(context))

    def execute(self, receiver: CommandReceiver) -> None:
        self._body.execute(receiver)

    def __repr__(self) -> str:
        return f"[program {self._body!r}]"


class CommandListNode(Node):
    """<command list> ::= <command>* "end" """

    def __init__(self, commands: List["CommandNode"]) -> None:
        self._commands = list(commands)

    @classmethod
    def parse(cls, context: Context) -> "CommandListNode":
        commands: List[CommandNode] = []
        while True:
            token = context.current_token
            if token is None:
                raise ParseError("missing 'end'")
            if token == "end":
                context.advance()
                return cls(commands)
            commands.append(CommandNode.parse(context))

    def execute(self, receiver: CommandReceiver) -> None:
        for command in self._commands:
            command.execute(receiver)

    def __repr__(self) -> str:
        return "[" + ", ".join(repr(c) for c in self._commands) + "]"


class CommandNode(Node):
    """<command> ::= <repeat command> | <primitive command>

    An alternative rule: it produces no node of its own, it only decides
    which sub-rule applies by peeking at the current token.
    """

    @classmethod
    def parse(cls, context: Context) -> "CommandNode":
        if context.current_token == "repeat":
            return RepeatNode.parse(context)
        return PrimitiveNode.parse(context)


class RepeatNode(CommandNode):
    """<repeat command> ::= "repeat" <number> <command list>

    A NonterminalExpression: it contains another expression (its body)
    and its interpretation loops over the body's interpretation. Because
    the body may itself contain repeats, nesting comes for free.
    """

    def __init__(self, count: int, body: CommandListNode) -> None:
        self._count = count
        self._body = body

    @classmethod
    def parse(cls, context: Context) -> "RepeatNode":
        context.expect("repeat")
        count = context.read_number()
        return cls(count, CommandListNode.parse(context))

    def execute(self, receiver: CommandReceiver) -> None:
        for _ in range(self._count):
            self._body.execute(receiver)

    def __repr__(self) -> str:
        return f"[repeat {self._count} {self._body!r}]"


class PrimitiveNode(CommandNode):
    """<primitive command> ::= "go" | "right" | "left"

    A TerminalExpression: it contains no sub-expressions. Interpreting it
    performs one concrete action on the receiver.
    """

    _VALID = ("go", "right", "left")

    def __init__(self, word: str) -> None:
        self._word = word

    @classmethod
    def parse(cls, context: Context) -> "PrimitiveNode":
        token = context.current_token
        if token not in cls._VALID:
            raise ParseError(f"unknown command {token!r}")
        context.advance()
        return cls(token)

    def execute(self, receiver: CommandReceiver) -> None:
        if self._word == "go":
            receiver.go()
        elif self._word == "right":
            receiver.turn_right()
        else:  # "left"
            receiver.turn_left()

    def __repr__(self) -> str:
        return self._word


def parse(program_text: str) -> ProgramNode:
    """Parse a whole program text into a syntax tree.

    The convenience entry point client code should use: it wraps the text
    in a :class:`Context`, parses a ``<program>``, and verifies nothing is
    left over afterwards.
    """
    context = Context(program_text)
    tree = ProgramNode.parse(context)
    if context.current_token is not None:
        raise ParseError(
            f"unexpected token {context.current_token!r} after program end"
        )
    return tree
